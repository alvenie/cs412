# project/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True, help_text="Short bio about the doctor.")
    image_url = models.URLField(blank=True, help_text="Link to a profile image (optional)")

    def __str__(self):
        return f"Dr. {self.last_name} ({self.specialty})"

    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'pk': self.pk})

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
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
        status = "BOOKED" if self.is_booked else "OPEN"
        return f"{self.date} @ {self.start_time} - {self.doctor.last_name} [{status}]"

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