"""Tests for the Appointment Models."""

from django.test import TestCase
from appointment.models import Appointment
from users.models import Doctor, DoctorUser, Patient, PatientUser
from clinic.models import Clinic
from datetime import datetime


class AppointmentModelTests(TestCase):
    """Test models from the Appointment Module."""

    def test_create_appointment_successful(self):
        """Test creating an appointment is successful."""
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
        clinic = Clinic.objects.create(
            clinic_name="Test Clinic"
        )
        currentDate = datetime.now().date()
        currentTime = datetime.now().time()
        ap = Appointment.objects.create(
            appointment_date=currentDate,
            appointment_time=currentTime,
            appointment_status=Appointment.Status.REQUESTED,
            appointment_comments="Test Comments",
            appointment_patient=patientIns,
            appointment_doctor=doctorIns,
            appointment_clinic=clinic,
            created_by=patientUser
        )
        self.assertEqual(str(ap), "Appointment " + str(ap.appointment_id))
