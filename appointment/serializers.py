"""Serailzers for the Appointment Module."""

from rest_framework import serializers
from appointment.models import Appointment
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer
from users.serializers import PatientSerializer, DoctorSerializer
from users.models import Patient, Doctor


class AppointmentSerializer(serializers.ModelSerializer):
    """Seralizer for Appointments."""
    appointment_patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all())
    appointment_doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all())
    appointment_clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        required=False)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appointment_id", "appointment_date", "appointment_time",
                  "appointment_status", "appointment_comments", "appointment_patient",
                  "appointment_doctor", "appointment_clinic", "created_by"]
        read_only_fields = ["appointment_id", "created_by"]

    def create(self, validated_data):
        """Create an appointment."""
        auth_user = self.context["request"].user
        appointment = Appointment.objects.create(
            created_by=auth_user, **validated_data)
        return appointment

    def update(self, instance, validated_data):
        """Update an appointment."""
        validated_data.pop("created_by", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AppointmentSerializerExtended(AppointmentSerializer):
    """Extended Seralizer for Appointments. Returns full Patient, Doctor and Clinic Model."""
    appointment_patient = PatientSerializer(read_only=True)
    appointment_doctor = DoctorSerializer(read_only=True)
    appointment_clinic = ClinicSerializer(read_only=True)
