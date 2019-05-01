from django.core.management.base import BaseCommand
from core.models import Tweet, Candidate, CandidateMeanSentiment
from datetime import datetime, timezone, timedelta
import argparse

class Command(BaseCommand):

    help = 'Calculates sentiment by applying weighing algorithm(i.e. engagement = retweets + favorites, followers), and calculates an average per candidate on given time-slice availabe in the database'

    def add_arguments(self, parser):
        def valid_date(s):
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except ValueError:
                msg = "Not a valid date: '{0}'.".format(s)
                raise argparse.ArgumentTypeError(msg)

        parser.add_argument('-o', '--overall', action='store_true', default=False)
        parser.add_argument('-d', '--date', help='The Date at which to calculate - format YYYY-MM-DD', type=valid_date, default=datetime.utcnow())

    def calculate_engagement(self, tweet):
        engagement = tweet.favorite_count + tweet.retweet_count
        engagement = 1 if engagement == 0 else engagement + 1 # engagement is at least 1
        return engagement

    def calculate_weighted_sentiments(self, tweets, total_engagement):
        weighted_sentiment = 0
        for tweet in tweets:
            engagement = self.calculate_engagement(tweet)
            weighted_sentiment += tweet.sentiment * engagement/total_engagement
        return weighted_sentiment

    def get_unique_tweets(self, candidate, from_dt, to_dt):
        
        unique_retweeted_tweets = Tweet.objects.order_by('retweeted_id', '-created_at').distinct('retweeted_id').filter(
            candidate=candidate, 
            created_at__gte=from_dt,
            created_at__lte=to_dt,
        ).exclude(retweeted_id=None)

        unique_tweets = Tweet.objects.filter(
            candidate=candidate, 
            created_at__gte=from_dt,
            created_at__lte=to_dt,
            retweeted_id=None
        )
        return unique_retweeted_tweets.union(unique_tweets)

    def handle(self, *args, **options):

        from_dt = datetime(options['date'].year, options['date'].month, options['date'].day, tzinfo=timezone.utc) - timedelta(days=1)
        if options['overall']:
            tweet = Tweet.objects.earliest('created_at')
            from_dt = datetime(tweet.created_at.year, tweet.created_at.month, tweet.created_at.day, tzinfo=timezone.utc)

        to_dt = datetime(options['date'].year, options['date'].month, options['date'].day, tzinfo=timezone.utc)

        for candidate in Candidate.objects.all():
            
            candidate_tweets = self.get_unique_tweets(candidate, from_dt, to_dt)

            positive_engagement = 0
            negative_engagement = 0

            positive_tweets = []
            negative_tweets = []

            for tweet in candidate_tweets:
                engagement = self.calculate_engagement(tweet)
                sentiment = tweet.sentiment

                if sentiment > 0:
                    positive_tweets.append(tweet)
                    positive_engagement += engagement
                elif sentiment < 0:
                    negative_tweets.append(tweet)
                    negative_engagement += engagement

            CandidateMeanSentiment.objects.create(
                candidate = candidate,
                mean_sentiment = self.calculate_weighted_sentiments(positive_tweets + negative_tweets, positive_engagement + negative_engagement),
                total_engagement = positive_engagement + negative_engagement,
                from_date_time = from_dt,
                to_date_time = to_dt,
                negative_engagement = negative_engagement,
                negative_mean_sentiment = self.calculate_weighted_sentiments(negative_tweets, negative_engagement),
                positive_engagement = positive_engagement,
                positive_mean_sentiment = self.calculate_weighted_sentiments(positive_tweets, positive_engagement),
                num_negative_tweets = len(negative_tweets),
                num_positive_tweets = len(positive_tweets)
            )
