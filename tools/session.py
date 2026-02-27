"""
ARGOS Session Manager - Protocolo de sesión en código.
Garantiza que abrir/checkpoint/cerrar SIEMPRE se registre en DB.
No depende de que Claude "se acuerde" — es código, no instrucción.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.tracker import get_connection, add_evento, add_mensaje, init_db


def abrir_sesion(proyecto_id=None, notas=None):
    """Registra apertura de sesión. Devuelve sesion_id.
    Debe llamarse al inicio de cada conversación ARGOS.
    """
    # Verificar si ya hay una sesión abierta
    abierta = get_sesion_abierta()
    if abierta:
        print(f"WARN: Sesión #{abierta['id']} sigue abierta desde {abierta['fecha']} {abierta['hora_inicio']}")
        print("Cerrándola automáticamente antes de abrir nueva...")
        cerrar_sesion(abierta['id'], resumen='Cerrada automáticamente por nueva sesión')

    init_db()  # asegurar que las tablas existen
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now()

    c.execute('''INSERT INTO sesiones (fecha, hora_inicio, estado, proyecto_id, notas)
                 VALUES (?, ?, 'abierta', ?, ?)''',
              (ahora.strftime('%Y-%m-%d'), ahora.strftime('%H:%M:%S'),
               proyecto_id, notas))
    sesion_id = c.lastrowid
    conn.commit()
    conn.close()

    # Evento de apertura
    add_evento(
        fecha=ahora.strftime('%Y-%m-%d'),
        tipo='admin',
        descripcion=f'Sesión #{sesion_id} abierta',
        subtipo='sesion_abierta',
        hora=ahora.strftime('%H:%M'),
        proyecto_id=proyecto_id,
        fuente='session.py',
        notas=notas
    )

    print(f"Sesión #{sesion_id} abierta | {ahora.strftime('%Y-%m-%d %H:%M')}")
    return sesion_id


def checkpoint(sesion_id, notas=None, humor=None, energia=None, estres=None):
    """Registra punto intermedio con estado anímico opcional.
    Puede llamarse periódicamente durante la sesión.
    humor/energia/estres: 1-10 (opcional, para tracking rápido)
    """
    ahora = datetime.now()

    # Registrar como mensaje tipo checkpoint
    contenido = notas or 'Checkpoint'
    if humor or energia or estres:
        contenido += f' | humor={humor} energia={energia} estres={estres}'
    add_mensaje(sesion_id, 'system', contenido, tipo='checkpoint')

    # Si hay datos de bienestar, registrar en tabla bienestar
    if any([humor, energia, estres]):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO bienestar (fecha, persona_id, humor, energia, estres)
                     VALUES (?, 12, ?, ?, ?)''',
                  (ahora.strftime('%Y-%m-%d'), humor, energia, estres))
        conn.commit()
        conn.close()

    print(f"Checkpoint sesión #{sesion_id} | {ahora.strftime('%H:%M')}")
    return True


def cerrar_sesion(sesion_id, resumen=None, ejecutar_backup=True):
    """Cierra sesión: calcula duración real, registra cierre, ejecuta backup.
    Debe llamarse al final de cada conversación ARGOS.
    """
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now()

    # Obtener datos de la sesión
    c.execute('SELECT hora_inicio, fecha, proyecto_id FROM sesiones WHERE id = ?', (sesion_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        print(f"ERROR: Sesión #{sesion_id} no encontrada")
        return None

    row = dict(row)

    # Calcular duración real
    try:
        hora_inicio = datetime.strptime(f"{row['fecha']} {row['hora_inicio']}", '%Y-%m-%d %H:%M:%S')
        duracion_min = round((ahora - hora_inicio).total_seconds() / 60)
    except ValueError:
        duracion_min = 0

    # Contar mensajes de la sesión
    c.execute('SELECT COUNT(*) as total FROM mensajes WHERE sesion_id = ?', (sesion_id,))
    total_mensajes = c.fetchone()['total']

    # Cerrar sesión
    c.execute('''UPDATE sesiones SET hora_fin = ?, duracion_min = ?,
                 estado = 'cerrada', resumen = ? WHERE id = ?''',
              (ahora.strftime('%H:%M:%S'), duracion_min, resumen, sesion_id))
    conn.commit()
    conn.close()

    # Evento de cierre
    desc = f'Sesión #{sesion_id} cerrada ({duracion_min} min, {total_mensajes} mensajes)'
    if resumen:
        desc += f': {resumen}'
    add_evento(
        fecha=ahora.strftime('%Y-%m-%d'),
        tipo='admin',
        descripcion=desc,
        subtipo='sesion_cerrada',
        hora=ahora.strftime('%H:%M'),
        proyecto_id=row['proyecto_id'],
        fuente='session.py',
        duracion_min=duracion_min
    )

    # Backup
    if ejecutar_backup:
        try:
            from tools.backup import backup_db
            backup_db()
        except Exception as e:
            print(f"WARN: Backup falló: {e}")

    horas = duracion_min // 60
    mins = duracion_min % 60
    print(f"Sesión #{sesion_id} cerrada | {horas}h {mins}m | {total_mensajes} mensajes")

    return {
        'sesion_id': sesion_id,
        'duracion_min': duracion_min,
        'total_mensajes': total_mensajes,
        'hora_cierre': ahora.strftime('%H:%M')
    }


def get_sesion_abierta():
    """Busca si hay una sesión abierta. Devuelve dict o None."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT id, fecha, hora_inicio, proyecto_id, notas
                 FROM sesiones WHERE estado = 'abierta'
                 ORDER BY id DESC LIMIT 1""")
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def resumen_sesion(sesion_id):
    """Genera resumen de una sesión: duración, mensajes por tipo, temas."""
    conn = get_connection()
    c = conn.cursor()

    # Datos de sesión
    c.execute('SELECT * FROM sesiones WHERE id = ?', (sesion_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    sesion = dict(row)

    # Mensajes agrupados por tipo
    c.execute('''SELECT tipo, COUNT(*) as total, rol
                 FROM mensajes WHERE sesion_id = ?
                 GROUP BY tipo, rol''', (sesion_id,))
    msg_stats = [dict(r) for r in c.fetchall()]

    # Mensajes tipo decision o accion (los más importantes)
    c.execute('''SELECT timestamp, contenido FROM mensajes
                 WHERE sesion_id = ? AND tipo IN ('decision', 'accion')
                 ORDER BY timestamp ASC''', (sesion_id,))
    decisiones = [dict(r) for r in c.fetchall()]

    conn.close()

    return {
        'sesion': sesion,
        'mensajes_stats': msg_stats,
        'decisiones': decisiones
    }


def listar_sesiones(limit=10):
    """Lista las últimas N sesiones."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT id, fecha, hora_inicio, hora_fin, duracion_min, estado, resumen
                 FROM sesiones ORDER BY id DESC LIMIT ?''', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    print(f"{'ID':>4} | {'Fecha':>10} | {'Inicio':>8} | {'Fin':>8} | {'Min':>5} | {'Estado':>8} | Resumen")
    print("-" * 80)
    for r in rows:
        print(f"{r['id']:>4} | {r['fecha']:>10} | {r['hora_inicio']:>8} | "
              f"{r.get('hora_fin') or '-':>8} | {r.get('duracion_min') or '-':>5} | "
              f"{r['estado']:>8} | {(r.get('resumen') or '')[:30]}")

    return rows


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'abrir':
            abrir_sesion()
        elif cmd == 'cerrar':
            sesion = get_sesion_abierta()
            if sesion:
                cerrar_sesion(sesion['id'], resumen=' '.join(sys.argv[2:]) or None)
            else:
                print("No hay sesión abierta")
        elif cmd == 'status':
            sesion = get_sesion_abierta()
            if sesion:
                print(f"Sesión #{sesion['id']} abierta desde {sesion['fecha']} {sesion['hora_inicio']}")
            else:
                print("No hay sesión abierta")
        elif cmd == 'listar':
            listar_sesiones()
        else:
            print("Uso: python tools/session.py [abrir|cerrar|status|listar]")
    else:
        print("Uso: python tools/session.py [abrir|cerrar|status|listar]")
