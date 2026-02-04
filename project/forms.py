# project/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AppointmentBooking, Patient

class BookingForm(forms.ModelForm):
    class Meta:
        model = AppointmentBooking
        fields = ['reason_for_visit']
        widgets = {
            'reason_for_visit': forms.Textarea(attrs={'rows': 3}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth']

    def save(self, commit=True):
        # 1. Create the User object
        user = super().save(commit=False)
        
        # 2. Fill in User fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            # 3. Save User to DB 
            user.save()
            
            # 4. CREATE the Patient Profile with all required data
            Patient.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )

        return user