from django.urls import path
from voice_recognition.views import VoiceRecognitionAPIView, VoiceRecognitionMobileAPIView

urlpatterns = [
    path("", VoiceRecognitionAPIView.as_view(),
         name="Voice Recognition Speech to Text for Web"),
    path("mobile/", VoiceRecognitionMobileAPIView.as_view(),
         name="Voice Recognition Speech to Text for Mobile")
]
