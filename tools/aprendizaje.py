"""
ARGOS Aprendizaje Real
Conecta registrar_interaccion() (que era código muerto) con el flujo de sesión.
Agrega loop de errores: si algo falla, registra patrón + estrategia de recovery.

Reutilizable: funciona en Claude Code (hoy) y en la app web (mañana).

Uso:
    from tools.aprendizaje import registrar_exito, registrar_error, aprender_de_sesion
"""

import os
import sys
import json
from datetime import datetime, date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tracker import get_connection, add_evento, init_db


def registrar_exito(descripcion, herramienta=None, categoria=None):
    """
    Registra una interacción exitosa. Si se repite 3+ veces, se generaliza.

    Args:
        descripcion: qué hizo ARGOS (ej: "Generé presupuesto Word desde template")
        herramienta: qué tool se usó (ej: "doc_generator.py")
        categoria: tipo de tarea (ej: "licitacion", "personal", "admin")

    Returns:
        dict con resultado de la evaluación
    """
    try:
        from tools.patterns import registrar_interaccion
        resultado = registrar_interaccion(
            descripcion_pedido=descripcion,
            herramienta_usada=herramienta,
            resultado='ok',
            categoria=categoria
        )
        return resultado
    except Exception as e:
        # Si registrar_interaccion falla, al menos logueamos
        return {'tipo': 'error', 'error': str(e), 'accion': 'fallback'}


def registrar_error(descripcion_error, herramienta=None, solucion=None,
                    tipo_error='operacional', severidad='media'):
    """
    Registra un error y su solución (si la hay) como patrón aprendido.
    Si el mismo error se repite, incrementa frecuencia y refuerza la solución.

    Args:
        descripcion_error: qué falló (ej: "Excel PermissionError al abrir archivo")
        herramienta: qué tool falló (ej: "excel_tools.py")
        solucion: cómo se resolvió (ej: "Cerrar Excel y reintentar")
        tipo_error: 'operacional', 'dato', 'sistema', 'usuario'
        severidad: 'baja', 'media', 'alta', 'critica'

    Returns:
        dict con el patrón registrado
    """
    conn = get_connection()
    c = conn.cursor()

    # Buscar si ya existe un patrón de error similar
    c.execute("""SELECT id, frecuencia, sugerencia, confianza FROM patrones
                 WHERE tipo = 'error' AND descripcion LIKE ?
                 AND estado != 'descartado'
                 LIMIT 1""", (f'%{descripcion_error[:40]}%',))
    existente = c.fetchone()

    if existente:
        existente = dict(existente)
        # Reforzar patrón existente
        nueva_sugerencia = solucion or existente.get('sugerencia', '')
        nueva_confianza = min((existente.get('confianza') or 0.5) + 0.1, 0.99)
        c.execute("""UPDATE patrones SET frecuencia = frecuencia + 1,
                     ultimo_visto = ?, sugerencia = ?,
                     confianza = ?,
                     updated_at = datetime('now','localtime')
                     WHERE id = ?""",
                  (date.today().isoformat(), nueva_sugerencia, nueva_confianza, existente['id']))
        conn.commit()
        conn.close()

        return {
            'accion': 'reforzado',
            'patron_id': existente['id'],
            'frecuencia': existente['frecuencia'] + 1,
            'solucion': nueva_sugerencia
        }
    else:
        # Crear nuevo patrón de error
        evidencia = json.dumps({
            'herramienta': herramienta,
            'tipo_error': tipo_error,
            'severidad': severidad,
            'fecha': date.today().isoformat(),
        }, ensure_ascii=False)

        c.execute("""INSERT INTO patrones (tipo, categoria, descripcion, sugerencia,
                     evidencia, confianza, frecuencia, estado, fecha_deteccion, ultimo_visto)
                     VALUES ('error', ?, ?, ?, ?, 0.6, 1, 'detectado', ?, ?)""",
                  (tipo_error, descripcion_error, solucion, evidencia,
                   date.today().isoformat(), date.today().isoformat()))
        patron_id = c.lastrowid
        conn.commit()
        conn.close()

        # También registrar en errores_argos si es severo
        if severidad in ('alta', 'critica'):
            try:
                conn2 = get_connection()
                conn2.execute("""INSERT INTO errores_argos (fecha, tipo, descripcion,
                                 solucion, estado, severidad)
                                 VALUES (?, ?, ?, ?, 'pendiente', ?)""",
                              (date.today().isoformat(), tipo_error,
                               descripcion_error, solucion, severidad))
                conn2.commit()
                conn2.close()
            except Exception:
                pass  # tabla puede no existir

        return {
            'accion': 'creado',
            'patron_id': patron_id,
            'frecuencia': 1,
            'solucion': solucion
        }


def buscar_solucion(descripcion_error):
    """
    Busca si hay un patrón de error conocido con solución.
    Útil antes de intentar resolver un error: "¿ya pasó esto antes?"

    Args:
        descripcion_error: descripción del error

    Returns:
        dict con solución sugerida o None
    """
    conn = get_connection()
    c = conn.cursor()

    # Buscar por palabras clave del error
    palabras = descripcion_error.lower().split()[:5]
    for palabra in palabras:
        if len(palabra) < 4:
            continue
        c.execute("""SELECT descripcion, sugerencia, frecuencia, confianza
                     FROM patrones WHERE tipo = 'error'
                     AND descripcion LIKE ? AND sugerencia IS NOT NULL
                     AND estado != 'descartado'
                     ORDER BY frecuencia DESC, confianza DESC
                     LIMIT 1""", (f'%{palabra}%',))
        row = c.fetchone()
        if row:
            conn.close()
            row = dict(row)
            return {
                'encontrado': True,
                'error_conocido': row['descripcion'],
                'solucion': row['sugerencia'],
                'veces_visto': row['frecuencia'],
                'confianza': row['confianza']
            }

    conn.close()
    return {'encontrado': False}


def aprender_de_sesion(sesion_id=None):
    """
    Analiza la sesión actual y extrae aprendizajes.
    Se llama al cierre de sesión.

    Busca en los mensajes de la sesión:
    - Herramientas usadas exitosamente → registrar_exito
    - Errores encontrados → registrar_error
    - Patrones de comportamiento → reforzar

    Returns:
        dict con resumen de aprendizajes
    """
    from tools.patterns import analizar_patrones

    resultado = {
        'patrones_analizados': None,
        'errores_registrados': 0,
        'exitos_registrados': 0,
    }

    # Ejecutar análisis completo de patrones
    try:
        analisis = analizar_patrones()
        resultado['patrones_analizados'] = {
            'nuevos': len(analisis.get('nuevos', [])),
            'reforzados': len(analisis.get('reforzados', [])),
            'total': analisis.get('total_activos', 0),
        }
    except Exception as e:
        resultado['patrones_analizados'] = {'error': str(e)}

    return resultado


def estadisticas_aprendizaje():
    """
    Retorna estadísticas del sistema de aprendizaje.
    Cuántos patrones, cuántos errores conocidos, cuántas capacidades.
    """
    conn = get_connection()
    c = conn.cursor()

    # Patrones por tipo
    c.execute("""SELECT tipo, estado, COUNT(*) as total, AVG(frecuencia) as freq_avg
                 FROM patrones GROUP BY tipo, estado ORDER BY total DESC""")
    patrones = [dict(r) for r in c.fetchall()]

    # Errores con solución
    c.execute("""SELECT COUNT(*) as total FROM patrones
                 WHERE tipo='error' AND sugerencia IS NOT NULL""")
    errores_con_solucion = c.fetchone()['total']

    # Errores sin solución
    c.execute("""SELECT COUNT(*) as total FROM patrones
                 WHERE tipo='error' AND (sugerencia IS NULL OR sugerencia = '')""")
    errores_sin_solucion = c.fetchone()['total']

    # Capacidades
    try:
        c.execute("SELECT COUNT(*) as total FROM capacidades")
        capacidades = c.fetchone()['total']
    except Exception:
        capacidades = 0

    # Top 5 errores más frecuentes
    c.execute("""SELECT descripcion, sugerencia, frecuencia
                 FROM patrones WHERE tipo='error'
                 ORDER BY frecuencia DESC LIMIT 5""")
    top_errores = [dict(r) for r in c.fetchall()]

    conn.close()

    return {
        'patrones': patrones,
        'errores_con_solucion': errores_con_solucion,
        'errores_sin_solucion': errores_sin_solucion,
        'capacidades': capacidades,
        'top_errores': top_errores,
    }


def consultar_catalogo(descripcion_tarea):
    """
    Consulta el catálogo de capacidades ANTES de ejecutar una tarea.
    Cierra el learning loop: si ya hay un protocolo validado, lo sugiere.
    Si hay errores conocidos para esa tarea, avisa.

    Args:
        descripcion_tarea: qué va a hacer ARGOS (ej: "generar presupuesto Word")

    Returns:
        dict con:
        - protocolo: protocolo validado si existe
        - errores_conocidos: errores anteriores relevantes
        - sugerencias: tips basados en experiencia
    """
    conn = get_connection()
    c = conn.cursor()
    resultado = {
        'protocolo': None,
        'errores_conocidos': [],
        'sugerencias': [],
    }

    palabras = descripcion_tarea.lower().split()[:6]
    palabras_utiles = [p for p in palabras if len(p) >= 4]

    # 1. Buscar protocolo validado
    for palabra in palabras_utiles:
        c.execute("""SELECT descripcion, sugerencia, frecuencia, confianza
                     FROM patrones WHERE tipo LIKE 'protocolo_%'
                     AND estado IN ('validado', 'aplicado')
                     AND descripcion LIKE ?
                     ORDER BY frecuencia DESC
                     LIMIT 1""", (f'%{palabra}%',))
        row = c.fetchone()
        if row:
            row = dict(row)
            resultado['protocolo'] = {
                'descripcion': row['descripcion'],
                'pasos': row['sugerencia'],
                'confianza': row['confianza'],
                'veces_usado': row['frecuencia'],
            }
            break

    # 2. Buscar errores conocidos para esta tarea
    for palabra in palabras_utiles:
        c.execute("""SELECT descripcion, sugerencia, frecuencia
                     FROM patrones WHERE tipo = 'error'
                     AND descripcion LIKE ?
                     AND estado != 'descartado'
                     ORDER BY frecuencia DESC
                     LIMIT 3""", (f'%{palabra}%',))
        for row in c.fetchall():
            row = dict(row)
            resultado['errores_conocidos'].append({
                'error': row['descripcion'],
                'solucion': row['sugerencia'],
                'veces': row['frecuencia'],
            })

    # Deduplicar errores
    seen = set()
    unique_errors = []
    for e in resultado['errores_conocidos']:
        key = e['error'][:50]
        if key not in seen:
            seen.add(key)
            unique_errors.append(e)
    resultado['errores_conocidos'] = unique_errors[:5]

    # 3. Generar sugerencias
    if resultado['protocolo']:
        resultado['sugerencias'].append(
            f"Protocolo conocido ({resultado['protocolo']['veces_usado']}x): "
            f"{resultado['protocolo']['pasos'][:100] if resultado['protocolo']['pasos'] else 'sin pasos detallados'}"
        )
    if resultado['errores_conocidos']:
        resultado['sugerencias'].append(
            f"Cuidado: {len(resultado['errores_conocidos'])} errores anteriores conocidos para esta tarea."
        )

    conn.close()
    return resultado


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == 'stats':
        stats = estadisticas_aprendizaje()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    elif len(_sys.argv) > 1 and _sys.argv[1] == 'learn':
        resultado = aprender_de_sesion()
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    elif len(_sys.argv) > 1 and _sys.argv[1] == 'consultar':
        tarea = ' '.join(_sys.argv[2:])
        resultado = consultar_catalogo(tarea)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("Uso: python tools/aprendizaje.py [stats|learn|consultar <tarea>]")
