"""Speech-to-Text con faster-whisper (local, gratis, sin límites)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot.config import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE, TEMP_DIR

_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        print(f"Cargando modelo Whisper '{WHISPER_MODEL}' (primera vez descarga ~500MB)...")
        _model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE)
        print("Modelo Whisper listo.")
    return _model


def transcribe(audio_path):
    """Transcribe un archivo de audio a texto. Retorna el texto."""
    model = _get_model()
    segments, info = model.transcribe(audio_path, language="es")
    text = " ".join(seg.text.strip() for seg in segments)
    return text


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Transcribiendo: {path}")
        result = transcribe(path)
        print(f"Texto: {result}")
    else:
        print("Uso: python bot/stt.py <archivo_audio>")
