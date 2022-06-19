import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import pandas as pd
import xgboost as xgb
import yfinance as yf
import datetime

from operator import attrgetter
from xgboost import plot_importance, plot_tree

def relative_strength_idx(df, n=14):
    '''
    Function to calculate the relative strenght index (RSI). The RSI indicates if a stock is overbought oder undersold.

    Args:
    - df: A pandas DataFrame of closing prices for a stock.
    '''
    close = df['Close']

    delta = close.diff()
    delta = delta[1:]

    pricesUp = delta.copy()
    pricesDown = delta.copy()
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0

    rollUp = pricesUp.rolling(n).mean()
    rollDown = pricesDown.abs().rolling(n).mean()

    rs = rollUp / rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def predict_price(ticker):
    '''
    Uses extreme gradient boosting algorithm to predict the future price of a stock.

    Args:
    - ticker: name of the ticker of a company (e.g. MSFT, AAPL, etc.).
    '''
    try:
        # Load in Microsoft Stock Data 
        stock = yf.Ticker(ticker)
        history = stock.history(period='max', interval='1d')
        hist_data = history['Close']

        # Printing out the header
        df = pd.DataFrame(history)
        df.head()

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        df = df['2020-01-04':today]

        df['EMA_9'] = df['Close'].ewm(9).mean().shift()
        df['SMA_5'] = df['Close'].rolling(5).mean().shift()
        df['SMA_10'] = df['Close'].rolling(10).mean().shift()
        df['SMA_15'] = df['Close'].rolling(15).mean().shift()
        df['SMA_30'] = df['Close'].rolling(30).mean().shift()

        df['RSI'] = relative_strength_idx(df).fillna(0)

        EMA_12 = pd.Series(df['Close'].ewm(span=12, min_periods=12).mean())
        EMA_26 = pd.Series(df['Close'].ewm(span=26, min_periods=26).mean())

        df['MACD'] = pd.Series(EMA_12 - EMA_26)
        df['MACD_signal'] = pd.Series(df.MACD.ewm(span=9, min_periods=9).mean())
        df['Close'] = df['Close'].shift(-1)
    
        # Moving averages and MACD line
        df = df.iloc[33:] 
        # Shifting close price
        df = df[:-1]      
        df.index = range(len(df))

        test_size  = 0.10
        valid_size = 0.10

        test_split_idx  = int(df.shape[0] * (1-test_size))
        valid_split_idx = int(df.shape[0] * (1-(valid_size+test_size)))

        train_df  = df.loc[:valid_split_idx].copy()
        valid_df  = df.loc[valid_split_idx+1:test_split_idx].copy()
        test_df   = df.loc[test_split_idx+1:].copy()

        drop_cols = ['Volume', 'Open', 'Low', 'High']

        train_df = train_df.drop(drop_cols, 1)
        valid_df = valid_df.drop(drop_cols, 1)
        test_df  = test_df.drop(drop_cols, 1)

        y_train = train_df['Close'].copy()
        X_train = train_df.drop(['Close'], 1)

        y_valid = valid_df['Close'].copy()
        X_valid = valid_df.drop(['Close'], 1)

        y_test  = test_df['Close'].copy()
        X_test  = test_df.drop(['Close'], 1)

        model = xgb.XGBRegressor(n_estimators=700, 
            gamma=0.03, 
            learning_rate=0.005, 
            max_depth=12,
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Get last prediction
        last_prediction = y_pred[-1]

    except:
        pass

    return last_prediction
