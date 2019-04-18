from django.core.management.base import BaseCommand
from core.api_key import access_secret, access_token, consumer_key, consumer_secret
from textblob import TextBlob
from core.models import Tweet, Candidate
from django.conf import settings
import tweepy

class Command(BaseCommand):

    def __init__(self):
        self.tweets = []
        self.candidate = []

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
        self.candidate = input("Enter Keyword/Tag/Name to search about: ")
        num_terms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=self.candidate, lang = "en").items(num_terms)

        new_candidate, _ = Candidate.objects.get_or_create(name=self.candidate)

        for tweet in self.tweets:

            tweet = Tweet.objects.create(
                candidate = new_candidate,
                id_str = tweet.id_str,
                created_at = tweet.created_at,
                polarity = TextBlob(tweet.text).sentiment.polarity,
                subjectivity = TextBlob(tweet.text).sentiment.subjectivity,
                location = tweet.user.location,
            )
