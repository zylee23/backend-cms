"""Test for appointment API."""

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from appointment.models import Appointment
from clinic.models import Clinic
from appointment.serializers import AppointmentSerializer, AppointmentSerializerExtended
from users.models import User, Patient, Doctor
from datetime import datetime

APPOINTMENT_URL = reverse("appointment:appointment-list")


def detail_url(appointment_id):
    """Create and return an detail url."""
    return reverse("appointment:appointment-detail", args=[appointment_id])


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


class PublicAppointmentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test Auth required for retriving Appointments."""
        res = self.client.get(APPOINTMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAppointmentAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.clinic = Clinic.objects.create(clinic_name="Test Clinic")

    def test_retrieve_appointment_successful(self):
        """Test retrieving list of appointments for ADMIN users successfully."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        Appointment.objects.create(
            appointment_date=datetime.strptime("2022-02-02", "%Y-%m-%d"),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.BOOKED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        res = self.client.get(APPOINTMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        appointments = Appointment.objects.all().order_by(
            "-appointment_date", "-appointment_time")
        serializer = AppointmentSerializerExtended(appointments, many=True)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_appointment_detail(self):
        """Test retrieving appointment detail for ADMIN user."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        ap = Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        url = detail_url(ap.appointment_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = AppointmentSerializerExtended(ap)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_appointment_for_patient_user(self):
        """Test Retrieving appointments only for patient user."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        ap = Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        patient_user2 = create_patient_user(email="patient2@example.com")
        patient2 = create_patient(patient_user2)
        Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient2,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user2
        )
        patient_client = APIClient()
        patient_client.force_authenticate(patient_user)
        res = patient_client.get(APPOINTMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        serializer = AppointmentSerializerExtended(ap)
        self.assertEqual(res.data, [serializer.data])

    def test_creating_appointment(self):
        """Test creating appointment as a patient."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        p_client = APIClient()
        p_client.force_authenticate(patient_user)
        payload = {
            "appointment_date": "2022-09-09",
            "appointment_time": "10:10:00",
            "appointment_status": Appointment.Status.REQUESTED,
            "appointment_comments": "Test Comments",
            "appointment_patient": patient.patient_id,
            "appointment_doctor": doctor.doctor_id,
            "appointment_clinic": self.clinic.clinic_id
        }
        res = p_client.post(APPOINTMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ap = Appointment.objects.get(created_by=patient_user)
        serializer = AppointmentSerializerExtended(ap)
        self.assertEqual(res.data, serializer.data)

    def test_updating_appointment(self):
        """Test updating appointment as doctor."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        ap = Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        payload = {
            "appointment_status": Appointment.Status.CANCELLED
        }
        d_client = APIClient()
        d_client.force_authenticate(doctor_user)
        url = detail_url(ap.appointment_id)
        res = d_client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ap.refresh_from_db()
        self.assertEqual(ap.appointment_status, Appointment.Status.CANCELLED)

    def test_delete_appointment(self):
        """Test deleting an appointment as admin."""
        patient_user = create_patient_user()
        patient = create_patient(patient_user)
        doctor_user = create_doctor_user()
        doctor = create_doctor(doctor_user)
        ap = Appointment.objects.create(
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            appointment_status=Appointment.Status.REQUESTED,
            appointment_patient=patient,
            appointment_doctor=doctor,
            appointment_clinic=self.clinic,
            created_by=patient_user
        )
        url = detail_url(ap.appointment_id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Appointment.objects.filter(
            appointment_id=ap.appointment_id).exists()
        self.assertFalse(exists)
