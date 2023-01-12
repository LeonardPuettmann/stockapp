import pandas as pd 
import constants

def prep_data(dataframe):
    # get rolling mean an exponential moving average
    dataframe["rolling_3_mean"] = dataframe["close"].shift(1).rolling(3).mean()
    dataframe["rolling_7_mean"] = dataframe["close"].shift(1).rolling(3).mean()
    dataframe["ewma"] = dataframe["close"].shift(1).ewm(alpha=0.5).mean()

    # convert timestamp to unix timecode 
    dataframe['unix_timestamp'] = pd.to_datetime(dataframe['timestamp']).astype(int)/ 10**9

    # get day of week and month
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe["weekday"] = dataframe['timestamp'].dt.dayofweek
    dataframe["month"] = dataframe['timestamp'].dt.month
    dataframe = dataframe.drop("timestamp", axis=1)

    # shift the target column 
    dataframe["close_shifted"] = dataframe["close"].shift(-1)
    return dataframe

def predict_price(model):
    # Get last 100 days of data
    dataframe = get_data(function="TIME_SERIES_DAILY_ADJUSTED", interval="")
    
    # Enrich and modify data
    dataframe = prep_data(dataframe)
    dataframe = dataframe.drop(["close", "close_shifted", "adjusted_close"], axis=1)

    # Get latest entry
    dataframe.iloc[0].to_frame().T

    # Predict on the latest entry
    new_pred = model.predict(dataframe.iloc[0].to_frame().T)

    # Return prediction
    return round(new_pred[0], 2)

def get_latest_price():
    dataframe = get_data()
    return dataframe.iloc[0]["close"]

def get_data(
    function = "TIME_SERIES_INTRADAY",
    symbol = "IBM",
    interval = "&interval=1min",
    outputsize = "compact",
    apikey = constants.ALPHAVANTAGE_KEY,
    ):

    return pd.read_csv(
        f"https://www.alphavantage.co/query?function={function}&symbol={symbol}{interval}&datatype=csv&outputsize={outputsize}&apikey={apikey}"
    )