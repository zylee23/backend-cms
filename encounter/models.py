"""Models for the Encounter Module."""

from django.db import models
from users.models import Patient, Doctor, User
from appointment.models import Appointment
from clinic.models import Clinic


class Encounter(models.Model):
    """Encounter model for storing encounter data."""

    encounter_id = models.AutoField(primary_key=True)
    encounter_date = models.DateField()
    encounter_time = models.TimeField()
    encounter_appointment = models.ForeignKey(Appointment,
                                              on_delete=models.SET_NULL,
                                              related_name="encounter_appointment",
                                              blank=True,
                                              null=True)
    encounter_comments = models.TextField(blank=True, null=True)
    encounter_patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="encounter_patient")
    encounter_doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="encounter_doctor")
    encounter_clinic = models.ForeignKey(
        Clinic, on_delete=models.SET_NULL, related_name="encounter_clinic", null=True)
    encounter_created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="encounter_created_by")

    def __str__(self):
        return f"Encounter {str(self.encounter_id)}"
