"""Serializers for the users API View."""

from django.utils.translation import gettext as _
from rest_framework import serializers
from clinic.models import Clinic
from users.models import (
    Admin, AdminUser, Doctor, DoctorUser, Patient, PatientUser, User
)
from django.contrib.auth import authenticate


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient Model."""
    patient_clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        required=False
    )

    class Meta:
        model = Patient
        fields = ["patient_id", "patient_name", "patient_dob",
                  "patient_address", "patient_contact", "patient_clinic"]
        read_only_fields = ["patient_id"]


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor Model."""
    doctor_clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        required=False
    )

    class Meta:
        model = Doctor
        fields = ["doctor_id", "doctor_name", "doctor_dob",
                  "doctor_address", "doctor_contact", "doctor_clinic"]
        read_only_fields = ["doctor_id"]


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin Model."""
    admin_clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        required=False
    )

    class Meta:
        model = Admin
        fields = ["admin_id", "admin_name", "admin_dob",
                  "admin_address", "admin_contact", "admin_clinic"]
        read_only_fields = ["admin_id"]


class PatientUserSerializer(serializers.ModelSerializer):
    """Serializer for the PatientUser Container (PatientUser + Patient)."""
    patient_info = PatientSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "password", "role", "patient_info"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}, "role": {
            "read_only": True}, "is_staff": {"read_only": True}}

    def create(self, validated_data):
        """Create and return a new PatientUser with encrypted password. Insert patient_info into Patient table."""
        patient_info_data = validated_data.pop('patient_info')
        user = PatientUser.objects.create_user(**validated_data)
        Patient.objects.create(user=user, **patient_info_data)
        return user

    def update(self, instance, validated_data):
        """Update and return PatientUser. Update Patient table as well."""
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        patient_info_data = validated_data.pop('patient_info')
        user = super().update(instance, validated_data)

        if patient_info_data:
            patient_profile_instance = Patient.objects.filter(
                user=user).first()
            patient_profile_sz = PatientSerializer(
                instance=patient_profile_instance, data=patient_info_data)
            if patient_profile_sz.is_valid():
                patient_profile_sz.save()
        if password:
            user.set_password(password)
            user.save()
        return user


class DoctorUserSerializer(serializers.ModelSerializer):
    """Serializer for the DoctorUser Container (DoctorUser + Doctor)."""
    doctor_info = DoctorSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "password", "role", "doctor_info"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}, "role": {
            "read_only": True}, "is_staff": {"read_only": True}}

    def create(self, validated_data):
        """Create and return a new DoctorUser with encrypted password. Insert doctor_info into doctor table."""
        doctor_info_data = validated_data.pop('doctor_info')
        user = DoctorUser.objects.create_user(**validated_data)
        Doctor.objects.create(user=user, **doctor_info_data)
        return user

    def update(self, instance, validated_data):
        """Update and return doctorUser. Update doctor table as well."""
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        doctor_info_data = validated_data.pop('doctor_info')
        user = super().update(instance, validated_data)

        if doctor_info_data:
            doctor_profile_instance = Doctor.objects.filter(
                user=user).first()
            doctor_profile_sz = DoctorSerializer(
                instance=doctor_profile_instance, data=doctor_info_data)
            if doctor_profile_sz.is_valid():
                doctor_profile_sz.save()
        if password:
            user.set_password(password)
            user.save()
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for the AdminUser Container (AdminUser + Admin)."""
    admin_info = AdminSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "password", "role", "admin_info"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}, "role": {
            "read_only": True}, "is_staff": {"read_only": True}}

    def create(self, validated_data):
        """Create and return a new AdminUser with encrypted password. Insert admin_info into admin table."""
        admin_info_data = validated_data.pop('admin_info')
        user = AdminUser.objects.create_user(**validated_data)
        Admin.objects.create(user=user, **admin_info_data)
        return user

    def update(self, instance, validated_data):
        """Update and return AdminUser. Update Admin table as well."""
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        admin_info_data = validated_data.pop('admin_info')
        user = super().update(instance, validated_data)

        if admin_info_data:
            admin_profile_instance = Admin.objects.filter(
                user=user).first()
            admin_profile_sz = AdminSerializer(
                instance=admin_profile_instance, data=admin_info_data)
            if admin_profile_sz.is_valid():
                admin_profile_sz.save()
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
        attrs['user'] = user
        return attrs


def get_user_serializer(role):
    """Return correct user serializer based on user role."""
    if role == User.Role.ADMIN:
        return AdminUserSerializer
    if role == User.Role.PATIENT:
        return PatientUserSerializer
    if role == User.Role.DOCTOR:
        return DoctorUserSerializer
