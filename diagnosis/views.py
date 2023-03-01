"""View for the Diagnosis API."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from diagnosis.serializers import DiagnosisSerializer
from diagnosis.models import Diagnosis
from diagnosis.permissions import IsDoctorOrAdmin


class DiagnosisViewset(ModelViewSet):
    """View for managing Diagnosis API."""
    serializer_class = DiagnosisSerializer
    queryset = Diagnosis.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        encounter_id = self.request.query_params.get("encounter_id")
        if encounter_id is not None:
            encounter_id = int(encounter_id)
            queryset = queryset.filter(diagnosis_encounter_id=encounter_id)
        return queryset

    def get_permissions(self):
        """Instantiates and returns the list of permission that this view requires"""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsDoctorOrAdmin]
        return [permission() for permission in permission_classes]
