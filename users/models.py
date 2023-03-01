from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.validators import RegexValidator
from clinic.models import Clinic
PHONE_REGEX = RegexValidator(regex=r'^\+?\d{9,16}$')


class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        if not email:
            raise ValueError("User must have email address.")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.role = User.Role.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    "Base user Account in the system."

    class Role(models.TextChoices):
        """Different Roles a user can take. Each user must have a single role."""
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    base_role = None
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices)
    USERNAME_FIELD = "email"
    objects = UserManager()

    def save(self, *args, **kwargs):
        """Override the save method to add role."""
        if not self.pk:
            if self.base_role is not None:
                self.role = self.base_role
            return super().save(*args, *kwargs)

    def __str__(self):
        return self.email + " as " + self.role


class PatientManager(BaseUserManager):
    """Manager for Patients."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new patient."""
        if not email:
            raise ValueError("User must have email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = User.Role.PATIENT
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        """Filter Users and returns Patients."""
        res = super().get_queryset(*args, **kwargs)
        return res.filter(role=User.Role.PATIENT)


class PatientUser(User):
    """Proxy Model for Patients, based off User."""
    base_role = User.Role.PATIENT
    objects = PatientManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Patients."


class Patient(models.Model):
    """Patient Profile model for storing patient data."""
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    patient_dob = models.DateField()
    patient_address = models.TextField(blank=True, null=True)
    patient_contact = models.CharField(
        validators=[PHONE_REGEX], max_length=17, blank=True, null=True)
    patient_clinic = models.ForeignKey(
        Clinic, on_delete=models.SET_NULL, related_name="patient_clinic", null=True)
    user = models.OneToOneField(
        User, related_name="patient_info", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Patient " + self.patient_name


class DoctorManager(BaseUserManager):
    """Manager for Doctors."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new doctor."""
        if not email:
            raise ValueError("User must have email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = User.Role.DOCTOR
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        """Filter Users and returns Doctors."""
        res = super().get_queryset(*args, **kwargs)
        return res.filter(role=User.Role.DOCTOR)


class DoctorUser(User):
    """Proxy Model for Doctor, based off User."""
    base_role = User.Role.DOCTOR
    objects = DoctorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Doctors."


class Doctor(models.Model):
    """Doctor Profile model for storing doctor data."""
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=100)
    doctor_dob = models.DateField()
    doctor_address = models.TextField(blank=True, null=True)
    doctor_contact = models.CharField(
        validators=[PHONE_REGEX], max_length=17, blank=True, null=True)
    doctor_clinic = models.ForeignKey(
        Clinic, on_delete=models.SET_NULL, related_name="doctor_clinic", null=True)
    user = models.OneToOneField(
        User, related_name="doctor_info", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Doctor " + self.doctor_name


class AdminManager(BaseUserManager):
    """Manager for Admins."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new Admin."""
        if not email:
            raise ValueError("User must have email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = User.Role.ADMIN
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser. Only Admin can be a superuser."""
        if not email:
            raise ValueError("User must have email address.")
        su = self.model(email=self.normalize_email(email))
        su.set_password(password)
        su.is_staff = True
        su.is_superuser = True
        su.save(using=self._db)
        return su

    def get_queryset(self, *args, **kwargs):
        """Filter Users and returns Admins."""
        res = super().get_queryset(*args, **kwargs)
        return res.filter(role=User.Role.ADMIN)


class AdminUser(User):
    """Proxy Model for Admins, based off User."""
    base_role = User.Role.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Admins."


class Admin(models.Model):
    """Admin Profile model for storing Admin data."""
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    admin_dob = models.DateField()
    admin_address = models.TextField(blank=True, null=True)
    admin_contact = models.CharField(
        validators=[PHONE_REGEX], max_length=17, blank=True, null=True)
    admin_clinic = models.ForeignKey(
        Clinic, on_delete=models.SET_NULL, related_name="admin_clinic", null=True)
    user = models.OneToOneField(
        User, related_name="admin_info", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Admin " + self.admin_name
