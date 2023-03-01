from deepspeech import Model
import numpy as np
import wave
import av


class DeepSpeechModel:
    """DeepSpeech Voice Recognition Model."""

    def __init__(self) -> None:
        # setting the environment and getting the model instance
        model_file_path = "voice_recognition/engine/deepspeech-0.9.3-models.pbmm"
        lm_file_path = "voice_recognition/engine/deepspeech-0.9.3-models.scorer"
        beam_width = 500
        lm_alpha = 0.75
        lm_beta = 1.85

        self.model = Model(model_file_path)
        self.model.enableExternalScorer(lm_file_path)
        self.model.setScorerAlphaBeta(lm_alpha, lm_beta)
        self.model.setBeamWidth(beam_width)

    def read_wave_file(self, filename: str):
        with wave.open(filename, 'rb') as w:
            rate = w.getframerate()
            frames = w.getnframes()
            buffer = w.readframes(frames)
        return buffer, rate

    def transcibe_batch(self, audio_filename: str):
        buffer, rate = self.read_wave_file(audio_filename)
        data16 = np.frombuffer(buffer, dtype=np.int16)
        return self.model.stt(data16)

    def transcribe_batch_with_buffer(self, buffer):
        data16 = np.frombuffer(buffer, dtype=np.int16)
        return self.model.stt(data16)


def decode_using_pyav(file):
    """Resample the input audio to 16kHz Mono. (Deepspeech Model requirements).
    :returns: 1D numpy array 
    """
    audio = av.open(file)
    # print(f"number of channels: {audio.streams.audio}")
    if len(audio.streams.audio) > 1:
        print("Audio has more than 1 stream. Only one will be used.")

    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    resampled_frames = []
    for frame in audio.decode(audio=0):
        # As of PyAV 9.0, one input frame may be resampled to multiple outputs.
        # Convert each into a numpy ndarray...
        iterable_frames = map(lambda f: f.to_ndarray(),
                              resampler.resample(frame))
        # ...then flatten each of those arrays down to 1D
        flat_frames = list(map(lambda f: f.flatten(), iterable_frames))
        # Add all of the resampled frames to our output list
        resampled_frames.extend(flat_frames)
    return np.concatenate(resampled_frames)
