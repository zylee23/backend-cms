"""View for Voice Recognition API."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser
from voice_recognition.models import DeepSpeechModel, decode_using_pyav
from voice_recognition.serializers import WavFileSerializer, Base64EncodedStringSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from base64 import b64decode
from io import BytesIO
from sys import getsizeof
from django.core.files.uploadedfile import InMemoryUploadedFile


def error_response(msg, status_code):
    payload = {
        "detail": msg,
    }
    return Response(payload, status_code)


class VoiceRecognitionAPIView(CreateAPIView):
    """CreateAPI view to upload .wav file and convert speech to text."""
    serializer_class = WavFileSerializer
    parser_classes = [FileUploadParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stt = DeepSpeechModel()

    def post(self, request, format="audio/wave"):
        """Transcribe the wav audio file speech to text."""
        try:
            wav_file = request.data['file']  # get django InMemoryUploadedFile
        except KeyError:
            return error_response("Audio file must be uploaded", status.HTTP_400_BAD_REQUEST)
        # audio_stream = wav_file.read()  # convert to bytes stream
        audio_bytes_stream = decode_using_pyav(wav_file)
        txt = self.stt.transcribe_batch_with_buffer(audio_bytes_stream)
        print(f"Transcribed: {txt}")
        payload = {
            "data": {
                "text": txt,
                "words": len(txt.split())
            }
        }
        return Response(payload, status.HTTP_200_OK)


class VoiceRecognitionMobileAPIView(CreateAPIView):
    """CreateAPI view to convert speech to text sent from mobile device. 

    The capacitor-voice-recorder plugin returns a base64 string representing the
    audio recording

    From my understanding, it is difficult to convert base64 string to a file/blob
    on Ionic native. So I propose to create a separate endpoint that takes in a
    base64 string within the request body, processes this base64 string into an
    audio buffer, and perform the speech to text conversion.

    Reference links:
    Write .wav file: https://stackoverflow.com/questions/62587308/python-how-to-use-speech-recognition-or-other-modules-to-convert-base64-audio
    Initialise io buffer: https://stackoverflow.com/questions/71280669/how-to-convert-base64-format-audio-files-into-wav-files-without-storage-them-on
    Intialise InMemoryUploadedFile object: https://stackoverflow.com/questions/67244002/how-to-create-inmemoryuploadedfile-objects-proper-in-django
    """
    serializer_class = Base64EncodedStringSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stt = DeepSpeechModel()

    def post(self, request, *args, **kwargs):
        """Transcribe the encoded string audio sent from Mobile to text."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        encoded_data = serializer.validated_data['data']
        decode_bytes = b64decode(encoded_data)

        with BytesIO() as buffer:
            # Create a buffer
            buffer.write(decode_bytes)
            buffer.seek(0)  # go to the start of the buffer

            # Initialise the InMemoryUploadedFile object
            in_memory_file = InMemoryUploadedFile(
                buffer,
                None,
                "speech.wav",
                "audio/wave",
                getsizeof(buffer),
                "utf-8"
            )
            audio_bytes_stream = decode_using_pyav(in_memory_file)
            txt = self.stt.transcribe_batch_with_buffer(audio_bytes_stream)
            print(f"Transcribed: {txt}")
            payload = {
                "data": {
                    "text": txt,
                    "words": len(txt.split())
                }
            }
            return Response(payload, status.HTTP_200_OK)
