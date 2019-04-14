from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
]

# model - candidate needs "candidate-detail page"
