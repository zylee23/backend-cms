"""URL mappings for the user API."""

from django.urls import path
from users import views

app_name = "users"
urlpatterns = [
    path("patients/create/", views.PatientUserCreateAPIView.as_view(),
         name="patient-create"),
    path("doctors/create/", views.DoctorUserCreateAPIView.as_view(),
         name="doctor-create"),
    path("admins/create/", views.AdminUserCreateAPIView.as_view(),
         name="admin-create"),
    path("patients/", views.PatientProfileListAPIView.as_view(),
         name="patients"),
    path("doctors/", views.DoctorProfileListAPIView.as_view(),
         name="doctors"),
    path("admins/", views.AdminProfileListAPIView.as_view(),
         name="admins"),
    path("patients/<int:pk>", views.PatientProfileRetrieveAPIView.as_view(),
         name="patients-details"),
    path("doctors/<int:pk>", views.DoctorProfileRetrieveAPIView.as_view(),
         name="doctor-details"),
    path("admins/<int:pk>", views.AdminProfileRetrieveAPIView.as_view(),
         name="admin-details"),
    path("me", views.ManageUserView.as_view(), name="me"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
]
