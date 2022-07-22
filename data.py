import requests
from datetime import timedelta, date

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "https://www.alphavantage.co/query"
STOCK_KEY = "ED114Y82ATB0FZG4"
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_KEY = "96913bf2f5d14544bbdd71010655b62c"

today = date.today()
yesterday = today - timedelta(days=1)
day_before = today - timedelta(days=2)
month_ago = today - timedelta(days=30)


def fetch_stock_data():
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "datatype": "json",
        "apikey": STOCK_KEY
    }

    stock_response = requests.get(STOCK_API, params=stock_parameters)
    stock_response.raise_for_status()
    stock_data = stock_response.json()
    return stock_data


def fetch_news_data():
    news_parameters = {
        "q": COMPANY_NAME,
        "from": str(month_ago),
        "sortBy": "popularity",
        "apiKey": NEWS_KEY,
        "pageSize": 3,
        "page": 1
    }
    news_response = requests.get(NEWS_API, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    return news_data