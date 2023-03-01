"""Views for the Clinic API."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    """Views for Managing the Clinic APIs."""
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def get_queryset(self):
        """Retrieves Clinics for Authenticated users."""
        return self.queryset.order_by("-clinic_id")

    def get_permissions(self):
        """Instantiates and returns the list of permission that this view requires"""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
