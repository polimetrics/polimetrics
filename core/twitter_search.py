from api_key import access_secret, access_token, consumer_key, consumer_secret
try:
    import json
except ImportError:
    import simplejson as json

import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = access_token
ACCESS_SECRET = access_secret
CONSUMER_KEY = consumer_key
CONSUMER_SECRET = consumer_secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


tweets = api.search(q="Sanders", count=10, lang='en')

for tweet in tweets:
    print(tweet.text)


