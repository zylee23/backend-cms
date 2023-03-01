"""Views for the User API."""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import (AdminUser, DoctorUser, PatientUser,
                          User, Patient, Doctor, Admin)
from users.serializers import (
    AdminUserSerializer, AuthTokenSerializer, DoctorUserSerializer,
    PatientSerializer, PatientUserSerializer, DoctorSerializer, AdminSerializer,
    get_user_serializer
)


class PatientUserCreateAPIView(generics.CreateAPIView):
    """Create a new PatientUser along with Patient data."""
    queryset = PatientUser.objects.all()
    serializer_class = PatientUserSerializer


class DoctorUserCreateAPIView(generics.CreateAPIView):
    """Create a new DoctorUser along with Doctor data."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer


class AdminUserCreateAPIView(generics.CreateAPIView):
    """Create a new AdminUser along with Admin data."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """Validate login credentials & return the token with user object."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_sz = get_user_serializer(user.role)
        user_data = user_sz(user).data
        return Response({'token': token.key, 'user': user_data})


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Generic View to retrieve and update User with UserProfile."""
    serializer_class = PatientUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user

    def get_serializer_class(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return AdminUserSerializer
        elif user.role == User.Role.DOCTOR:
            return DoctorUserSerializer
        else:
            return self.serializer_class


class PatientProfileListAPIView(generics.ListAPIView,
                                generics.RetrieveAPIView):
    """Get list of all patient profiles or a single patient profile."""
    serializer_class = PatientSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Patient.objects.all()


class PatientProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Get a single patient profile."""
    serializer_class = PatientSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Patient.objects.all()


class DoctorProfileListAPIView(generics.ListAPIView,
                               generics.RetrieveAPIView):
    """Get list of all Doctor profiles or a single doctor profile."""
    serializer_class = DoctorSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.all()


class DoctorProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Get a single doctor profile."""
    serializer_class = DoctorSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.all()


class AdminProfileListAPIView(generics.ListAPIView):
    """Get list of all Admin profiles or a single admin profile."""
    serializer_class = AdminSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Admin.objects.all()


class AdminProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Get a single Admin profile."""
    serializer_class = AdminSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Admin.objects.all()
