from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Candidate(models.Model):
    '''This model represents a candidate'''
    name = models.CharField(max_length=32)
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
        return self.name

class Tweet(models.Model):
    '''
    This model represents the specific info from our DB.
    '''
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE,)
    id_str = models.CharField(max_length=100)
    created_at = models.CharField(max_length=50)
    polarity = models.DecimalField(max_digits=10, decimal_places=9)
    subjectivity = models.DecimalField(max_digits=10, decimal_places=9)
    location = models.CharField(max_length=50)
