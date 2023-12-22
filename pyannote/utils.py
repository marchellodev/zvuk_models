import base64
import io

import brotli
from torchaudio import load


def decode_audio(audio_base64, audio_brotli=False):
    wav_bytes = base64.b64decode(audio_base64)
    if audio_brotli:
        wav_bytes = brotli.decompress(wav_bytes)
    wav_file = io.BytesIO(wav_bytes)
    waveform, sampling_rate = load(wav_file)
    return waveform, sampling_rate
