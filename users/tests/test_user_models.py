"""Test for User models."""

from django.test import TestCase
from clinic.models import Clinic
from users.models import (
    User, PatientUser, DoctorUser, AdminUser,
    Patient, Doctor, Admin)


class UserModelTests(TestCase):
    "Test user models."

    def test_create_patient_with_email_successful(self):
        """Test creating a patient with email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = PatientUser.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, User.Role.PATIENT)

    def test_create_doctors_with_email_successful(self):
        """Test creating a doctor with email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = DoctorUser.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, User.Role.DOCTOR)

    def test_create_admin_with_email_successful(self):
        """Test creating a admin with email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = AdminUser.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertTrue(user.is_staff)

    def test_create_superuser_with_email_successful(self):
        """Test creating a superuser with email is successful."""
        email = "super@example.com"
        password = "testpass123"
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertTrue(user.is_superuser)

    def test_new_patient_email_normalized(self):
        """Test email is normalized for new patients."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"]
        ]
        for email, expected in sample_emails:
            user = PatientUser.objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
            self.assertEqual(user.role, User.Role.PATIENT)

    def test_new_doctor_email_normalized(self):
        """Test email is normalized for new doctors."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"]
        ]
        for email, expected in sample_emails:
            user = DoctorUser.objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
            self.assertEqual(user.role, User.Role.DOCTOR)

    def test_new_patient_without_email_raises_error(self):
        """Test that creating a patient without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            PatientUser.objects.create_user('', 'test123')

    def test_new_doctor_without_email_raises_error(self):
        """Test that creating a doctor without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            PatientUser.objects.create_user('', 'test123')

    def test_creating_patient_profile_for_registered_patient_successfully(self):
        """Test that Patient table can be populated once patient user is created."""
        email = "test@example.com"
        password = "testpass123"
        user1 = PatientUser.objects.create_user(
            email=email,
            password=password
        )
        clinic = Clinic.objects.create(clinic_name="Test Clinic")
        patient = Patient.objects.create(
            patient_name="Test User",
            patient_dob="2000-01-01",
            patient_address="Kuala Lumpur, Malaysia",
            patient_contact="+6012345678",
            patient_clinic=clinic,
            user=user1,
        )
        self.assertEqual(user1, patient.user)
        self.assertEqual(str(patient), "Patient " + patient.patient_name)

    def test_creating_doctor_profile_for_registered_doctor_successfully(self):
        """Test that Doctor table can be populated once doctor user is created."""
        email = "test@example.com"
        password = "testpass123"
        user1 = DoctorUser.objects.create_user(
            email=email,
            password=password
        )
        clinic = Clinic.objects.create(clinic_name="Test Clinic")
        doctor = Doctor.objects.create(
            doctor_name="Test User",
            doctor_dob="2000-01-01",
            doctor_address="Kuala Lumpur, Malaysia",
            doctor_contact="+6012345678",
            doctor_clinic=clinic,
            user=user1,
        )
        self.assertEqual(user1, doctor.user)
        self.assertEqual(str(doctor), "Doctor " + doctor.doctor_name)

    def test_creating_admin_profile_for_registered_admin_successfully(self):
        """Test that Admin table can be populated once Admin user is created."""
        email = "test@example.com"
        password = "testpass123"
        user1 = AdminUser.objects.create_user(
            email=email,
            password=password
        )
        clinic = Clinic.objects.create(clinic_name="Test Clinic")
        admin = Admin.objects.create(
            admin_name="Test User",
            admin_dob="2000-01-01",
            admin_address="Kuala Lumpur, Malaysia",
            admin_contact="+6012345678",
            admin_clinic=clinic,
            user=user1,
        )
        self.assertEqual(user1, admin.user)
        self.assertEqual(str(admin), "Admin " + admin.admin_name)
