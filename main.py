import requests
from datetime import timedelta, date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header


def percentage_of_two_numbers(num1, num2):
    return ((num1 - num2) / num2) * 100


def send_mail(description, header):
    message = MIMEMultipart()
    message["From"] = f"{USER}"
    message["To"] = "nicolajlpedersen@gmail.com"
    message["Subject"] = Header(s=f"{header}", charset="utf-8")

    # Add the text message
    msg_text = MIMEText(_text=f"{description}", _subtype="plain", _charset="utf-8")
    message.attach(msg_text)

    with smtplib.SMTP("smtp.gmail.com", 587) as conn:
        conn.starttls()
        conn.login(user=USER, password=PASSWORD)
        conn.sendmail(
            from_addr=USER,
            to_addrs="nicolajlpedersen@gmail.com",
            msg=f"{message.as_string()}"
        )


today = date.today()
yesterday = today - timedelta(days=1)
day_before = today - timedelta(days=2)
month_ago = today - timedelta(days=30)

USER = "nicowishesyouahappybirthday@gmail.com"
PASSWORD = "xmebpypmfzhilrnk"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "https://www.alphavantage.co/query"
STOCK_KEY = "ED114Y82ATB0FZG4"
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_KEY = "96913bf2f5d14544bbdd71010655b62c"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": STOCK_KEY
}

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

stock_response = requests.get(STOCK_API, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
yesterday_closing_price = float(stock_data["Time Series (Daily)"][str(yesterday)]["4. close"])
day_before_closing_price = float(stock_data["Time Series (Daily)"][str(day_before)]["4. close"])
res = percentage_of_two_numbers(yesterday_closing_price, day_before_closing_price)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
message = ""
if res > 5 or res < -5:
    arrow_symbol = "🔺"
    if res < 0:
        arrow_symbol = "🔻"
    message += f"{STOCK} {arrow_symbol}{round(res, 2)}% \n\n"

    if len(news_data["articles"]) > 0:
        for x in news_data["articles"]:
            message += f"Headline: {x['title']}\n"
            message += f"Brief: {x['description']}\n"
            message += f"source: {x['source']['name']}\n\n"
    else:
        message += f"Couldn't find any news about {COMPANY_NAME}."

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    # Couldn't get access to SMS so it'll be with e-mail instead.
    subject = f"STOCK NEWS: {STOCK} {arrow_symbol}{round(res, 2)}% \n"
    send_mail(description=message, header=subject)
