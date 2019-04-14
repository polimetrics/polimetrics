from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Candidate(models.Model):
    '''This model represents a candidate'''
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    party = models.CharField(max_length=32)
    about = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='core/static/img', blank=True)
    slug = models.SlugField()

    def set_slug(self):
        '''Creates a unique slug for every candidate'''
        if self.slug:
            return
          
    def save(self, *args, **kwargs):
        '''Hides slug field in admin & saves slug to use in url'''
        self.set_slug()
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('candidate-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.last_name

class Sentiment(models.Model):
    '''This model represents the sentiment '''
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    average = models.IntegerField(null=True, blank=True)
    positive = models.IntegerField(null=True, blank=True)
    negative = models.IntegerField(null=True, blank=True)
    highest = models.IntegerField(null=True, blank=True)
    lowest = models.IntegerField(null=True, blank=True)
    