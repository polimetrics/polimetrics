from django.contrib import admin
from .models import Candidate, Tweet, Developer

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'description', 'image')
    exclude = ('slug',)

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'text', 'followers', 'id_str', 'created_at', 'polarity', 'subjectivity', 'location')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('image', 'name', 'header', 'bio', 'fav_album', 'fav_coffee', 'fav_president')
