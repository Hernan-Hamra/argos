"""
ARGOS Bot Loop - Escucha Telegram continuamente.
Escribe al inbox JSONL para que Claude Code (backend) procese y responda.

Uso:
    python bot/loop.py          # Foreground
    python bot/loop.py &        # Background

Qué hace:
- Polling cada 10 seg
- Texto: escribe al inbox + guarda en DB
- Audio: descarga + transcribe con Whisper + escribe al inbox + guarda en DB
- Confirma recepción por Telegram
"""

import sys
import os
import time
import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.receive import get_updates, download_voice
from bot.send import send_text
from bot.bridge import escribir_mensaje
from bot.config import ALLOWED_CHAT_ID

# Whisper se carga lazy (tarda ~10seg primera vez)
_stt_loaded = False


def _transcribe(audio_path):
    """Transcribir audio con Whisper (carga lazy)."""
    global _stt_loaded
    from bot.stt import transcribe
    if not _stt_loaded:
        print("[LOOP] Cargando Whisper (primera vez)...")
        _stt_loaded = True
    return transcribe(audio_path)


def _save_to_db(tipo, contenido, transcripcion=None):
    """Guardar mensaje recibido en la DB."""
    try:
        from tools.tracker import get_connection
        from datetime import datetime
        conn = get_connection()
        c = conn.cursor()
        ahora = datetime.now()

        # Buscar sesión abierta
        c.execute("SELECT id FROM sesiones WHERE estado = 'abierta' ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        sesion_id = row['id'] if row else None

        # Guardar como mensaje
        c.execute('''INSERT INTO mensajes (sesion_id, timestamp, rol, contenido, tipo)
                     VALUES (?, ?, 'user', ?, ?)''',
                  (sesion_id, ahora.strftime('%Y-%m-%d %H:%M:%S'),
                   transcripcion or contenido, tipo))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[LOOP] Error guardando en DB: {e}")


def process_message(msg):
    """Procesar un mensaje de Telegram."""
    chat_id = msg.get('chat_id')

    # Seguridad: solo procesar mensajes del chat autorizado
    if str(chat_id) != str(ALLOWED_CHAT_ID):
        print(f"[LOOP] Mensaje ignorado de chat_id={chat_id} (no autorizado)")
        return

    if msg['type'] == 'text':
        print(f"[LOOP] Texto: {msg['content'][:80]}")
        # Escribir al inbox para que Claude Code lo lea
        escribir_mensaje('in', msg['content'], tipo='text')
        _save_to_db('texto_telegram', msg['content'])
        send_text(f"Recibido. ARGOS procesando...")

    elif msg['type'] == 'voice':
        dur = msg.get('duration', '?')
        print(f"[LOOP] Audio {dur}s recibido, procesando...")
        send_text(f"Audio {dur}s recibido, transcribiendo...")

        try:
            path = download_voice(msg['file_id'])
            texto = _transcribe(path)
            print(f"[LOOP] Transcripcion: {texto[:100]}")
            # Escribir al inbox con la transcripción
            escribir_mensaje('in', texto, tipo='audio',
                           extra={'duracion': dur, 'audio_original': msg['content']})
            _save_to_db('audio_telegram', msg['content'], transcripcion=texto)
            send_text(f"Transcrito. ARGOS procesando...")
        except Exception as e:
            print(f"[LOOP] Error transcribiendo: {e}")
            send_text(f"Error procesando audio: {e}")

    elif msg['type'] == 'audio':
        print(f"[LOOP] Archivo de audio recibido")
        send_text("Archivo de audio recibido (solo soporto notas de voz por ahora)")

    else:
        print(f"[LOOP] Mensaje tipo '{msg['type']}' no soportado")


def run_loop(interval=10):
    """Loop principal de polling."""
    print(f"[LOOP] ARGOS Bot escuchando (cada {interval}s)...")
    print(f"[LOOP] Chat autorizado: {ALLOWED_CHAT_ID}")
    print(f"[LOOP] Ctrl+C para detener")

    escribir_mensaje('system', 'Loop iniciado - escuchando Telegram', tipo='system')
    send_text("ARGOS escuchando. Tus mensajes llegan al backend.")

    while True:
        try:
            msgs = get_updates(mark_read=True)
            for msg in msgs:
                process_message(msg)
        except KeyboardInterrupt:
            print("\n[LOOP] Detenido por usuario")
            send_text("ARGOS Bot detenido.")
            break
        except Exception as e:
            print(f"[LOOP] Error en polling: {e}")
            time.sleep(30)  # Esperar más si hay error
            continue

        time.sleep(interval)


if __name__ == '__main__':
    run_loop()
