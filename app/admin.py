from django.contrib import admin
from .models import Quote, Appointment

# Register Quote model
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('english', 'tamil')      # Fields to show in admin list
    search_fields = ('english', 'tamil')     # Searchable fields
    list_filter = ()                          # Can add filters if needed

# Register Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'symptoms', 'date', 'time')
    search_fields = ('name', 'phone', 'symptoms')
    list_filter = ('date',)