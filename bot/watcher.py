"""
Watcher: espera hasta que llegue un mensaje nuevo de Telegram al inbox.
Sale con el mensaje cuando lo encuentra. Diseñado para ser llamado
en background por Claude Code — cuando termina, Claude Code responde.
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INBOX_FILE = os.path.join(DATA_DIR, 'telegram_inbox.jsonl')
POS_FILE = os.path.join(DATA_DIR, 'telegram_watcher.pos')


def _leer_posicion():
    if os.path.exists(POS_FILE):
        with open(POS_FILE) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def _guardar_posicion(pos):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(POS_FILE, 'w') as f:
        f.write(str(pos))


def watch(interval=3, timeout=300):
    """Espera mensajes nuevos. Sale cuando encuentra uno entrante."""
    if not os.path.exists(INBOX_FILE):
        # Empezar desde el final del archivo actual
        _guardar_posicion(0)

    # Si es primera vez, ir al final del archivo para no leer historial
    pos = _leer_posicion()
    if pos == 0 and os.path.exists(INBOX_FILE):
        with open(INBOX_FILE, 'r', encoding='utf-8') as f:
            f.seek(0, 2)  # ir al final
            _guardar_posicion(f.tell())

    inicio = time.time()
    while time.time() - inicio < timeout:
        if not os.path.exists(INBOX_FILE):
            time.sleep(interval)
            continue

        pos = _leer_posicion()
        with open(INBOX_FILE, 'r', encoding='utf-8') as f:
            f.seek(pos)
            contenido_leido = f.read()
            nueva_pos = f.tell()

        # Procesar lineas leidas
        for line in contenido_leido.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get('dir') == 'in':
                    _guardar_posicion(nueva_pos)
                    tipo = msg.get('tipo', 'text')
                    contenido = msg.get('contenido', '')
                    print(f"[TELEGRAM] ({tipo}) {contenido}")
                    return contenido
            except json.JSONDecodeError:
                continue
        _guardar_posicion(nueva_pos)

        time.sleep(interval)

    print("[WATCHER] Timeout sin mensajes")
    return None


if __name__ == '__main__':
    watch()
