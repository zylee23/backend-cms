"""URL mapping for Encounter Module."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from encounter import views

router = DefaultRouter()
router.register("encounters", views.EncounterViewSet)
app_name = "encounter"
urlpatterns = [
    path("", include(router.urls)),
]
