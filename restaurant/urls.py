# restaurant/urls.py
# url patterns for the 'restaurant' app.

from django.urls import path
from django.conf import settings
from . import views

# URL patterns for this app:
urlpatterns = [
    path(r'', views.main, name='main_page'),
    path(r'order', views.order, name='order_page'),
    path(r'submit', views.submit, name='confirmation_page') ## NEW
]