# voter_analytics/urls.py
# auther: Chonghao Chen (alvenie@bu.edu), 10/31/2025
# description: The urls.py file specific to the voter analytics app

from django.urls import path
from . import views

app_name = 'voter_analytics'
urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
]