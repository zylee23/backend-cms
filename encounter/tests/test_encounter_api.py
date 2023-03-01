"""Tests for the Encounter API."""

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from clinic.models import Clinic
from encounter.models import Encounter
from encounter.serializers import (
    EncounterSerializer,
    EncounterSerializerExtended
)
from appointment.models import Appointment
from users.models import User, Patient, Doctor
from datetime import datetime
from pprint import pprint

ENCOUNTER_URL = reverse("encounter:encounter-list")


def detail_url(encounter_id):
    """Create and return an detail url."""
    return reverse("encounter:encounter-detail", args=[encounter_id])


def create_user(email="testuser@example.com", password="testpass123", role=User.Role.ADMIN, is_staff=True):
    """Create and return a user. Returns AdminUser by default."""
    return User.objects.create_user(email=email, password=password, role=role, is_staff=is_staff)


def create_patient_user(email="patient@example.com", role=User.Role.PATIENT, is_staff=False):
    """Create and return a patient user."""
    return create_user(email=email, role=role, is_staff=is_staff)


def create_doctor_user(email="doctor@example.com", role=User.Role.DOCTOR, is_staff=False):
    """Create and return a doctor user."""
    return create_user(email=email, role=role, is_staff=is_staff)


def create_patient(patient_user, name="Test Patient", dob="2000-03-13"):
    """Create and return a patient profile."""
    return Patient.objects.create(
        patient_name=name,
        patient_dob=dob,
        user=patient_user,
    )


def create_doctor(doctor_user, name="Test Doctor", dob="2000-02-12"):
    """Create and return a doctor profile."""
    return Doctor.objects.create(
        doctor_name=name,
        doctor_dob=dob,
        user=doctor_user,
    )


class PublicEncounterAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test Auth required for retriving Encounters."""
        res = self.client.get(ENCOUNTER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEncounterAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.clinic = Clinic.objects.create(clinic_name="Test Clinic")

    def test_retrieve_encounter_successful(self):
        """Test retrieving the list of encounters for any authenticated user successfully."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        Encounter.objects.create(
            encounter_date=datetime.now().date(),
            encounter_time=datetime.now().time(),
            encounter_patient=patient,
            encounter_doctor=doctor,
            encounter_clinic=self.clinic,
            encounter_created_by=self.user
        )
        Encounter.objects.create(
            encounter_date=datetime.strptime("2021-12-02", "%Y-%m-%d").date(),
            encounter_time=datetime.now().time(),
            encounter_patient=patient,
            encounter_doctor=doctor,
            encounter_clinic=self.clinic,
            encounter_created_by=self.user
        )
        res = self.client.get(ENCOUNTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        encounters = Encounter.objects.all().order_by(
            "-encounter_date", "-encounter_time")
        serializer = EncounterSerializerExtended(encounters, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_encounter_detail_successful(self):
        """Test retrieving an encounter detail."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        encounter = Encounter.objects.create(
            encounter_date=datetime.now().date(),
            encounter_time=datetime.now().time(),
            encounter_patient=patient,
            encounter_doctor=doctor,
            encounter_clinic=self.clinic,
            encounter_created_by=self.user
        )
        url = detail_url(encounter.encounter_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = EncounterSerializerExtended(encounter)
        self.assertEqual(res.data, serializer.data)

    def test_create_encounter_no_appointment_successful(self):
        """Test creating an encounter without prior appointment successful."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        payload = {
            "encounter_date": "2022-09-12",
            "encounter_time": "23:55:14",
            "encounter_patient": patient.patient_id,
            "encounter_doctor": doctor.doctor_id,
            "encounter_clinic": self.clinic.clinic_id
        }
        res = self.client.post(ENCOUNTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        enc = Encounter.objects.get(
            encounter_id=res.data["encounter_id"])
        serializer = EncounterSerializerExtended(enc)
        self.assertEqual(res.data, serializer.data)
