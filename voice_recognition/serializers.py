"""Serializer for Wave file for voice recognition."""

from rest_framework import serializers


class WavFileSerializer(serializers.Serializer):
    """Serializer for uploading wav files."""
    file = serializers.FileField()


class Base64EncodedStringSerializer(serializers.Serializer):
    """Serializer for the audio, which is a base64 encoded string"""
    data = serializers.CharField(allow_blank=False)
