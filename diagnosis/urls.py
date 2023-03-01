"""URL mapping for Diagnosis Module."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from diagnosis import views

router = DefaultRouter()
router.register("diagnosis", views.DiagnosisViewset)
app_name = "diagnosis"
urlpatterns = [
    path("", include(router.urls)),
]
