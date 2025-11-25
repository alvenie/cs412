# project/admin.py
from django.contrib import admin
from .models import Doctor, Patient, AppointmentSlot, AppointmentBooking

# Register your models here.
@admin.register(AppointmentSlot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'is_booked')
    list_filter = ('doctor', 'date', 'is_booked')

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(AppointmentBooking)