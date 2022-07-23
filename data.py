import requests
from datetime import timedelta, date
from dotenv import load_dotenv
import os

load_dotenv()

STOCK = os.getenv('STOCK')
COMPANY_NAME = os.getenv('COMPANY_NAME')
STOCK_ENDPOINT = os.getenv('STOCK_ENDPOINT')
STOCK_KEY = os.getenv('STOCK_KEY')
NEWS_ENDPOINT = os.getenv('NEWS_ENDPOINT')
NEWS_KEY = os.getenv('NEWS_KEY')

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

    stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
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

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    return news_data
