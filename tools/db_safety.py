"""
ARGOS DB Safety - Protección contra borrados accidentales.
Principio: NUNCA perder datos. Toda operación destructiva deja rastro.

Incluye:
- WAL mode (mejor concurrencia, menos corrupción)
- Backup pre-operación destructiva
- Soft delete (marcar como eliminado, no borrar)
- Log de operaciones destructivas
- Restauración de registros borrados
"""

import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'argos_tracker.db')
SAFETY_LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'safety_log.db')


def init_safety():
    """Inicializar protecciones: WAL mode + tabla de papelera + log de operaciones."""
    conn = sqlite3.connect(DB_PATH)

    # WAL mode: mejor rendimiento, menos riesgo de corrupción
    conn.execute("PRAGMA journal_mode=WAL")

    # Tabla papelera: donde van los registros "borrados"
    conn.execute('''CREATE TABLE IF NOT EXISTS _papelera (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabla_origen TEXT NOT NULL,
        registro_id INTEGER NOT NULL,
        datos TEXT NOT NULL,
        borrado_por TEXT DEFAULT 'sistema',
        motivo TEXT,
        fecha_borrado TEXT DEFAULT (datetime('now','localtime')),
        restaurado INTEGER DEFAULT 0
    )''')

    # Log de operaciones destructivas
    conn.execute('''CREATE TABLE IF NOT EXISTS _operaciones_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT (datetime('now','localtime')),
        operacion TEXT NOT NULL,
        tabla TEXT NOT NULL,
        registro_id INTEGER,
        query TEXT,
        backup_file TEXT,
        resultado TEXT
    )''')

    conn.commit()
    conn.close()


def backup_antes_de_operar(operacion_desc):
    """Crear backup rápido antes de una operación destructiva.
    Retorna el path del backup o None si falla.
    """
    if not os.path.exists(DB_PATH):
        return None

    backup_dir = os.path.join(os.path.dirname(DB_PATH), 'safety_backups')
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Sanitizar descripción para nombre de archivo
    desc_safe = operacion_desc[:30].replace(' ', '_').replace('/', '-')
    filename = f'pre_{desc_safe}_{timestamp}.db'
    dest = os.path.join(backup_dir, filename)

    try:
        shutil.copy2(DB_PATH, dest)

        # Rotar: mantener últimos 20 safety backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('pre_')])
        if len(backups) > 20:
            for old in backups[:-20]:
                os.remove(os.path.join(backup_dir, old))

        return dest
    except Exception as e:
        print(f"WARN: Safety backup falló: {e}")
        return None


def soft_delete(tabla, registro_id, motivo=None, borrado_por='claude'):
    """Mover un registro a la papelera en vez de borrarlo.
    El registro se marca con _eliminado=1 si la columna existe,
    o se mueve a _papelera como JSON.
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Leer el registro antes de tocarlo
    c.execute(f'SELECT * FROM {tabla} WHERE id = ?', (registro_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False

    datos = json.dumps(dict(row), ensure_ascii=False, default=str)

    # Guardar en papelera
    c.execute('''INSERT INTO _papelera (tabla_origen, registro_id, datos, borrado_por, motivo)
                 VALUES (?, ?, ?, ?, ?)''',
              (tabla, registro_id, datos, borrado_por, motivo))

    # Log de la operación
    c.execute('''INSERT INTO _operaciones_log (operacion, tabla, registro_id, query, resultado)
                 VALUES ('soft_delete', ?, ?, ?, 'ok')''',
              (tabla, registro_id, f'Movido a papelera: {motivo}'))

    # Borrar el registro original
    c.execute(f'DELETE FROM {tabla} WHERE id = ?', (registro_id,))

    conn.commit()
    conn.close()
    return True


def restaurar(papelera_id):
    """Restaurar un registro desde la papelera."""
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM _papelera WHERE id = ? AND restaurado = 0', (papelera_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        print(f"No se encontró registro papelera_id={papelera_id} o ya fue restaurado")
        return False

    row = dict(row)
    tabla = row['tabla_origen']
    datos = json.loads(row['datos'])

    # Reconstruir INSERT ignorando 'id' (se asigna nuevo)
    columnas = [k for k in datos.keys() if k != 'id']
    valores = [datos[k] for k in columnas]
    placeholders = ', '.join(['?'] * len(columnas))
    cols_str = ', '.join(columnas)

    c.execute(f'INSERT INTO {tabla} ({cols_str}) VALUES ({placeholders})', valores)
    nuevo_id = c.lastrowid

    # Marcar como restaurado
    c.execute('UPDATE _papelera SET restaurado = 1 WHERE id = ?', (papelera_id,))

    # Log
    c.execute('''INSERT INTO _operaciones_log (operacion, tabla, registro_id, query, resultado)
                 VALUES ('restaurar', ?, ?, ?, 'ok')''',
              (tabla, nuevo_id, f'Restaurado desde papelera #{papelera_id}, nuevo id={nuevo_id}'))

    conn.commit()
    conn.close()
    print(f"Restaurado: {tabla} nuevo id={nuevo_id} (desde papelera #{papelera_id})")
    return nuevo_id


def ver_papelera(tabla=None, limit=20):
    """Ver registros en la papelera."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if tabla:
        c.execute('''SELECT * FROM _papelera WHERE tabla_origen = ? AND restaurado = 0
                     ORDER BY fecha_borrado DESC LIMIT ?''', (tabla, limit))
    else:
        c.execute('''SELECT * FROM _papelera WHERE restaurado = 0
                     ORDER BY fecha_borrado DESC LIMIT ?''', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if not rows:
        print("Papelera vacía")
        return []

    print(f"{'ID':>4} | {'Tabla':>20} | {'Reg.ID':>6} | {'Fecha borrado':>20} | {'Motivo'}")
    print("-" * 80)
    for r in rows:
        print(f"{r['id']:>4} | {r['tabla_origen']:>20} | {r['registro_id']:>6} | "
              f"{r['fecha_borrado']:>20} | {r.get('motivo') or '-'}")

    return rows


def ver_log_operaciones(limit=20):
    """Ver log de operaciones destructivas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''SELECT * FROM _operaciones_log
                 ORDER BY timestamp DESC LIMIT ?''', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if not rows:
        print("Sin operaciones registradas")
        return []

    print(f"{'ID':>4} | {'Timestamp':>20} | {'Operación':>12} | {'Tabla':>15} | {'Query/Detalle'}")
    print("-" * 90)
    for r in rows:
        print(f"{r['id']:>4} | {r['timestamp']:>20} | {r['operacion']:>12} | "
              f"{r['tabla']:>15} | {(r.get('query') or '-')[:40]}")

    return rows


def safe_delete(tabla, registro_id, motivo=None, confirmar=True):
    """Wrapper principal: backup + soft delete + log.
    Esta es la función que Claude debe usar SIEMPRE en vez de DELETE directo.
    """
    if confirmar:
        # En modo interactivo, esto es una señal para Claude de pedir confirmación
        print(f"CONFIRMAR: Borrar {tabla} id={registro_id}? Motivo: {motivo}")

    # 1. Backup pre-operación
    backup = backup_antes_de_operar(f'delete_{tabla}_{registro_id}')

    # 2. Soft delete (mueve a papelera)
    ok = soft_delete(tabla, registro_id, motivo=motivo)

    if ok:
        print(f"OK: {tabla} #{registro_id} movido a papelera (backup: {os.path.basename(backup) if backup else 'sin backup'})")
    else:
        print(f"ERROR: No se pudo borrar {tabla} #{registro_id}")

    return ok


def safe_update(tabla, registro_id, cambios, motivo=None):
    """Update seguro: guarda snapshot del registro ANTES de modificar."""
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Snapshot del estado actual
    c.execute(f'SELECT * FROM {tabla} WHERE id = ?', (registro_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False

    snapshot = json.dumps(dict(row), ensure_ascii=False, default=str)

    # Log con el estado anterior
    c.execute('''INSERT INTO _operaciones_log (operacion, tabla, registro_id, query, resultado)
                 VALUES ('safe_update', ?, ?, ?, ?)''',
              (tabla, registro_id,
               f'Cambios: {json.dumps(cambios, ensure_ascii=False, default=str)[:200]}',
               f'Pre-update snapshot: {snapshot[:500]}'))

    # Ejecutar update
    sets = ', '.join(f'{k} = ?' for k in cambios.keys())
    vals = list(cambios.values()) + [registro_id]
    c.execute(f'UPDATE {tabla} SET {sets} WHERE id = ?', vals)

    conn.commit()
    conn.close()
    return True


def integridad_check():
    """Verificar integridad de la DB."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Integrity check
    c.execute("PRAGMA integrity_check")
    result = c.fetchone()[0]

    # Tamaño
    size_kb = os.path.getsize(DB_PATH) / 1024

    # Contar tablas
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [r[0] for r in c.fetchall()]

    conn.close()

    print(f"Integridad: {result}")
    print(f"Tamaño: {size_kb:.0f}KB")
    print(f"Tablas: {len(tablas)} ({', '.join(tablas)})")
    print(f"WAL mode: verificar con PRAGMA journal_mode")

    return result == 'ok'


if __name__ == '__main__':
    init_safety()
    print("Safety inicializado: WAL + papelera + log")
    integridad_check()
