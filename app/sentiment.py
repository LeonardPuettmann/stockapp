import requests
import constants
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_sentiment(headlines):
    analyzer = SentimentIntensityAnalyzer()

    sentiments = []
    compound_values = []
    for sentence in headlines:
        vs = analyzer.polarity_scores(sentence)
        compound_values.append(vs["compound"])

        if vs["compound"] >= 0.05:
            sentiments.append("positive")
        elif vs["compound"] > -0.05:
            sentiments.append("neutral")
        elif vs["compound"] <= -0.05:
            sentiments.append("negative")
        else:
            pass

    return sentiments, compound_values

def get_news(search_term):
    subscription_key = constants.BING_KEY
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "mkt": "en-US"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    headers = ["name", "description", "provider", "datePublished", "url"]

    results = {}
    for i in headers:
        if i == "provider": 
            providers = [article[i][0] for article in search_results["value"]]
            names = []
            for index in range(len(providers)):
                for key in providers[index]:
                    if key == "name":
                        names.append(providers[index][key])

            results[i] = names
        else: 
            part_of_response = [article[i] for article in search_results["value"]]
            results[i] = part_of_response
            
    if len(search_term) == 0:
        results["topic"] = ["popular"] * len(results["name"])
    else:
        results["topic"] = [search_term] * len(results["name"])

    return results
