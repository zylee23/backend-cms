"""Views for Appointment Module."""

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from appointment.models import Appointment
from users.models import User, Patient, Doctor
from appointment.serializers import AppointmentSerializer, AppointmentSerializerExtended


class AppointmentViewSet(viewsets.ModelViewSet):
    """View for managing the Appointments API."""
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve appointments for authenticated users."""
        status = self.request.query_params.get("status")
        queryset = self.queryset.exclude(
            appointment_status=Appointment.Status.CANCELLED)
        if self.action == "retrieve":
            queryset = self.queryset
        if status and self.action == "list":
            if status.lower() == "attended":
                queryset = queryset.filter(
                    appointment_status=Appointment.Status.ATTENDED)
            if status.lower() == "unattended":
                queryset = queryset.exclude(
                    appointment_status=Appointment.Status.ATTENDED)
            if status.lower() == "cancelled":
                queryset = self.queryset.filter(
                    appointment_status=Appointment.Status.CANCELLED)
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return queryset.order_by("-appointment_date", "-appointment_time")
        elif user.role == User.Role.PATIENT:
            patient_profile = Patient.objects.get(user=user)
            return queryset.filter(appointment_patient=patient_profile).order_by("-appointment_date", "-appointment_time")
        else:
            # user is a doctor
            doctor_profile = Doctor.objects.get(user=user)
            return queryset.filter(appointment_doctor=doctor_profile).order_by("-appointment_date", "-appointment_time")

    def create(self, request, *args, **kwargs):
        """Creates appointments using given serializer, and returns data using ExtendedSerializer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ap = serializer.save()
        return_serializer = AppointmentSerializerExtended(ap)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        """Update existing appointment using given serializer, and return data using ExtendedSerializer."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        ap = serializer.save()
        return_serializer = AppointmentSerializerExtended(ap)
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """Partial Update existing appointment using given serializer, and return data using ExtendedSerializer."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ap = serializer.save()
        return_serializer = AppointmentSerializerExtended(ap)
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AppointmentSerializerExtended
        return self.serializer_class
