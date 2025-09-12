# file: quotes/urls.py
# auther: Alven Chen (alvenie@bu.edu), 9/8/2025
# description: The urls.py file specific to the quotes app

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the quotes app:

urlpatterns = [
    path(r'', views.home_page, name="home_page"),
    path(r'quote', views.quote, name="quote_page"),
    path(r'show_all', views.show_all, name="show_page"),
    path(r'about', views.about, name="about_page"),
]