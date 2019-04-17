from api_key import access_secret, access_token, consumer_key, consumer_secret
from pandas import DataFrame
from textblob import TextBlob
import csv
import os.path


try:
    import json
except ImportError:
    import simplejson as json

import tweepy

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []

    def DownloadData(self):
        # Variables that contains the user credentials to access Twitter API 
        ACCESS_TOKEN = access_token
        ACCESS_SECRET = access_secret
        CONSUMER_KEY = consumer_key
        CONSUMER_SECRET = consumer_secret

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

        # input for term to be searched and how many tweets to search
        searchTerms = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerms, lang = "en").items(NoOfTerms)

        for tweet in self.tweets:

            file_exists = os.path.isfile('result.csv')

            with open('result.csv', 'a', newline='') as csvfile:
                headers = ['politician', 'id', 'timeStamp', 'analysis', 'location']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                a = searchTerms
                b = tweet.id_str
                c = tweet.created_at
                d = TextBlob(tweet.text).sentiment
                e = tweet.user.location

                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    'politician': a,
                    'id': b,
                    'timeStamp': c,
                    'analysis': d,
                    'location': e,
                })

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
