"""Leer mensajes nuevos de Telegram."""
import sys
import os
import json
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot.config import API_BASE, ALLOWED_CHAT_ID, TEMP_DIR

# Archivo para guardar el último update_id procesado
OFFSET_FILE = os.path.join(os.path.dirname(__file__), '.last_update_id')


def _load_offset():
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE) as f:
            return int(f.read().strip())
    return None


def _save_offset(offset):
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))


def get_updates(mark_read=True):
    """Obtiene mensajes nuevos de Telegram. Retorna lista de mensajes."""
    params = {"timeout": 1}
    offset = _load_offset()
    if offset:
        params["offset"] = offset

    resp = requests.get(f"{API_BASE}/getUpdates", params=params)
    data = resp.json()

    if not data.get("ok"):
        print(f"Error: {data}")
        return []

    updates = data.get("result", [])
    messages = []

    for update in updates:
        msg = update.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        from_user = msg.get("from", {}).get("first_name", "?")
        update_id = update["update_id"]

        entry = {
            "update_id": update_id,
            "chat_id": chat_id,
            "from": from_user,
            "date": msg.get("date"),
        }

        if msg.get("text"):
            entry["type"] = "text"
            entry["content"] = msg["text"]
        elif msg.get("voice"):
            entry["type"] = "voice"
            entry["file_id"] = msg["voice"]["file_id"]
            entry["duration"] = msg["voice"].get("duration", 0)
            entry["content"] = f"[Audio {entry['duration']}s]"
        elif msg.get("audio"):
            entry["type"] = "audio"
            entry["file_id"] = msg["audio"]["file_id"]
            entry["content"] = f"[Audio file]"
        else:
            entry["type"] = "other"
            entry["content"] = "[Mensaje no soportado]"

        messages.append(entry)

        if mark_read:
            _save_offset(update_id + 1)

    return messages


def download_voice(file_id, output_path=None):
    """Descarga un archivo de audio de Telegram. Retorna path al archivo."""
    resp = requests.get(f"{API_BASE}/getFile", params={"file_id": file_id})
    data = resp.json()
    if not data.get("ok"):
        print(f"Error obteniendo archivo: {data}")
        return None

    file_path = data["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN', '')}/{file_path}"

    # Usar token de config
    from bot.config import TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

    if not output_path:
        os.makedirs(TEMP_DIR, exist_ok=True)
        ext = os.path.splitext(file_path)[1] or '.ogg'
        output_path = os.path.join(TEMP_DIR, f"voice_msg{ext}")

    resp = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(resp.content)
    print(f"Audio descargado: {output_path} ({len(resp.content)} bytes)")
    return output_path


def show_chat_ids():
    """Muestra todos los chat_ids de mensajes recientes (para configurar ALLOWED_CHAT_ID)."""
    params = {"timeout": 1}
    resp = requests.get(f"{API_BASE}/getUpdates", params=params)
    data = resp.json()
    if not data.get("ok") or not data.get("result"):
        print("No hay mensajes. Mandá /start al bot desde Telegram primero.")
        return

    seen = set()
    for update in data["result"]:
        msg = update.get("message", {})
        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        name = chat.get("first_name", "?")
        if chat_id and chat_id not in seen:
            print(f"  Chat ID: {chat_id}  |  Nombre: {name}")
            seen.add(chat_id)


if __name__ == "__main__":
    if "--chat-ids" in sys.argv:
        print("Chat IDs encontrados:")
        show_chat_ids()
    else:
        msgs = get_updates()
        if not msgs:
            print("No hay mensajes nuevos.")
        for m in msgs:
            print(f"[{m['type']}] {m['from']} (chat:{m['chat_id']}): {m['content']}")
