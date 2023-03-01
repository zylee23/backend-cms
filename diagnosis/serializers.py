"""Serializers for the Diagnosis View."""

from rest_framework import serializers
from diagnosis.models import Diagnosis
from encounter.models import Encounter


class DiagnosisSerializer(serializers.ModelSerializer):
    """Serializer for Diagnosis."""
    diagnosis_encounter = serializers.PrimaryKeyRelatedField(
        queryset=Encounter.objects.all()
    )

    class Meta:
        model = Diagnosis
        fields = ["diagnosis_id", "diagnosis_weight", "diagnosis_height", "diagnosis_symptoms", "diagnosis_history",
                  "diagnosis_blood_pressure", "diagnosis_heart_rate", "diagnosis_resp_rate", "diagnosis_oxy_saturation",
                  "diagnosis_temp", "diagnosis_descr", "diagnosis_icd", "diagnosis_prescription", "diagnosis_encounter"]
        read_only_fields = ["diagnosis_id"]
