from django.core.management.base import BaseCommand
# from core.api_key import access_secret, access_token, consumer_key, consumer_secret
from textblob import TextBlob
from core.models import Tweet, Candidate
from django.conf import settings
import tweepy
import re 
from datetime import datetime, timezone, timedelta
import argparse
from django.db.utils import DataError

class Command(BaseCommand):

    def add_arguments(self, parser):
        def valid_date(s):
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except ValueError:
                msg = "Not a valid date: '{0}'.".format(s)
                raise argparse.ArgumentTypeError(msg)

        parser.add_argument('-a', '--all', help='Collect tweets for all candidates in the database', action='store_true', default=False)
        parser.add_argument('-n', '--name', nargs=2, help='The first and last name of the candidate to search')
        parser.add_argument('-c', '--count', help='The number of tweets to fetch', type=int, default=10)
        parser.add_argument('-d', '--date', help='The Date at which to calculate - format YYYY-MM-DD', type=valid_date, default=datetime.utcnow())

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def handle(self, *args, **options):
        # Variables that contains the user credentials to access Twitter API 

        ACCESS_TOKEN = settings.ACCESS_TOKEN
        ACCESS_SECRET = settings.ACCESS_SECRET
        CONSUMER_KEY = settings.CONSUMER_KEY
        CONSUMER_SECRET = settings.CONSUMER_SECRET

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        utc_date_str = (options['date'] + timedelta(days=1)).strftime("%Y-%m-%d")
        num_terms = options['count']

        candidates = []

        if options['all']:
            for candidate in Candidate.objects.all():
                candidates.append(str(candidate).lower())

        if options['name']:
            first_name=options['name'][0].lower() 
            last_name=options['name'][1].lower()
            temp_name = first_name + " " + last_name
            if temp_name not in candidates:
                candidates.append(temp_name)

        tweets = []

        for candidate in candidates:
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

            # searching for tweets
            tweets = tweepy.Cursor(api.search, q=candidate, until=utc_date_str, lang = "en").items(num_terms)

            first_name, last_name = candidate.split()

            new_candidate, _ = Candidate.objects.get_or_create(
                first_name=first_name,
                last_name=last_name
            )
            
            i = 0
            for tweet in tweets:
                textBlob = TextBlob(self.clean_tweet(tweet.text))
                temp_polarity = textBlob.sentiment.polarity
                temp_subjectivity = textBlob.sentiment.subjectivity
                temp_sentiment = temp_polarity * (1-temp_subjectivity/2)
                i += 1
                try:
                    Tweet.objects.create(
                        candidate = new_candidate,
                        text = tweet.text,
                        followers = tweet.user.followers_count,
                        created_at = tweet.created_at.replace(tzinfo=timezone.utc),
                        polarity = temp_polarity,
                        subjectivity = temp_subjectivity,
                        location = tweet.user.location[:100],
                        sentiment = temp_sentiment,
                        retweet_count = tweet.retweet_count,
                        favorite_count = tweet.retweeted_status.favorite_count if hasattr(tweet, 'retweeted_status') else tweet.favorite_count,
                        tweet_id = tweet.id_str,
                        retweeted_id = tweet.retweeted_status.id_str if hasattr(tweet, 'retweeted_status') else None
                    )
                except DataError:
                    pass
            print('Finished writing {0} tweets for {1}'.format(i, candidate))
        print(Tweet.objects.all().count())
