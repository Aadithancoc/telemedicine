# app/tasks.py
from celery import shared_task
from .utils import send_sms
from .models import Appointment
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_appointment_reminder(self, appointment_id):
    """
    Sends SMS reminder for a given appointment.
    Retries up to 3 times if sending fails.
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        phone_number = appointment.patient_phone  # field in model
        message = (
            f"Hello {appointment.patient_name}, your appointment with {appointment.doctor} "
            f"is scheduled on {appointment.date} at {appointment.time}."
        )
        send_sms(phone_number, message)
        logger.info(f"Reminder sent for appointment {appointment_id}")
        return f"Reminder sent for appointment {appointment_id}"
    except Appointment.DoesNotExist:
        logger.warning(f"Appointment {appointment_id} does not exist")
        return f"Appointment {appointment_id} does not exist"
    except Exception as exc:
        logger.error(f"Error sending reminder for appointment {appointment_id}: {exc}")
        # Retry if something goes wrong
        raise self.retry(exc=exc)

@shared_task
def schedule_follow_up_reminder(appointment_id, days_after=7):
    """
    Schedule a follow-up reminder for a patient after a certain number of days.
    Uses Celery's ETA to delay the task until the scheduled time.
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        follow_up_time = timezone.datetime.combine(
            appointment.date + timedelta(days=days_after),
            appointment.time
        )
        follow_up_time = timezone.make_aware(follow_up_time, timezone.get_current_timezone())

        # Schedule the reminder
        send_appointment_reminder.apply_async(
            args=[appointment_id],
            eta=follow_up_time
        ) # type: ignore

        logger.info(f"Follow-up reminder scheduled for appointment {appointment_id} at {follow_up_time}")
        return f"Follow-up reminder scheduled for appointment {appointment_id} at {follow_up_time}"
    except Appointment.DoesNotExist:
        logger.warning(f"Appointment {appointment_id} does not exist")
        return f"Appointment {appointment_id} does not exist"
    except Exception as e:
        logger.error(f"Error scheduling follow-up for appointment {appointment_id}: {e}")
        return f"Error scheduling follow-up for appointment {appointment_id}: {str(e)}"
