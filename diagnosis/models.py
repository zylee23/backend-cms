from django.db import models
from encounter.models import Encounter


class Diagnosis(models.Model):
    """Model for Diagnosis."""
    diagnosis_id = models.AutoField(primary_key=True)
    diagnosis_weight = models.CharField(blank=True, null=True, max_length=3)
    diagnosis_height = models.CharField(blank=True, null=True, max_length=3)
    diagnosis_symptoms = models.TextField(blank=True, null=True)
    diagnosis_history = models.TextField(blank=True, null=True)
    diagnosis_blood_pressure = models.CharField(
        blank=True, null=True, max_length=7)
    diagnosis_heart_rate = models.CharField(
        blank=True, null=True, max_length=3)
    diagnosis_resp_rate = models.CharField(blank=True, null=True, max_length=3)
    diagnosis_oxy_saturation = models.CharField(
        blank=True, null=True, max_length=3)
    diagnosis_temp = models.CharField(blank=True, null=True, max_length=3)
    diagnosis_descr = models.TextField(blank=True, null=True)
    diagnosis_icd = models.TextField(blank=True, null=True)
    diagnosis_prescription = models.TextField(blank=True, null=True)
    diagnosis_encounter = models.OneToOneField(
        Encounter, on_delete=models.CASCADE, related_name="diagnosis_encounter")

    def __str__(self):
        return f"Diagnosis {str(self.diagnosis_id)}"
