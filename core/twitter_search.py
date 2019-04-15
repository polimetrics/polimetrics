try:
    import json
except ImportError:
    import simplejson as json

import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1116579167825305600-FICyHGcbHBv5weRMAArEjYEmQSkRVG'
ACCESS_SECRET = 'sAbozMP6ochwoOhDKZ2M0Z3uh4LWWhdRMvjIGyGcFgzUj'
CONSUMER_KEY = 'QWqHOOdvwYROiuAD7lDgZ45zU'
CONSUMER_SECRET = 'eNj1D3bOYCdwVaIYJy2w5ybzv7dwkV12gxkTUoK1PJYV4nu3tj'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
tweets = api.search(q="Sanders", count=10, lang='en')

for i in tweets:
    print(i)


