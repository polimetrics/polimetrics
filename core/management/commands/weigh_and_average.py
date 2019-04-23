from django.core.management.base import BaseCommand, CommandError
from core.models import Tweet, Candidate, CandidateMeanSentiment
from datetime import datetime, timezone
import argparse
from django.utils.timezone import make_aware

class Command(BaseCommand):

    help = 'Calculates sentiment by applying weighing algorithm(i.e. engagement = retweets + favorites, followers), and calculates an average per candidate on given time-slice availabe in the database'

    def add_arguments(self, parser):
        def valid_date(s):
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except ValueError:
                msg = "Not a valid date: '{0}'.".format(s)
                raise argparse.ArgumentTypeError(msg)

        parser.add_argument('command', nargs='?', choices=['daily', 'total'], default='daily')
        parser.add_argument('-d', '--date', help='The Date at which to calculate - format YYYY-MM-DD', type=valid_date)

    def handle(self, *args, **options):

        self.candidates = Candidate.objects.all()
        self.tweets = {}
        
        current_utc = datetime.utcnow()
        day = current_utc.day
        month = current_utc.month
        year = current_utc.year

        if 'daily' in options['command']:

            for candidate in self.candidates:
                total_favorites = 0
                total_retweets = 0
                weighted_sentiments = []
                from_dt = datetime(year, month, day, tzinfo=timezone.utc)
                to_dt = datetime(year, month, day+1, tzinfo=timezone.utc)
                temp_tweets = Tweet.objects.filter(
                    candidate=candidate, 
                    created_at__gte=from_dt,
                    created_at__lte=to_dt
                )

                # clean out unique retweeted_ids to hold only one record per. 
                # If retweeted_id doesn't exist (i.e. tweet wasn't retweeted) then
                # store the tweet_id with the same values.  (favorite_count, retweet_count, sentiment)
                for tweet in temp_tweets:
                    if tweet.retweeted_id:
                        self.tweets[tweet.retweeted_id] = [tweet.favorite_count, tweet.retweet_count, tweet.sentiment]
                    else:
                        self.tweets[tweet.tweet_id] = [tweet.favorite_count, tweet.retweet_count, tweet.sentiment]
                
                # Loop through the unique retweeted_id tweet_id values in the dictionary from above
                # and sum the favorites and retweet counts for each in a running total
                for vals in self.tweets.values():
                    total_favorites += vals[0]
                    total_retweets += vals[1]

                # add them together to compute "total engagement" for the candidate
                total_engagement = total_favorites + total_retweets

                # Computed weighted sentiment value for each unique tweet
                # Store them in a list called weighted_sentiments
                for vals in self.tweets.values():
                    weighted_sentiments.append(vals[2] * (vals[0] + vals[1])/total_engagement)
                
                # sum the entire list to compute the mean daily sentiment for the candidate
                mean_daily_sentiment = sum(weighted_sentiments)

                # create the record in the database
                # set the from time to be today UTC 00:00:00
                # set the to time to be tomorrow 00:00:00
                # i.e. 24 hours time slice
                cms = CandidateMeanSentiment.objects.create(
                    candidate = candidate,
                    mean_sentiment = mean_daily_sentiment,
                    from_date_time = make_aware(datetime(year, month, day)),
                    to_date_time = make_aware(datetime(year, month, day+1))
                )

        if 'total' in options['command']:
            # do something else
            pass
