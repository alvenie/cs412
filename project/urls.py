# project/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('patient/new/', views.PatientCreateView.as_view(), name='create_patient'),
    path('book/<int:slot_id>/', views.BookingCreateView.as_view(), name='book_appointment'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.PatientUpdateView.as_view(), name='edit_profile'),
]