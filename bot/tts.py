"""Text-to-Speech con edge-tts (gratis, voz argentina)."""
import os
import sys
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot.config import TTS_VOICE, TEMP_DIR


async def _synthesize(text, output_path):
    import edge_tts
    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(output_path)


def text_to_audio(text, output_path=None):
    """Genera audio desde texto. Retorna path al archivo MP3."""
    if not output_path:
        os.makedirs(TEMP_DIR, exist_ok=True)
        output_path = os.path.join(TEMP_DIR, "tts_response.mp3")
    asyncio.run(_synthesize(text, output_path))
    print(f"Audio generado: {output_path} ({os.path.getsize(output_path)} bytes)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        texto = " ".join(sys.argv[1:])
        path = text_to_audio(texto)
        print(f"Guardado en: {path}")
    else:
        print("Uso: python bot/tts.py <texto a convertir>")
