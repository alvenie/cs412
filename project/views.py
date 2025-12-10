from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Doctor, AppointmentSlot, AppointmentBooking, Patient
from .forms import BookingForm, PatientForm, PatientRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class DoctorListView(ListView):
    """Displays a list of doctors with search functionality."""
    model = Doctor
    template_name = 'project/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        """Filtering logic"""
        query = self.request.GET.get('q')
        if query:
            return Doctor.objects.filter(
                Q(last_name__icontains=query) | 
                Q(specialty__icontains=query)
            )
        return Doctor.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the search term to the template explicitly
        context['last_search'] = self.request.GET.get('q', '')
        return context

class DoctorDetailView(DetailView):
    """Displays doctor details and their AVAILABLE slots."""
    model = Doctor
    template_name = 'project/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter: Only show slots that are NOT booked and order them by date
        context['available_slots'] = AppointmentSlot.objects.filter(
            doctor=self.object, 
            is_booked=False
        ).order_by('date', 'start_time')
        return context

class PatientCreateView(CreateView):
    """Allows creating a new patient profile."""
    model = Patient
    form_class = PatientForm
    template_name = 'project/patient_form.html'
    success_url = reverse_lazy('doctor_list')

class BookingCreateView(LoginRequiredMixin, CreateView):
    """Allows creating a booking"""
    model = AppointmentBooking
    form_class = BookingForm
    template_name = 'project/booking_form.html'
    success_url = reverse_lazy('profile')

    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.slot = get_object_or_404(AppointmentSlot, pk=self.kwargs['slot_id'])
        # Check if the slot is booked
        if self.slot.is_booked:
            return redirect('doctor_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slot'] = self.slot 
        return context

    def form_valid(self, form):
        form.instance.slot = self.slot
        
        # automatically assign the patient based on the logged-in user
        form.instance.patient = self.request.user.patient 
        
        self.slot.is_booked = True
        self.slot.save()
        return super().form_valid(form)
    
def register(request):
    if request.method == "POST":
        # Use the custom form here
        form = PatientRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save() # This calls the custom save method we wrote above
            login(request, user)
            return redirect('profile') # Or 'doctor_list'
    else:
        form = PatientRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, ListView):
    """Displays the current patients profile"""
    model = AppointmentBooking
    template_name = 'project/profile.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # 1. Get the currently logged-in user's patient profile
        if hasattr(self.request.user, 'patient'):
            patient_profile = self.request.user.patient
            # 2. Return only bookings for this specific patient
            return AppointmentBooking.objects.filter(patient=patient_profile).order_by('slot__date')
        else:
            return AppointmentBooking.objects.none()
        
class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """Displays a form that allows the patient to update their profile"""
    model = Patient
    fields = ['phone', 'date_of_birth']
    template_name = 'project/patient_form.html'
    success_url = reverse_lazy('profile') # Go back to profile after saving

    def get_object(self):
        # Limit editing to the logged-in user's own profile
        return self.request.user.patient