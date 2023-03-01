"""Views for Encounter Module."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from encounter.models import Encounter
from users.models import User, Patient, Doctor
from encounter.serializers import (
    EncounterSerializer, EncounterSerializerExtended
)


class EncounterViewSet(viewsets.ModelViewSet):
    """View for managing the Encounters API."""
    serializer_class = EncounterSerializer
    queryset = Encounter.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve encounters for authenticated users."""
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return self.queryset.all().order_by("-encounter_date", "-encounter_time")
        elif user.role == User.Role.PATIENT:
            patient_profile = Patient.objects.get(user=user)
            return self.queryset.filter(encounter_patient=patient_profile).order_by("-encounter_date", "-encounter_time")
        else:
            # user is a doctor
            doctor_profile = Doctor.objects.get(user=user)
            return self.queryset.filter(encounter_doctor=doctor_profile).order_by("-encounter_date", "-encounter_time")

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return EncounterSerializerExtended
        return self.serializer_class

    def get_permissions(self):
        """Instantiates and returns the list of permission that this view requires"""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Creates Encounters using given serializer, and returns data using ExtendedSerializer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enc = serializer.save()
        return_serializer = EncounterSerializerExtended(enc)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        """Update existing encounter using given serializer, and return data using ExtendedSerializer."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        enc = serializer.save()
        return_serializer = EncounterSerializerExtended(enc)
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """Partial Update existing encounter using given serializer, and return data using ExtendedSerializer."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ap = serializer.save()
        return_serializer = EncounterSerializerExtended(ap)
        return Response(return_serializer.data, status=status.HTTP_200_OK)
