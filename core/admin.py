from django.contrib import admin
from .models import Candidate

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'about', 'image')
    exclude = ('slug',)

# @admin.register(Sentiment)
# class SnippetAdmin(admin.ModelAdmin):
#     list_display = ('candidate', 'average', 'positive', 'negative', 'highest', 'lowest')
