# mini_insta/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The views.py file specific to the mini insta app

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile, Post

# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to show all mini insta Profiles.'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Define a view class to show a specific Profile'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Define a view class to show a specific Post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'