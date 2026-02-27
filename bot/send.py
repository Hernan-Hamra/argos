"""Enviar mensajes y audio a Hernán por Telegram."""
import sys
import os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot.config import API_BASE, ALLOWED_CHAT_ID, TEMP_DIR


def send_text(text, chat_id=None):
    """Envía un mensaje de texto por Telegram."""
    chat_id = chat_id or ALLOWED_CHAT_ID
    if not chat_id:
        print("ERROR: ALLOWED_CHAT_ID no configurado en .env")
        return None
    resp = requests.post(f"{API_BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })
    data = resp.json()
    if data.get("ok"):
        print(f"Enviado OK: {text[:80]}...")
    else:
        # Fallback: enviar sin Markdown si falla el parsing
        resp2 = requests.post(f"{API_BASE}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
        data = resp2.json()
        if data.get("ok"):
            print(f"Enviado OK (sin formato): {text[:80]}...")
        else:
            print(f"Error: {data}")
    return data


def send_voice(audio_path, chat_id=None, caption=None):
    """Envía un archivo de audio como nota de voz por Telegram."""
    chat_id = chat_id or ALLOWED_CHAT_ID
    if not chat_id:
        print("ERROR: ALLOWED_CHAT_ID no configurado en .env")
        return None
    with open(audio_path, 'rb') as f:
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        resp = requests.post(f"{API_BASE}/sendVoice", data=data, files={"voice": f})
    result = resp.json()
    if result.get("ok"):
        print(f"Audio enviado OK: {audio_path}")
    else:
        print(f"Error enviando audio: {result}")
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mensaje = " ".join(sys.argv[1:])
        send_text(mensaje)
    else:
        print("Uso: python bot/send.py <mensaje>")
