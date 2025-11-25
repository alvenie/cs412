# project/models.py
from django.db import models
from django.urls import reverse

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.last_name} ({self.specialty})"

    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'pk': self.pk})

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AppointmentSlot(models.Model):
    """
    Pre-populated time slots.
    If 'is_booked' is True, this slot cannot be selected.
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.date} @ {self.start_time} - Dr. {self.doctor.last_name}"

class AppointmentBooking(models.Model):
    """
    The actual transaction linking a patient to a slot.
    """
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason_for_visit = models.TextField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.patient} with {self.slot.doctor}"
    
    def save(self, *args, **kwargs):
        # Automate the state change: When booking is saved, mark slot as booked
        self.slot.is_booked = True
        self.slot.save()
        super().save(*args, **kwargs)