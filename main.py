import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TIME_SERIES_DAILY_API = os.environ.get("TIME_SERIES_DAILY_API")

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["TWILIO_FROM_NUMBER"]
to_number = os.environ["TWILIO_TO_NUMBER"]

parameters = {
       "function": "TIME_SERIES_DAILY",
       "symbol": STOCK,
       "apikey": TIME_SERIES_DAILY_API,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()
# print(data)

time_series = data["Time Series (Daily)"]
daily_list = list(time_series.items())  # convert dict to list of tuples

latest_two = daily_list[:2]

print(latest_two)

yest_close = float(latest_two[0][1]["4. close"])
print(yest_close)
day_before_yest = float(latest_two[1][1]["4. close"])
print(day_before_yest)


up_down = None
difference = round(yest_close - day_before_yest)
if difference > 0:
       up_down = "🔺"
else:
       up_down = "🔻"
print(difference)
diff_percentage = round(((difference / yest_close) * 100),2)
print(diff_percentage)

if abs(diff_percentage) > 0.5:
       parameters_news = {
              "q": COMPANY_NAME,
              "apiKey": os.environ.get("NEWS_API"),

       }

       response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
       news_data = response_news.json()
       # print(news_data)

       articles = news_data["articles"]
       list_articles = list(articles)
       first_three_articles = list_articles[:3]

              # print(first_three_articles)


       client = Client(account_sid, auth_token)

       formatted_articles = [f"{STOCK}: {up_down}{diff_percentage}% \nHeadline: {article['title']}. \nBrief: {article['description']}." for article in first_three_articles]

       print(formatted_articles)

       for article in formatted_articles:
              message = client.messages.create(
                  body=article,
                  from_=from_number,
                  to=to_number,
              )
              print(message.sid)
              print(message.status)