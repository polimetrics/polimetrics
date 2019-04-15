try:
    import json
except ImportError:
    import simplejson as json

import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
tweets = api.search(q="Sanders", count=10, lang='en')

for i in tweets:
    print(i)


