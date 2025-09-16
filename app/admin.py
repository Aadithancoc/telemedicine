from django.contrib import admin
from .models import Appointment

# Register Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_phone', 'symptoms', 'date', 'time')
    search_fields = ('patient_name', 'patient_phone', 'symptoms')
    list_filter = ('date',)
