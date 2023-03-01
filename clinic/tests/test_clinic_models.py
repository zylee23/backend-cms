"""Tests for Clinic Models."""

from django.test import TestCase
from clinic.models import Clinic


class ClinicModelTests(TestCase):
    """Test the clinic model."""

    def test_create_clinic(self):
        """Test creating a new clinic."""
        clinic = Clinic.objects.create(clinic_name="My Clinic",
                                       clinic_address="PAlto", clinic_contact="60312312300")
        self.assertEqual(str(clinic), clinic.clinic_name)
