from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Candidate(models.Model):
    '''This model represents a candidate'''
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, blank=False)
    party = models.CharField(max_length=32)
    description = models.TextField(max_length=1000, null=True, blank=True)
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
        return self.name

class Tweet(models.Model):
    '''
    This model represents the specific info from our DB.
    '''
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    text = models.CharField(max_length=400, null=True)
    followers = models.PositiveIntegerField(null=True)
    id_str = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    polarity = models.DecimalField(max_digits=10, decimal_places=9)
    subjectivity = models.DecimalField(max_digits=10, decimal_places=9)
    location = models.CharField(max_length=50)

class CandidatePolarityAverage(models.Model):
    '''
    This model represents the polarity average for candidates at a certain time.
    '''
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    positivePolarityAverage = models.DecimalField(max_digits=10, decimal_places=9)
    negativePolarityAverage = models.DecimalField(max_digits=10, decimal_places=9)
    created_at = models.DateTimeField(auto_now_add=True)
