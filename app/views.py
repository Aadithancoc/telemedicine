# app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SymptomForm, AppointmentForm
from .utils import get_daily_quote, get_advice, send_sms
from .tasks import send_appointment_reminder, schedule_follow_up_reminder
from django.core.exceptions import ValidationError

def index(request):
    """Home page with daily quote."""
    quote = get_daily_quote()
    return render(request, 'index.html', {'quote': quote})

def symptom_checker(request):
    """Simple symptom checker that provides advice based on user input."""
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            symptoms_list = [s.strip().lower() for s in symptoms.split(',')]
            advice = get_advice(symptoms_list)
            return render(request, 'symptom_checker.html', {'form': form, 'advice': advice})
    else:
        form = SymptomForm()
    return render(request, 'symptom_checker.html', {'form': form})

def appointment_scheduler(request):
    """
    Handles appointment scheduling:
    - Saves appointment to database
    - Sends immediate SMS confirmation
    - Schedules follow-up reminder via Celery
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Save appointment
                appointment = form.save()

                # Send immediate SMS confirmation
                try:
                    send_sms(
                        appointment.patient_phone,
                        f"Hello {appointment.patient_name}, your appointment is scheduled on {appointment.date} at {appointment.time}."
                    )
                except Exception as e:
                    messages.warning(request, f"SMS could not be sent: {str(e)}")

                # Schedule follow-up SMS in 2 days (using Celery)
                try:
                    schedule_follow_up_reminder.delay(appointment.id, days_after=2) # type: ignore
                except Exception as e:
                    messages.warning(request, f"Follow-up scheduling failed: {str(e)}")

                messages.success(request, "Appointment scheduled successfully!")
                return redirect('success')

            except Exception as e:
                messages.error(request, f"Error scheduling appointment: {str(e)}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AppointmentForm()

    return render(request, 'appointment_scheduler.html', {'form': form})

def success(request):
    """Simple success page after appointment submission."""
    return render(request, 'success.html')

