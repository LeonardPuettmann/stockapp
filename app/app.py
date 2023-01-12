import json
import requests
import streamlit as st
import plotly.graph_objects as go
import datetime
import constants

from sentiment import get_news, get_sentiment
from util import get_data

# Sidebar
st.sidebar.subheader('Query parameters')

# Preset interval for the date
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.datetime.today())

# Ticker data
ticker_list = open("app\\snp500.txt", "r").read().split()
ticker_symbol = st.sidebar.selectbox('Stock ticker', ticker_list) 

ticker_df = get_data(symbol=ticker_symbol, function="TIME_SERIES_DAILY_ADJUSTED", outputsize="full", interval="")

# Get news and sentiment 
news = get_news(ticker_symbol)
sentiment, values = get_sentiment(news["description"])

# Header col
st.header(ticker_symbol)

# Indicator for enviromental, social and governance score
col1, col2, col3 = st.columns(3)

# Indicator for the calculated seniment score
compound_sentiment = round((1 - sum(values)/7) * 100, 2)
if compound_sentiment >= 90.0:
    col1.metric('Sentiment score', f'{compound_sentiment} %', 'Amazing')
elif compound_sentiment >= 80.0:
    col1.metric('Sentiment score', f'{compound_sentiment} %', 'Good')
elif compound_sentiment >= 60.0:
    col1.metric('Sentiment score', f'{compound_sentiment} %', 'Alright')
elif compound_sentiment >= 40.0:
    col1.metric('Sentiment score', f'{compound_sentiment} %', 'Neutral', delta_color="inverse")
elif compound_sentiment < 40.0:
    col1.metric('Sentiment score', f'{compound_sentiment} %', 'Horrible', delta_color="inverse")

# Indicator for the predicted price
# call model hosted on Azure Function app
URL = constants.STOCK_ENDPOINT_URL
headers = {"Content-type": "application/json"}
req = requests.post(URL, json=json.dumps({"symbol": f"{ticker_symbol}"}))

price_pred = float(req.text)
last_close = ticker_df.iloc[1].close 
current_price = get_data(symbol=ticker_symbol)
current_price = current_price.iloc[0].close  
delta = price_pred - current_price

# Display the other columns
col2.metric('Price prediction', f'{price_pred} USD', round(delta, 2))
col3.metric('Current price', f'{current_price} USD', round(delta, 2))

# Filter data by the selected data
ticker_df = ticker_df[
    (ticker_df["timestamp"] > start_date.strftime("%Y-%d-%m")) & 
    (ticker_df["timestamp"] < end_date.strftime("%Y-%d-%m"))
]

# Plot with ploly
fig = go.Figure(data=go.Ohlc(x=ticker_df.timestamp,
                    open=ticker_df['open'],
                    high=ticker_df['high'],
                    low=ticker_df['low'],
                    close=ticker_df['close'],
                    increasing_line_color= 'lightgreen', 
                    decreasing_line_color= 'lightcoral'))

st.plotly_chart(fig, use_container_width=True)

news_col1, news_col2, news_col3 = st.columns(3)
with news_col1:
    st.caption(f':blue[{news["provider"][0]}]')
    st.markdown(news["description"][0].replace("$", "\$"))
with news_col2:
    st.caption(f':blue[{news["provider"][1]}]')
    st.markdown(news["description"][1].replace("$", "\$"))
with news_col3:
    st.caption(f':blue[{news["provider"][2]}]')
    st.markdown(news["description"][2].replace("$", "\$"))

news_col4, news_col5, news_col6 = st.columns(3)
with news_col4:
    st.caption(f':blue[{news["provider"][3]}]')
    st.markdown(news["description"][3].replace("$", "\$"))
with news_col5:
    st.caption(f':blue[{news["provider"][4]}]')
    st.markdown(news["description"][4].replace("$", "\$"))
with news_col6:
    st.caption(f':blue[{news["provider"][5]}]')
    st.markdown(news["description"][5].replace("$", "\$"))


# Mandatory warining 
st.markdown("---")
st.caption("If you want to support me, you can buy me a coffee here: :orange[https://www.buymeacoffee.com/leopuettmaw]")
st.caption("Made by Leonard Püttmann. No investment advice. Please do your own research before investing and be aware of the risks that come when investing into the stock market. \
    information on this site may not be correct or out of date at times.")