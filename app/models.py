# app/models.py
from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    symptoms = models.TextField()
    doctor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"


