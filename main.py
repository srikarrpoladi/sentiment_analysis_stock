from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import pandas as pd
import matplotlib.pyplot as plt


finviz_url = "https://finviz.com/quote.ashx?t="
tickers = ["AMZN", "AMD", "FB"]

news_tables = {}

for ticker in tickers:
    url = finviz_url+ticker

    req = Request(url=url, headers={"user-agent":'my-app'})
    response = urlopen(req)
    
    html = BeautifulSoup(response, features='html.parser')
    
    news_table = html.find(id="news-table")
    news_tables[ticker] = news_table

    break
'''
amzn_data = news_tables["AMZN"]
amzn_rows = amzn_data.findAll("tr")

for index,row in enumerate(amzn_rows):
    title = row.a.text
    timestamp = row.td.text

'''

parsed_data = []

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        a_tag = row.find('a', class_='tab-link-news')
        
        if a_tag:
            title = a_tag.text
            date_data = row.td.text.split()

            if len(date_data) == 2:
                date = date_data[0]
                time = date_data[1]
            else:
                time = date_data


            parsed_data.append([ticker, date, time, title])
        else:
            # Handle cases where a_tag is None, if necessary
            continue
        
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

vader = SentimentIntensityAnalyzer()

f = lambda title: vader.polarity_scores(title)["compound"]
df['compound'] = df["title"].apply(f)

df["date"] = df["date"].apply(lambda x: "07-25-24" if x == "Today" else x)
df["date"] = pd.to_datetime(df.date).dt.date

plt.figure(figsize=(10,8))

df["date"]
mean_df = df.groupby(['ticker','date']).mean()
print(mean_df)



