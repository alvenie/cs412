# dadjokes/urls.py
# auther: Chonghao Chen (alvenie@bu.edu), 11/13/2025
# description: The urls.py file specific to the dadjokes app

from django.urls import path
from . import views

urlpatterns = [
    # Regular URLs
    path('', views.RandomJokeAndPictureView.as_view(), name='home'),
    path('random/', views.RandomJokeAndPictureView.as_view(), name='random'),
    path('jokes/', views.AllJokesView.as_view(), name='all_jokes'),
    path('joke/<int:pk>/', views.JokeDetailView.as_view(), name='joke_detail'),
    path('pictures/', views.AllPicturesView.as_view(), name='all_pictures'),
    path('picture/<int:pk>/', views.PictureDetailView.as_view(), name='picture_detail'),
    
    # API URLs
    path('api/', views.ApiRandomJoke.as_view(), name='api_random_joke'),
    path('api/random/', views.ApiRandomJoke.as_view(), name='api_random_joke_alias'),
    path('api/jokes/', views.ApiJokeList.as_view(), name='api_all_jokes'), # Handles GET (list) and POST (create)
    path('api/joke/<int:pk>/', views.ApiJokeDetail.as_view(), name='api_joke_detail'),
    path('api/pictures/', views.ApiPictureList.as_view(), name='api_all_pictures'),
    path('api/picture/<int:pk>/', views.ApiPictureDetail.as_view(), name='api_picture_detail'),
    path('api/random_picture/', views.ApiRandomPicture.as_view(), name='api_random_picture'),
]