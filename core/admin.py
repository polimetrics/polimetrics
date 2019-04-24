from django.contrib import admin
from .models import Candidate, Tweet, Developer, CandidateMeanSentiment

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'description', 'image')
    exclude = ('slug',)

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'text', 'followers', 'created_at', 'polarity', 'subjectivity', 'location', 'sentiment', 'retweet_count', 'favorite_count', 'tweet_id', 'retweeted_id')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('image', 'name', 'header', 'bio', 'fav_album', 'fav_coffee', 'fav_president')

@admin.register(CandidateMeanSentiment)
class CandidateMeanSentiment(admin.ModelAdmin):
    list_display = ('candidate', 'mean_sentiment', 'from_date_time', 'to_date_time', 'created_at')
