"""Tests forthe Encounter Model."""

from django.test import TestCase
from appointment.models import Appointment
from clinic.models import Clinic
from encounter.models import Encounter
from users.models import Doctor, DoctorUser, Patient, PatientUser
from datetime import datetime


class EncounterModelTests(TestCase):
    """Test models from the encounter module."""

    def test_create_encounter_no_appointment_successful(self):
        """Test creating an encounter without appointment is successful."""
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
        clinic = Clinic.objects.create(clinic_name="Test Clinic")
        enc = Encounter.objects.create(
            encounter_date=currentDate,
            encounter_time=currentTime,
            encounter_comments="Test Comments",
            encounter_patient=patientIns,
            encounter_doctor=doctorIns,
            encounter_clinic=clinic,
            encounter_created_by=patientUser
        )
        self.assertEqual(str(enc), f"Encounter {str(enc.encounter_id)}")

    def test_create_encounter_with_appointment_successful(self):
        """Test creating an encounter with appointment is successful."""
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
        clinic = Clinic.objects.create(clinic_name="Test Clinic")
        ap = Appointment.objects.create(
            appointment_date=currentDate,
            appointment_time=currentTime,
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patientIns,
            appointment_doctor=doctorIns,
            appointment_clinic=clinic,
            created_by=patientUser
        )
        enc = Encounter.objects.create(
            encounter_date=currentDate,
            encounter_time=currentTime,
            encounter_appointment=ap,
            encounter_patient=patientIns,
            encounter_doctor=doctorIns,
            encounter_clinic=clinic,
            encounter_created_by=patientUser
        )
        self.assertEqual(str(enc), f"Encounter {str(enc.encounter_id)}")
        self.assertEqual(enc.encounter_appointment, ap)
