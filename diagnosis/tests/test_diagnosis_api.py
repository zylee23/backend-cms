"""Tests for the diagnosis API."""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from diagnosis.models import Diagnosis
from django.urls import reverse
from users.models import User, PatientUser, DoctorUser, Patient, Doctor
from datetime import datetime
from encounter.models import Encounter
from diagnosis.serializers import DiagnosisSerializer

DIAGNOSIS_URL = reverse("diagnosis:diagnosis-list")


def detail_url(diagnosis_id):
    """Create and return a detail url."""
    return reverse("diagnosis:diagnosis-detail", args=[diagnosis_id])


def create_user(email="testuser@example.com", password="testpass123", role=User.Role.ADMIN, is_staff=True):
    """Create and return a user. Returns AdminUser by default."""
    return User.objects.create_user(email=email, password=password, role=role, is_staff=is_staff)


def create_encounter():
    """Create and return a new encounter."""
    patientUser = PatientUser.objects.create_user(
        email="patient@example.com",
        password="testpass123"
    )
    patientIns = Patient.objects.create(
        patient_name="Test Patient",
        patient_dob="2000-01-01",
        patient_address="Kuala Lumpur, Malaysia",
        patient_contact="+6012345678",
        user=patientUser,
    )
    doctorUser = DoctorUser.objects.create_user(
        email="doctor@example.com",
        password="testpass123"
    )
    doctorIns = Doctor.objects.create(
        doctor_name="Test Doctor",
        doctor_dob="2000-01-01",
        doctor_address="Kathmandu, Nepal",
        user=doctorUser
    )
    currentDate = datetime.now().date()
    currentTime = datetime.now().time()
    enc = Encounter.objects.create(
        encounter_date=currentDate,
        encounter_time=currentTime,
        encounter_patient=patientIns,
        encounter_doctor=doctorIns,
        encounter_created_by=doctorUser
    )
    return enc


class PublicDiagnosisAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test Auth required for retriving Diagnosis."""
        res = self.client.get(DIAGNOSIS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDiagnosisAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user(
            email="doctor1@example.com", is_staff=False, role=User.Role.DOCTOR)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_diagnosis_successful(self):
        """Test retrieve a diagnosis listing is successful."""
        enc = create_encounter()
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Influenza",
            diagnosis_icd="J09",
            diagnosis_encounter=enc
        )
        res = self.client.get(DIAGNOSIS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        sz = DiagnosisSerializer(diagnosis)
        self.assertEqual([sz.data], res.data)

    def test_retrieve_diagnosis_detail_successful(self):
        """Test retrieve a single diagnosis detail"""
        enc = create_encounter()
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Influenza",
            diagnosis_icd="J09",
            diagnosis_encounter=enc
        )
        url = detail_url(diagnosis.diagnosis_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        sz = DiagnosisSerializer(diagnosis)
        self.assertEqual(sz.data, res.data)

    def test_retrieve_diagnosis_by_queryparam_successful(self):
        """Test retrieve a single diagnosis via query param"""
        enc = create_encounter()
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Influenza",
            diagnosis_icd="J09",
            diagnosis_encounter=enc
        )
        params = {"encounter_id": f"{enc.encounter_id}"}
        res = self.client.get(DIAGNOSIS_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        sz = DiagnosisSerializer(diagnosis)
        self.assertEqual(res.data, [sz.data])

    def test_create_diagnosis_doctor_successful(self):
        """Test creating a diagnosis as a Doctor is successful."""
        enc = create_encounter()
        payload = {
            "diagnosis_descr": "Tuberculosis",
            "diagnosis_icd": "A16.0",
            "diagnosis_encounter": str(enc.encounter_id)
        }
        res = self.client.post(DIAGNOSIS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Diagnosis.objects.filter(
            diagnosis_encounter_id=enc.encounter_id).exists())

    def test_create_diagnosis_patient_unsuccessful(self):
        """Test creating a diagnosis as a Patient is unsuccessful."""
        enc = create_encounter()
        payload = {
            "diagnosis_descr": "Tuberculosis",
            "diagnosis_icd": "A16.0",
            "diagnosis_encounter": str(enc.encounter_id)
        }
        p_user = create_user(email="testpatient@example.com",
                             role=User.Role.PATIENT, is_staff=False)
        new_client = APIClient()
        new_client.force_authenticate(p_user)
        res = new_client.post(DIAGNOSIS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Diagnosis.objects.filter(
            diagnosis_encounter_id=enc.encounter_id).exists())

    def test_deleting_diagnosis_successful(self):
        """Test deleting a diagnosis by id is successful by doctor."""
        enc = create_encounter()
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Influenza",
            diagnosis_icd="J09",
            diagnosis_encounter=enc
        )
        url = detail_url(diagnosis.diagnosis_id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Diagnosis.objects.filter(
            diagnosis_id=diagnosis.diagnosis_id).exists())

    def test_updating_diagnosis_successful(self):
        """"Test updating a single diagnosis."""
        enc = create_encounter()
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Influenza",
            diagnosis_icd="J09",
            diagnosis_encounter=enc
        )
        payload = {
            "diagnosis_prescription": "Paracetemol",
            "diagnosis_icd": "J09.09",
            "diagnosis_heart_rate": "80"
        }
        url = detail_url(diagnosis.diagnosis_id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        diagnosis.refresh_from_db()
        sz = DiagnosisSerializer(diagnosis)
        self.assertIn("diagnosis_prescription", sz.data)
