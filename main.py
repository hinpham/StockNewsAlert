import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = 'APIKEY'
NEWS_API = 'APIKEY2'

account_sid = "SID"
auth_token = "TOKEN"
PHONE = "NUMBER"

stock_parameters = {
  'function': "TIME_SERIES_DAILY",
  'symbol' : STOCK_NAME,
  'apikey' : STOCK_API,
}

#Get yesterday's closing stock price.
r = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = r.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price, yesterday_opening_price = yesterday_data["4. close"], yesterday_data['1. open']
print(yesterday_closing_price)


#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_closing_price = day_before_yesterday_data["4. close"]
print(day_before_closing_price)


difference = abs(float(yesterday_closing_price) - float(day_before_closing_price))
print(difference)


diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)


if diff_percent > 3:
  print("GEt news")
  news_parameters = {
   'apiKey': NEWS_API,
   'qInTitle': COMPANY_NAME,
  }
  
  news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
  articles = news_response.json()['articles']



#Use Python slice operator to create a list that contains the first 3 articles
  three_articles = articles[:3]
  #print(three_articles)

  articles_info = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
  #print(articles_info)
#Send each article as a separate message via Twilio.
  client = Client(account_sid, auth_token)

  for article in articles_info:
    message = client.messages.create(
      body=article,
      from_=PHONE,
      to="YOUR_PHONE",
    )

    print(message.status)
