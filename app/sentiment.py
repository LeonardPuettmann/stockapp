import pandas as pd
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# load Bert model
tokenizer = AutoTokenizer.from_pretrained('zhayunduo/roberta-base-stocktwits-finetuned')
model = AutoModelForSequenceClassification.from_pretrained('zhayunduo/roberta-base-stocktwits-finetuned')

# Function to get news from finwiz
def get_news(ticker):
    '''
    Function to scrape news headlines from finviz, a site for finance news. Returns a list of headlines with the corresponding date.m 

    Args:
    - ticker: name of the ticker of a company (e.g. MSFT, AAPL, etc.).
    '''
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    url = finwiz_url + ticker
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)    

    # Read the contents of the file into 'html'
    html = BeautifulSoup(response, features='lxml')

    # Find 'news-table' in the Soup and load it into 'news_table'
    news_table = html.find(id='news-table')

    # Add the table to our dictionary
    news_tables[ticker] = news_table

    # Read one single day of headlines for ‘AMZN’ 
    company = news_tables[ticker]
    # Get all the table rows tagged in HTML with <tr> into ‘amzn_tr’
    company_tr = company.findAll('tr')

    news_list = []
    news_date = []
    for i, table_row in enumerate(company_tr):
        # Read the text of the element ‘a’ into ‘link_text’
        a_text = table_row.a.text
        # Read the text of the element ‘td’ into ‘data_text’
        td_text = table_row.td.text
        # Print the contents of ‘link_text’ and ‘data_text’ 
        news_list.append(a_text)
        news_date.append(td_text)

        # Exit after printing 4 rows of data
        if i == 20:
            break
    
    return (news_list, news_date)

def get_sentiment(headlines, model, tokenizer):
    '''
    Takes in a list of headlines and uses a BERT model to get the sentiment of the headline.

    Args:
    - headlines: list of headline of stock news.
    - model: already loaded bert model to get sentiments.
    - tokenizer: already loaded bert model to tokenize the text inputs.
    '''
    news_sentiment = []
    news_values = []
    for headline in headlines:
        hl_token = tokenizer.encode(headline, return_tensors='pt')
        hl_sentiment = model(hl_token)
        if int(torch.argmax(hl_sentiment.logits)) == 1:
            news_sentiment.append('Positive') 
            news_values.append(1)
        else:
            news_sentiment.append('Negative')
            news_values.append(0)

    return (news_sentiment, news_values)
