from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    # path('<slug:slug>/', views.candidate, name='candidate'),
    path('', views.tags, name='tags'),
    path('about/', views.about, name='about')
]

# model - candidate needs "candidate-detail page"
