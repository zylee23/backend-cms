"""Serializer for Encounter View."""

from rest_framework import serializers
from encounter.models import Encounter
from appointment.models import Appointment
from users.models import Patient, Doctor
from users.serializers import PatientSerializer, DoctorSerializer
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer


class EncounterSerializer(serializers.ModelSerializer):
    """Serializer for Encounters."""

    encounter_patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )
    encounter_doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )
    encounter_appointment = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(),
        required=False
    )
    encounter_clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        required=False
    )
    encounter_created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Encounter
        fields = ["encounter_id", "encounter_date", "encounter_time", "encounter_appointment",
                  "encounter_comments", "encounter_patient", "encounter_doctor", "encounter_clinic",
                  "encounter_created_by"]
        read_only_fields = ["encounter_id", "encounter_created_by"]

    def create(self, validated_data):
        """Create an encounter."""
        auth_user = self.context["request"].user
        encounter = Encounter.objects.create(
            encounter_created_by=auth_user, **validated_data)
        return encounter

    def update(self, instance, validated_data):
        """Update an encounter."""
        validated_data.pop("created_by", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class EncounterSerializerExtended(EncounterSerializer):
    """Extended Seralizer for Encounters. Returns full Patient, Doctor and Clinic Model."""
    encounter_patient = PatientSerializer(read_only=True)
    encounter_doctor = DoctorSerializer(read_only=True)
    encounter_clinic = ClinicSerializer(read_only=True)
