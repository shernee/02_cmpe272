from django.urls import path

from app_tweets import views

app_name = 'app_tweets'

urlpatterns = [
    path('', views.home, name='home'),
    path('posted/', views.posted, name='posted'),
    path('deleted/', views.deleted, name='deleted'),
    path('retrieved/<int:tweet_id>/', views.retrieved, name='retrieved'),
]