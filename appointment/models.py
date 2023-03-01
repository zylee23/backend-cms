"""Models for the Appointment Module."""

from django.db import models
from users.models import Patient, Doctor, User
from clinic.models import Clinic


class Appointment(models.Model):
    """Appointment Model for storing appointment data."""

    class Status(models.TextChoices):
        """Different types of appointment status."""
        REQUESTED = "REQUESTED", "Requested"
        BOOKED = "BOOKED", "Booked"
        CANCELLED = "CANCELLED", "Cancelled"
        RESCHEDULED = "RESCHEDULED", "Rescheduled"
        ATTENDED = "ATTENDED", "Attended"

    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_status = models.CharField(
        choices=Status.choices, max_length=15)
    appointment_comments = models.TextField(blank=True, null=True)
    appointment_patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointment_patient")
    appointment_doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointment_doctor")
    appointment_clinic = models.ForeignKey(
        Clinic, on_delete=models.SET_NULL, related_name="appointment_clinic",
        null=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by")

    def __str__(self):
        return f"Appointment {str(self.appointment_id)}"
