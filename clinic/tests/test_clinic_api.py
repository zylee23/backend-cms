"""Tests for the Clinic API."""

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer
from users.models import User

CLINIC_URL = reverse("clinic:clinic-list")


def detail_url(clinic_id):
    """Create and return a clinic detail url."""
    return reverse("clinic:clinic-detail", args=[clinic_id])


def create_user(email="testuser@example.com", password="testpass123", role=User.Role.ADMIN, is_staff=True):
    """Create and return a user. Returns AdminUser by default."""
    return User.objects.create_user(email=email, password=password, role=role, is_staff=is_staff)


class PublicClinicAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_get_request(self):
        """Test unauthenticated request for retriving Clinics."""
        Clinic.objects.create(clinic_name="Test Clinic 1",
                              clinic_address="Gau")
        res = self.client.get(CLINIC_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        clinics = Clinic.objects.all().order_by("-clinic_id")
        serializer = ClinicSerializer(clinics, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_unauthenticated_post_request_unsuccessful(self):
        """Test auth required for creating new clinic."""
        payload = {
            "clinic_name": "Test Clinic",
            "clinic_address": "Kuala Lumpur"
        }
        res = self.client.post(CLINIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClinicAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_clinics_successful(self):
        """Test retrieving list of clinics successful for any authenticated user."""
        Clinic.objects.create(clinic_name="Test Clinic 1",
                              clinic_address="Gau")
        Clinic.objects.create(clinic_name="Test Clinic 2",
                              clinic_address="Sahar")
        res = self.client.get(CLINIC_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        clinics = Clinic.objects.all().order_by("-clinic_id")
        serializer = ClinicSerializer(clinics, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_clinic_detail(self):
        """Test retrieving a Clinic's details."""
        clinic = Clinic.objects.create(
            clinic_name="Test Clinic", clinic_address="Gau")
        url = detail_url(clinic.clinic_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ClinicSerializer(clinic)
        self.assertEqual(res.data, serializer.data)

    def test_creating_clinics_for_admin_successful(self):
        payload = {
            "clinic_name": "Test Clinic",
            "clinic_address": "Kuala Lumpur"
        }
        res = self.client.post(CLINIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        clinic = Clinic.objects.get(clinic_id=res.data["clinic_id"])
        for k, v in payload.items():
            self.assertEqual(getattr(clinic, k), v)

    def test_create_clinics_for_not_admin_unsuccessful(self):
        """Test creating clinic for doctor or patient is unauthorized."""
        patient_user = create_user(
            email="testpatient@example.com", role=User.Role.PATIENT, is_staff=False)
        stub_client = APIClient()
        stub_client.force_authenticate(patient_user)
        payload = {
            "clinic_name": "Test Clinic",
            "clinic_address": "Kuala Lumpur"
        }
        res = stub_client.post(CLINIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        saved = Clinic.objects.filter(clinic_name=payload["clinic_name"],
                                      clinic_address=payload["clinic_address"]).exists()
        self.assertFalse(saved)

    def test_delete_clinic_admin_successful(self):
        """Test deleting a clinic as an admin."""
        clinic = Clinic.objects.create(
            clinic_name="Test Clinic", clinic_address="Gau")
        url = detail_url(clinic.clinic_id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Clinic.objects.filter(
            clinic_id=clinic.clinic_id).exists())

    def test_update_clinic_admin_successful(self):
        """Test editing existing clinic as an admin."""
        clinic = Clinic.objects.create(
            clinic_name="Test Clinic", clinic_address="Gau")
        payload = {"clinic_name": "New Clinic"}
        url = detail_url(clinic.clinic_id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        clinic.refresh_from_db()
        self.assertEqual(clinic.clinic_name, payload["clinic_name"])
