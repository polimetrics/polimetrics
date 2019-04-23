from django.core.management.base import BaseCommand
# from core.api_key import access_secret, access_token, consumer_key, consumer_secret
from textblob import TextBlob
from core.models import Tweet, Candidate
from django.conf import settings
import tweepy
import re 
from django.utils.timezone import make_aware
import pytz

class Command(BaseCommand):

    

    def __init__(self):
        self.tweets = []
        self.candidate = []

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def handle(self, *args, **kwargs):
        # Variables that contains the user credentials to access Twitter API 

        ACCESS_TOKEN = settings.ACCESS_TOKEN
        ACCESS_SECRET = settings.ACCESS_SECRET
        CONSUMER_KEY = settings.CONSUMER_KEY
        CONSUMER_SECRET = settings.CONSUMER_SECRET

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

        # input for term to be searched and how many tweets to search
        self.candidate = input("Enter first and last name of candidate: ")
        num_terms = int(input("Enter how many tweets to search: "))

        temp_candidate = self.candidate.split()

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=self.candidate, lang = "en").items(num_terms)
        
        new_candidate, _ = Candidate.objects.get_or_create(first_name=temp_candidate[0].lower(), last_name=temp_candidate[1].lower())
        for tweet in self.tweets:
            print(tweet.created_at)
            print(tweet)
            textBlob = TextBlob(self.clean_tweet(tweet.text))
            temp_polarity = textBlob.sentiment.polarity
            temp_subjectivity = textBlob.sentiment.subjectivity
            temp_sentiment = temp_polarity * (1-temp_subjectivity/2)
            tweet = Tweet.objects.create(
                candidate = new_candidate,
                text = tweet.text,
                followers = tweet.user.followers_count,
                created_at = make_aware(tweet.created_at),
                polarity = temp_polarity,
                subjectivity = temp_subjectivity,
                location = tweet.user.location,
                sentiment = temp_sentiment,
                retweet_count = tweet.retweet_count,
                favorite_count = tweet.retweeted_status.favorite_count if hasattr(tweet, 'retweeted_status') else tweet.favorite_count,
                tweet_id = tweet.id_str,
                retweeted_id = tweet.retweeted_status.id_str if hasattr(tweet, 'retweeted_status') else None
            )
