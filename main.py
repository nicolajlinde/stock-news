from send_mail import send_mail
import data


def percentage_of_two_numbers(num1, num2):
    return ((num1 - num2) / num2) * 100


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
yesterday_closing_price = float(data.fetch_stock_data()["Time Series (Daily)"][str(data.yesterday)]["4. close"])
day_before_closing_price = float(data.fetch_stock_data()["Time Series (Daily)"][str(data.day_before)]["4. close"])
res = percentage_of_two_numbers(yesterday_closing_price, day_before_closing_price)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
message = ""
if res > 5 or res < -5:
    arrow_symbol = "🔺"
    if res < 0:
        arrow_symbol = "🔻"
    message += f"{data.STOCK} {arrow_symbol}{round(res, 2)}% \n\n"

    if len(data.fetch_news_data()["articles"]) > 0:
        for x in data.fetch_news_data()["articles"]:
            message += f"Headline: {x['title']}\n"
            message += f"Brief: {x['description']}\n"
            message += f"source: {x['source']['name']}\n\n"
    else:
        message += f"Couldn't find any news about {data.COMPANY_NAME}."

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    # Couldn't get access to SMS so it'll be with e-mail instead.
    subject = f"STOCK NEWS: {data.STOCK} {arrow_symbol}{round(res, 2)}% \n"
    send_mail(description=message, header=subject)
