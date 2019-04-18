from django.contrib import admin
from .models import Candidate, Tweet

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'about', 'image')
    exclude = ('slug',)

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'id_str', 'created_at', 'polarity', 'subjectivity', 'location')
