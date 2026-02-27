"""
ARGOS Proactivo - Nudges inteligentes para estimular completar datos.
No es invasivo: máximo 3 nudges por apertura, priorizados por urgencia.

Uso:
    from tools.proactivo import generar_nudges
    nudges = generar_nudges()  # lista de strings priorizados
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.tracker import get_connection


def _dias_desde_ultimo(tabla, campo_fecha='fecha'):
    """Cuántos días desde el último registro en una tabla."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'SELECT MAX({campo_fecha}) as ultima FROM {tabla}')
    row = c.fetchone()
    conn.close()
    if not row or not row['ultima']:
        return 999  # nunca se registró
    try:
        ultima = datetime.strptime(row['ultima'], '%Y-%m-%d')
        return (datetime.now() - ultima).days
    except ValueError:
        return 999


def _contar_vencidos():
    """Cuántos seguimientos vencidos hay."""
    conn = get_connection()
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    c.execute("""SELECT COUNT(*) as total FROM seguimiento
                 WHERE estado NOT IN ('completado','cerrado','cancelado')
                 AND fecha_limite < ?""", (hoy,))
    total = c.fetchone()['total']
    conn.close()
    return total


def _reflexiones_sin_revisar():
    """Cuántas reflexiones sin revisar y la más reciente."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) as total FROM reflexiones WHERE revisado = 0""")
    total = c.fetchone()['total']
    if total > 0:
        c.execute("""SELECT tema, contenido, sentimiento, fecha
                     FROM reflexiones WHERE revisado = 0
                     ORDER BY fecha DESC LIMIT 1""")
        ultima = dict(c.fetchone())
    else:
        ultima = None
    conn.close()
    return total, ultima


def _metas_sin_actividad():
    """Metas activas que no tienen eventos recientes (últimos 7 días)."""
    conn = get_connection()
    c = conn.cursor()
    hace_7 = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    c.execute("""SELECT m.id, m.descripcion, m.area,
                 MAX(e.fecha) as ultimo_evento
                 FROM metas m
                 LEFT JOIN eventos e ON e.proyecto_id = m.proyecto_id AND e.fecha >= ?
                 WHERE m.estado = 'activa'
                 GROUP BY m.id
                 HAVING ultimo_evento IS NULL""", (hace_7,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def _areas_descuidadas():
    """Detectar áreas sin datos recientes."""
    areas = {}

    # Bienestar
    dias_bienestar = _dias_desde_ultimo('bienestar')
    if dias_bienestar >= 2:
        areas['bienestar'] = {
            'dias': dias_bienestar,
            'prioridad': min(dias_bienestar, 10),
            'nudge': f"Hace {dias_bienestar} día{'s' if dias_bienestar != 1 else ''} sin registrar bienestar. "
                     f"¿Cómo estás hoy? (humor/energía/estrés, rápido)"
        }

    # Nutrición
    dias_nutricion = _dias_desde_ultimo('nutricion')
    if dias_nutricion >= 3:
        if dias_nutricion >= 999:
            areas['nutricion'] = {
                'dias': dias_nutricion,
                'prioridad': 5,
                'nudge': "Nunca registramos comidas. ¿Querés arrancar hoy con algo simple? "
                         "Solo decime qué comiste y yo lo registro."
            }
        else:
            areas['nutricion'] = {
                'dias': dias_nutricion,
                'prioridad': min(dias_nutricion, 8),
                'nudge': f"Hace {dias_nutricion} días sin registrar comidas. "
                         f"¿Qué comiste hoy/ayer?"
            }

    # Salud
    dias_salud = _dias_desde_ultimo('salud')
    if dias_salud >= 14:
        areas['salud'] = {
            'dias': dias_salud,
            'prioridad': 4,
            'nudge': f"Hace {dias_salud} días sin nada en salud. "
                     f"¿Tenés algún turno pendiente o algo que registrar?"
        }

    return areas


def generar_nudges(max_nudges=3):
    """Genera lista priorizada de nudges para la apertura de sesión.
    Retorna lista de dicts: {tipo, prioridad, mensaje}
    """
    nudges = []

    # 1. Seguimientos vencidos (siempre importante)
    vencidos = _contar_vencidos()
    if vencidos > 0:
        nudges.append({
            'tipo': 'vencidos',
            'prioridad': 9,
            'mensaje': f"Tenés {vencidos} seguimiento{'s' if vencidos != 1 else ''} vencido{'s' if vencidos != 1 else ''}. "
                       f"¿Revisamos los más urgentes?"
        })

    # 2. Reflexiones sin revisar
    total_ref, ultima_ref = _reflexiones_sin_revisar()
    if total_ref > 0 and ultima_ref:
        emoji_sent = {'positivo': '+', 'negativo': '-', 'mixto': '~', 'neutro': '='}
        sent = emoji_sent.get(ultima_ref['sentimiento'], '?')
        nudges.append({
            'tipo': 'reflexion',
            'prioridad': 7,
            'mensaje': f"Tenés {total_ref} reflexion{'es' if total_ref != 1 else ''} sin retomar. "
                       f"Última: \"{ultima_ref['tema']}\" ({sent}) del {ultima_ref['fecha']}. "
                       f"¿Querés revisarla?"
        })

    # 3. Áreas descuidadas
    areas = _areas_descuidadas()
    for area_name, data in sorted(areas.items(), key=lambda x: -x[1]['prioridad']):
        nudges.append({
            'tipo': f'area_{area_name}',
            'prioridad': data['prioridad'],
            'mensaje': data['nudge']
        })

    # 4. Metas sin actividad
    metas_inactivas = _metas_sin_actividad()
    if metas_inactivas:
        nombres = ', '.join(m['descripcion'][:30] for m in metas_inactivas[:3])
        nudges.append({
            'tipo': 'metas',
            'prioridad': 5,
            'mensaje': f"Metas activas sin movimiento en 7 días: {nombres}. "
                       f"¿Querés revisar alguna?"
        })

    # Ordenar por prioridad (mayor primero) y limitar
    nudges.sort(key=lambda x: -x['prioridad'])
    return nudges[:max_nudges]


def mostrar_nudges(max_nudges=3):
    """Muestra nudges en formato legible. Para usar en apertura de sesión."""
    nudges = generar_nudges(max_nudges)
    if not nudges:
        print("Todo al día - sin nudges pendientes.")
        return nudges

    print(f"\n--- ARGOS te sugiere ({len(nudges)} tema{'s' if len(nudges) != 1 else ''}) ---")
    for i, n in enumerate(nudges, 1):
        print(f"  {i}. [{n['tipo']}] {n['mensaje']}")
    print("---")
    return nudges


def extraer_reflexion(texto_libre):
    """Extrae datos estructurados de texto libre para crear una reflexión.
    Analiza el texto y sugiere tema, sentimiento, intensidad, área.
    Retorna dict con los campos sugeridos.

    Esto es una extracción heurística simple. La versión con Claude API
    será mucho mejor.
    """
    texto = texto_libre.lower()

    # Detectar sentimiento por palabras clave
    palabras_negativas = ['podrido', 'frustrad', 'cansad', 'harto', 'bronca', 'enojad',
                          'preocupad', 'angustia', 'miedo', 'ansiedad', 'mal', 'peor',
                          'no aguanto', 'no puedo', 'decepcion', 'triste', 'duel',
                          'no dorm', 'agotad', 'estresad', 'quemad', 'bajón',
                          'no tengo energ', 'sin energ', 'irritad']
    palabras_positivas = ['bien', 'content', 'feliz', 'alegr', 'logr', 'avanz',
                          'orgullos', 'satisf', 'mejor', 'genial', 'bueno', 'excelente',
                          'productiv', 'motivad', 'tranquil', 'relajad', 'entusiasm']

    neg = sum(1 for p in palabras_negativas if p in texto)
    pos = sum(1 for p in palabras_positivas if p in texto)

    if neg > pos:
        sentimiento = 'negativo'
        intensidad = min(neg + 2, 5)
    elif pos > neg:
        sentimiento = 'positivo'
        intensidad = min(pos + 2, 5)
    elif neg > 0 and pos > 0:
        sentimiento = 'mixto'
        intensidad = 3
    else:
        sentimiento = 'neutro'
        intensidad = 2

    # Detectar área
    area = 'personal'
    if any(w in texto for w in ['trabajo', 'sbd', 'licitacion', 'laboral', 'jefe', 'oficina',
                                 'sueldo', 'salario', 'posadas', 'marcelo', 'richard']):
        area = 'laboral'
    elif any(w in texto for w in ['salud', 'medico', 'turno', 'dolor', 'duel', 'gym', 'ejercicio',
                                   'dormir', 'no dorm', 'sueño', 'peso', 'cabeza', 'fiebre',
                                   'pastilla', 'remedio']):
        area = 'salud'
    elif any(w in texto for w in ['familia', 'hijo', 'hija', 'mujer', 'pareja', 'mama',
                                   'papa', 'hermano']):
        area = 'familia'
    elif any(w in texto for w in ['aicontrol', 'argos', 'proyecto', 'bot', 'telegram']):
        area = 'proyecto'

    # Extraer tags de las palabras clave encontradas
    tags = []
    if area != 'personal':
        tags.append(area)
    if sentimiento != 'neutro':
        tags.append(sentimiento)

    return {
        'contenido': texto_libre.strip(),
        'sentimiento': sentimiento,
        'intensidad': intensidad,
        'area': area,
        'tags': ','.join(tags) if tags else None
    }


if __name__ == '__main__':
    mostrar_nudges()
