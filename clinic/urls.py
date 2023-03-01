"""URL mapping for Clinics."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clinic import views

router = DefaultRouter()
router.register("clinics", views.ClinicViewSet)
app_name = "clinic"
urlpatterns = [
    path("", include(router.urls)),
]
