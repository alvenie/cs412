# project/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('book/<int:slot_id>/', views.BookingCreateView.as_view(), name='book_appointment'),
]