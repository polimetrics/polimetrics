from django.contrib import admin
from .models import Candidate, Sentiment

# Register your models here.

@admin.register(Candidate)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'about', 'image')
    exclude = ('slug',)

# @admin.register(Sentiment)
# class SnippetAdmin(admin.ModelAdmin):
#     list_display = ('candidate', 'average', 'positive', 'negative', 'highest', 'lowest')
