# project/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Doctor, AppointmentSlot, AppointmentBooking

# Create your views here.
class DoctorListView(ListView):
    model = Doctor
    template_name = 'project/doctor_list.html'
    context_object_name = 'doctors'

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'project/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter to only show slots that are NOT booked
        context['available_slots'] = AppointmentSlot.objects.filter(
            doctor=self.object, 
            is_booked=False
        )
        return context

class BookingCreateView(CreateView):
    model = AppointmentBooking
    template_name = 'project/book_appointment.html'
    fields = ['patient', 'reason_for_visit'] 
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        # Manually attach the specific slot from the URL
        slot_id = self.kwargs['slot_id']
        slot = AppointmentSlot.objects.get(pk=slot_id)
        form.instance.slot = slot
        return super().form_valid(form)