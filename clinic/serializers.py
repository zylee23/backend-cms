"""Serializers for the Clinic Module."""

from rest_framework import serializers
from clinic.models import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    """Clinic Serializer."""

    class Meta:
        model = Clinic
        fields = ["clinic_id", "clinic_name",
                  "clinic_address", "clinic_contact"]
        read_only_fields = ["clinic_id"]
