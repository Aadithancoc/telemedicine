from django import forms
from .models import Appointment

class SymptomForm(forms.Form):
    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'e.g., fever, cough'}),
        required=True,
        label='Enter your symptoms'
    )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_email', 'patient_phone', 'symptoms', 'doctor', 'date', 'time']
        widgets = {
            'symptoms': forms.Textarea(attrs={'placeholder': 'e.g., fever, cough'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
