# mini_insta/urls.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The urls.py file specific to the mini insta app
# define URL patterns for the blog application

from django.urls import path
from .views import ProfileListView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
]