from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from .utils import send_sms, get_daily_quote, get_advice

def index(request):
    quote = get_daily_quote()
    return render(request, 'index.html', {'quote': quote})

def symptom_checker(request):
    advice = None
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        advice = get_advice(symptoms)
    return render(request, 'symptom_checker.html', {'advice': advice})

def appointment_scheduler(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            confirmation_msg = f"Appointment confirmed for {appointment.name} on {appointment.date} at {appointment.time}."
            send_sms(appointment.phone, confirmation_msg)
            return redirect('success')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_scheduler.html', {'form': form})

def success(request):
    return render(request, 'success.html')