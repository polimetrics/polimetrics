from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.candidates, name='candidates'),
    path('', views.tags, name='tags'),
    path('', views.about, name='about')
]

# model - candidate needs "candidate-detail page"
