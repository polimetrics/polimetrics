from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Candidate(models.Model):
    '''This model represents a candidate'''
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, blank=False)
    party = models.CharField(max_length=150)
    description = models.TextField(max_length=1500, null=True, blank=True)
    image = models.ImageField(upload_to='core/static/img', blank=True, max_length=100)
    slug = models.SlugField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name']
    
    def set_slug(self):
        '''Creates a unique slug for every candidate'''
        if self.slug:
            return
        slug = slugify(self.first_name+ ' ' +self.last_name)
        self.slug = slug
          
    def save(self, *args, **kwargs):
        '''Hides slug field in admin & saves slug to use in url'''
        self.set_slug()
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('candidate_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()

class Tweet(models.Model):
    '''
    This model represents the specific info from our DB.
    '''
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    text = models.CharField(max_length=400, null=True)
    followers = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField()
    polarity = models.DecimalField(max_digits=10, decimal_places=9)
    subjectivity = models.DecimalField(max_digits=10, decimal_places=9)
    location = models.CharField(max_length=100)
    sentiment = models.DecimalField(max_digits=10, decimal_places=9)
    retweet_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    tweet_id = models.CharField(max_length=100)
    retweeted_id = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-created_at']

class CandidateMeanSentiment(models.Model):
    '''
    This model represents the mean sentiment per candidate on a given time-slice
    for all unique tweets and only account for retweets once.  
    Also, weights are applied to sentiment based on total retweet and favorite counts.  
    '''
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    mean_sentiment = models.DecimalField(max_digits=10, decimal_places=9)
    total_engagement = models.PositiveIntegerField(default=0)
    from_date_time = models.DateTimeField()
    to_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    positive_mean_sentiment = models.DecimalField(max_digits=10, decimal_places=9, default=0)
    positive_engagement = models.IntegerField(default=0)
    negative_mean_sentiment = models.DecimalField(max_digits=10, decimal_places=9, default=0)
    negative_engagement = models.IntegerField(default=0)    
    num_positive_tweets = models.IntegerField(default=0)
    num_negative_tweets = models.IntegerField(default=0)    

    class Meta:
        ordering = ['to_date_time', '-created_at']

class Developer(models.Model):
    '''
    This model represents the project's developers
    '''
    name = models.CharField(max_length=50)
    header = models.CharField(max_length=100)
    bio = models.TextField(max_length=1000)    
    image = models.ImageField(upload_to='core/static/img', blank=True)
    fav_album = models.CharField(max_length=75)
    fav_coffee = models.CharField(max_length=50)
    fav_president = models.CharField(max_length=50)
