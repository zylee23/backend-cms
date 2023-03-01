"""Tests for the Deepspeech Voice Recognition Model."""

from django.test import TestCase
from voice_recognition.models import DeepSpeechModel

AUDIO_FILES_LOW = {
    "One": {
        "path": "voice_recognition/tests/media/lung_cancer.wav",
        "expected": "the patient is diagnosed with lung cancer"
    },
    "Two": {
        "path": "voice_recognition/tests/media/polite2.wav",
        "expected": "experience proves this"
    }
}

AUDIO_FILES_HIGH = {
    "One": {
        "path": "voice_recognition/tests/media/high_freq/cig.wav",
        "expected": "the patient has been diagnosed with lung cancer he needs\
             to stop smoking cigarettes if he wants to live"
    }
}


class VoiceRecognitionModelTests(TestCase):
    """Tests for the Deepspeech Voice Recognition model."""

    def setUp(self) -> None:
        self.model = DeepSpeechModel()

    def test_stt_from_file_on_system_one(self):
        """Test Speech to Text on a system audio file one."""
        txt = self.model.transcibe_batch(AUDIO_FILES_LOW["One"]["path"])
        self.assertEqual(txt, AUDIO_FILES_LOW["One"]["expected"])

    def test_stt_from_file_on_system_two(self):
        """Test Speech to Text on a system audio file two."""
        txt = self.model.transcibe_batch(AUDIO_FILES_LOW["Two"]["path"])
        self.assertEqual(txt, AUDIO_FILES_LOW["Two"]["expected"])
