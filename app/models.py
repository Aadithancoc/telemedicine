from django.db import models

# Model to store Telemedicine Quotes (English + Tamil)
class Quote(models.Model):
    english = models.TextField()
    tamil = models.TextField()

    def __str__(self):
        return self.english[:50]  # Display first 50 characters in admin list

# Model to store patient Appointments
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    symptoms = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for updates

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
