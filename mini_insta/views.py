# mini_insta/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

def ProfileListView(ListView):
    '''Define a view class to show all mini insta Profiles.'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

