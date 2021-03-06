from lib2to3.pgen2 import token
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime
import yfinance as yf
from operator import attrgetter

from transformers import AutoTokenizer, AutoModelForSequenceClassification

from sentiment import get_news, get_sentiment
from predict import predict_price

# load Bert model
tokenizer = AutoTokenizer.from_pretrained('zhayunduo/roberta-base-stocktwits-finetuned')
model = AutoModelForSequenceClassification.from_pretrained('zhayunduo/roberta-base-stocktwits-finetuned')

# Sidebar
st.sidebar.subheader('Query parameters')

# Get current date
attrs = ('year', 'month', 'day')
now = datetime.datetime.today()
today = attrgetter(*attrs)(now)

# Preset interval for the date
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", now)

# Ticker data
ticker_list = pd.read_csv('snp500.txt')
ticker_symbol = st.sidebar.selectbox('Stock ticker', ticker_list) 
ticker_data = yf.Ticker(ticker_symbol) 
ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date) 

# Get news and sentiment 
news, date = get_news(ticker_symbol)
sentiment, values = get_sentiment(news, model, tokenizer)

# Ticker information
string_logo = '<img src=%s>' % ticker_data.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = ticker_data.info['longName']
st.header('**%s**' % string_name)

# Indicator for enviromental, social and governance score
col1, col2, col3 = st.columns(3)

# Indicator for the calculated seniment score
if sum(values) >= 14:
    col1.metric('Sentiment score', f'{(sum(values) * 5) - 5} %', 'Great')
elif sum(values) >= 7:
    col1.metric('Sentiment score', f'{sum(values) * 5} %', 'Medium')
else:
    col1.metric('Sentiment score', f'{sum(values) * 5} %', 'Bad')

# Indicator for the predicted price
price_pred = predict_price(ticker_symbol)
rounded_price = round(int(price_pred), 2)
last_close = ticker_df.Close[-1] 
rounded_last_close = round(last_close, 2)
delta = price_pred - last_close
col2.metric('Price prediction', f'{rounded_price} USD', round(delta, 2))

# Indicator for suistainability
week_price = ticker_df.Close[-5]
week_delta = last_close - week_price
col3.metric('Current Price', f'{rounded_last_close} USD', round(week_delta, 2))

# Plot with ploly
fig = go.Figure(data=go.Ohlc(x=ticker_df.index,
                    open=ticker_df['Open'],
                    high=ticker_df['High'],
                    low=ticker_df['Low'],
                    close=ticker_df['Close'],
                    increasing_line_color= 'lightgreen', 
                    decreasing_line_color= 'lightcoral'))

st.plotly_chart(fig, use_container_width=True)

# Print current news and sentiment
st.subheader('Current news and sentiments')
sentiment_df = pd.DataFrame({'Headline': news, 'Sentiment': sentiment})
st.dataframe(sentiment_df, width=1000)

# Mandatory warining 
st.write('This site is no investment advice. Please do your own research before investing and be aware of the risks that come when investing into the stock market. \
    information on this site may not be correct or out of date at times.')
#st.write(tickerData.info)