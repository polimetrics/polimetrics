from django.core.management.base import BaseCommand, CommandError
from core.models import Tweet, Candidate, CandidateMeanSentiment
from datetime import datetime, timezone
import argparse
from django.db.models import Sum

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

    def calculate_weighted_sentiments(self, tweets, total_engagement):
        weighted_sentiment = 0
        for tweet in tweets:
            engagement = tweet.favorite_count + tweet.retweet_count
            engagement = 1 if engagement == 0 else engagement + 1 # engagement is at least 1
            weighted_sentiment += tweet.sentiment * engagement/total_engagement
        return weighted_sentiment

    def handle(self, *args, **options):

        utc_date = options['date']
        from_dt = datetime(utc_date.year, utc_date.month, utc_date.day, tzinfo=timezone.utc)
        if options['overall']:
            tweet = Tweet.objects.earliest('created_at')
            from_dt = tweet.created_at

        to_dt = datetime(utc_date.year, utc_date.month, utc_date.day + 1, tzinfo=timezone.utc)

        for candidate in Candidate.objects.all():

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
            temp_tweets = unique_retweeted_tweets.union(unique_tweets)

            positive_engagement = 0
            negative_engagement = 0

            positive_tweets = []
            negative_tweets = []

            for tweet in temp_tweets:
                engagement = tweet.favorite_count + tweet.retweet_count
                engagement = 1 if engagement == 0 else engagement + 1 # engagement is at least 1
                sentiment = tweet.sentiment

                if sentiment > 0:
                    positive_tweets.append(tweet)
                    positive_engagement += engagement
                elif sentiment < 0:
                    negative_tweets.append(tweet)
                    negative_engagement += engagement

            mean_positive_sentiment = self.calculate_weighted_sentiments(positive_tweets, positive_engagement)
            mean_negative_sentiment = self.calculate_weighted_sentiments(negative_tweets, negative_engagement)
            mean_overall_sentiment = self.calculate_weighted_sentiments(positive_tweets + negative_tweets, positive_engagement + negative_engagement)

            CandidateMeanSentiment.objects.create(
                candidate = candidate,
                mean_sentiment = mean_overall_sentiment,
                total_engagement = positive_engagement + negative_engagement,
                from_date_time = from_dt,
                to_date_time = to_dt,
                negative_engagement = negative_engagement,
                negative_mean_sentiment = mean_negative_sentiment,
                positive_engagement = positive_engagement,
                positive_mean_sentiment = mean_positive_sentiment,
                num_negative_tweets = len(negative_tweets),
                num_positive_tweets = len(positive_tweets)
            )
