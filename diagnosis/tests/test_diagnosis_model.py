"""Tests for Diagnosis Models."""

from django.test import TestCase
from diagnosis.models import Diagnosis
from users.models import PatientUser, Patient, DoctorUser, Doctor
from encounter.models import Encounter
from datetime import datetime


class DiagnosisModelTests(TestCase):
    """Test the Diagnosis model."""

    def test_create_diagnosis(self):
        """Test creating a new diagnosis."""
        # first create an encounter
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
            encounter_created_by=patientUser
        )
        diagnosis = Diagnosis.objects.create(
            diagnosis_descr="Lung Cancer",
            diagnosis_oxy_saturation="95",
            diagnosis_symptoms="High Fever",
            diagnosis_icd="J11.81: Influenza due to unidentified influenza virus with encephalopathy",
            diagnosis_encounter=enc)
        self.assertEqual(
            str(diagnosis), f"Diagnosis {str(diagnosis.diagnosis_id)}")
        self.assertEqual(diagnosis.diagnosis_encounter, enc)
