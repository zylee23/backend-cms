"""Models for Clinic Module."""

from django.db import models
from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(regex=r'^\+?\d{9,16}$')


class Clinic(models.Model):
    """Clinic Model."""
    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=255)
    clinic_address = models.TextField(blank=True, null=True)
    clinic_contact = models.CharField(
        validators=[PHONE_REGEX], max_length=17, blank=True, null=True)

    def __str__(self) -> str:
        return self.clinic_name
