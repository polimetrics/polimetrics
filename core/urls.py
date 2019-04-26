from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('candidates/', views.candidates, name='candidates'),
    path('about/', views.about, name='about'),
    path('methodology/', views.methodology, name='methodology'),
    path('<slug:slug>/', views.candidate_detail, name='candidate_detail'),
]

# model - candidate needs "candidate-detail page"
