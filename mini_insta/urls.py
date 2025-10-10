# mini_insta/urls.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The urls.py file specific to the mini insta app
# define URL patterns for the blog application

from django.urls import path
from .views import * # ProfileListView, ProfileDetailView, PostDetailView, UpdateProfileView, DeletePostView, UpdatePostView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post_form'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
]