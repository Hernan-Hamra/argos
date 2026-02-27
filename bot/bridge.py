"""
Bridge bidireccional Telegram <-> Claude Code.

El loop.py escribe mensajes entrantes al inbox.
Claude Code lee el inbox, muestra en pantalla, procesa, responde.
Las respuestas van a Telegram Y se muestran en pantalla.

Uso desde Claude Code:
    python bot/bridge.py --check          # Ver mensajes nuevos
    python bot/bridge.py --reply "texto"  # Responder por Telegram
    python bot/bridge.py --history 10     # Últimos N mensajes
"""
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INBOX_FILE = os.path.join(DATA_DIR, 'telegram_inbox.jsonl')
POS_FILE = os.path.join(DATA_DIR, 'telegram_inbox.pos')


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def escribir_mensaje(direccion, contenido, tipo='text', extra=None):
    """Escribe un mensaje al inbox (in=recibido, out=enviado)."""
    _ensure_data_dir()
    entry = {
        'ts': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dir': direccion,
        'tipo': tipo,
        'contenido': contenido,
    }
    if extra:
        entry.update(extra)
    with open(INBOX_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry


def _leer_posicion():
    """Lee la posición del último mensaje leído (byte offset)."""
    if os.path.exists(POS_FILE):
        with open(POS_FILE) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def _guardar_posicion(pos):
    """Guarda la posición del último mensaje leído."""
    _ensure_data_dir()
    with open(POS_FILE, 'w') as f:
        f.write(str(pos))


def leer_nuevos():
    """Lee mensajes nuevos desde la última posición. Retorna lista de dicts."""
    if not os.path.exists(INBOX_FILE):
        return []

    pos = _leer_posicion()
    mensajes = []

    with open(INBOX_FILE, 'r', encoding='utf-8') as f:
        f.seek(pos)
        for line in f:
            line = line.strip()
            if line:
                try:
                    mensajes.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        nueva_pos = f.tell()

    _guardar_posicion(nueva_pos)
    return mensajes


def leer_historial(n=20):
    """Lee los últimos N mensajes del inbox."""
    if not os.path.exists(INBOX_FILE):
        return []

    mensajes = []
    with open(INBOX_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    mensajes.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return mensajes[-n:]


def responder(texto):
    """Envía respuesta por Telegram y la registra en el inbox."""
    from bot.send import send_text
    result = send_text(texto)
    escribir_mensaje('out', texto, tipo='text')
    return result


def preguntar(pregunta, timeout=300, intervalo=5):
    """Manda pregunta por Telegram y espera respuesta. Retorna texto de respuesta o None si timeout."""
    import time
    from bot.send import send_text
    send_text(f"ARGOS pregunta: {pregunta}")
    escribir_mensaje('out', f"ARGOS pregunta: {pregunta}", tipo='pregunta')

    inicio = time.time()
    while time.time() - inicio < timeout:
        msgs = leer_nuevos()
        for m in msgs:
            if m.get('dir') == 'in':
                return m.get('contenido', '')
        time.sleep(intervalo)
    return None


def formatear_mensaje(msg):
    """Formatea un mensaje para mostrar en pantalla."""
    ts = msg.get('ts', '?')
    hora = ts.split(' ')[1] if ' ' in ts else ts
    direccion = msg.get('dir', '?')
    contenido = msg.get('contenido', '')
    tipo = msg.get('tipo', 'text')

    if direccion == 'in':
        prefijo = f"[{hora}] HERNÁN"
        if tipo == 'audio':
            dur = msg.get('duracion', '?')
            transcripcion = msg.get('transcripcion', '')
            return f"{prefijo} (audio {dur}s): {transcripcion}"
        return f"{prefijo}: {contenido}"
    else:
        return f"[{hora}] ARGOS: {contenido}"


def mostrar_nuevos():
    """Lee y muestra mensajes nuevos formateados."""
    msgs = leer_nuevos()
    if not msgs:
        print("(sin mensajes nuevos)")
        return []
    print(f"--- {len(msgs)} mensaje(s) nuevo(s) ---")
    for m in msgs:
        print(formatear_mensaje(m))
    print("---")
    return msgs


def mostrar_historial(n=20):
    """Muestra los últimos N mensajes formateados."""
    msgs = leer_historial(n)
    if not msgs:
        print("(sin historial)")
        return []
    print(f"--- Últimos {len(msgs)} mensajes ---")
    for m in msgs:
        print(formatear_mensaje(m))
    print("---")
    return msgs


if __name__ == '__main__':
    if '--check' in sys.argv:
        mostrar_nuevos()
    elif '--reply' in sys.argv:
        idx = sys.argv.index('--reply')
        if idx + 1 < len(sys.argv):
            texto = ' '.join(sys.argv[idx + 1:])
            responder(texto)
            print(f"Enviado: {texto}")
        else:
            print("Uso: python bot/bridge.py --reply <texto>")
    elif '--history' in sys.argv:
        idx = sys.argv.index('--history')
        n = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 20
        mostrar_historial(n)
    else:
        print("Uso:")
        print("  python bot/bridge.py --check          # Ver mensajes nuevos")
        print("  python bot/bridge.py --reply 'texto'  # Responder")
        print("  python bot/bridge.py --history 10     # Últimos N mensajes")
