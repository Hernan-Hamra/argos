"""
Detector de Coherencia Intención / Comportamiento.
Cruza metas declaradas (tabla metas) con actividad real (eventos + seguimiento).
Genera un reporte tipo "espejo" que muestra alineación sin juzgar.
"""

import os
import sys
from datetime import date, datetime, timedelta

# Path setup
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TOOLS_DIR, '..'))

from tools.tracker import (
    get_connection, get_metas, get_eventos_periodo,
    get_horas_resumen, get_pendientes, add_meta, init_db
)


def _horas_proyecto_periodo(proyecto_id, dias=30):
    """Calcula horas reales dedicadas a un proyecto en los últimos N días."""
    conn = get_connection()
    c = conn.cursor()
    fecha_desde = (date.today() - timedelta(days=dias)).isoformat()
    fecha_hasta = date.today().isoformat()

    c.execute('''SELECT SUM(duracion_min) as total_min, COUNT(*) as sesiones,
                 MAX(fecha) as ultima_actividad
                 FROM eventos
                 WHERE proyecto_id = ?
                 AND fecha BETWEEN ? AND ?
                 AND duracion_min IS NOT NULL AND duracion_min > 0''',
              (proyecto_id, fecha_desde, fecha_hasta))
    row = dict(c.fetchone())
    conn.close()

    total_min = row['total_min'] or 0
    semanas = max(dias / 7, 1)
    return {
        'horas_totales': round(total_min / 60, 1),
        'horas_semana': round(total_min / 60 / semanas, 1),
        'sesiones': row['sesiones'] or 0,
        'ultima_actividad': row['ultima_actividad']
    }


def _eventos_area_periodo(area, dias=30):
    """Calcula actividad por área (tipo de evento) cuando no hay proyecto_id."""
    conn = get_connection()
    c = conn.cursor()
    fecha_desde = (date.today() - timedelta(days=dias)).isoformat()
    fecha_hasta = date.today().isoformat()

    # Mapeo área -> tipo de evento
    tipo_map = {
        'laboral': 'laboral',
        'personal': 'personal',
        'salud': 'salud',
        'desarrollo': 'argos',
        'familia': 'familia'
    }
    tipo = tipo_map.get(area, area)

    c.execute('''SELECT SUM(duracion_min) as total_min, COUNT(*) as sesiones,
                 MAX(fecha) as ultima_actividad
                 FROM eventos
                 WHERE tipo = ?
                 AND fecha BETWEEN ? AND ?
                 AND duracion_min IS NOT NULL AND duracion_min > 0''',
              (tipo, fecha_desde, fecha_hasta))
    row = dict(c.fetchone())
    conn.close()

    total_min = row['total_min'] or 0
    semanas = max(dias / 7, 1)
    return {
        'horas_totales': round(total_min / 60, 1),
        'horas_semana': round(total_min / 60 / semanas, 1),
        'sesiones': row['sesiones'] or 0,
        'ultima_actividad': row['ultima_actividad']
    }


def _pendientes_proyecto(proyecto_id):
    """Cuenta pendientes abiertos y vencidos de un proyecto."""
    pendientes = get_pendientes(incluir_vencidos=True)
    del_proyecto = [p for p in pendientes if dict(p).get('proyecto_id') == proyecto_id]
    abiertos = len(del_proyecto)
    vencidos = sum(1 for p in del_proyecto
                   if dict(p).get('estado') == 'vencido'
                   or (dict(p).get('fecha_limite') and dict(p)['fecha_limite'] < date.today().isoformat()))
    return {'abiertos': abiertos, 'vencidos': vencidos}


def _dias_sin_actividad(ultima_actividad):
    """Calcula días desde la última actividad."""
    if not ultima_actividad:
        return 999  # Nunca hubo actividad
    try:
        ultima = datetime.strptime(ultima_actividad, '%Y-%m-%d').date()
        return (date.today() - ultima).days
    except (ValueError, TypeError):
        return 999


def medir_coherencia_meta(meta, dias=30):
    """
    Cruza una meta con la actividad real de los últimos N días.

    Args:
        meta: dict con datos de la meta (de get_metas())
        dias: período de análisis

    Returns: dict con intención, comportamiento, coherencia, señal, espejo
    """
    # Obtener actividad real
    if meta.get('proyecto_id'):
        actividad = _horas_proyecto_periodo(meta['proyecto_id'], dias)
        pendientes = _pendientes_proyecto(meta['proyecto_id'])
    else:
        actividad = _eventos_area_periodo(meta['area'], dias)
        pendientes = {'abiertos': 0, 'vencidos': 0}

    dias_inactivo = _dias_sin_actividad(actividad['ultima_actividad'])

    # Calcular coherencia
    if meta.get('horas_semana_meta') and meta['horas_semana_meta'] > 0:
        coherencia_base = min(actividad['horas_semana'] / meta['horas_semana_meta'], 1.0)
    elif actividad['sesiones'] > 0:
        # Sin horas meta: coherencia basada en actividad mínima (al menos 1 sesión/semana)
        semanas = max(dias / 7, 1)
        coherencia_base = min(actividad['sesiones'] / semanas, 1.0)
    else:
        coherencia_base = 0.0

    # Penalización por pendientes vencidos
    penalizacion = min(pendientes['vencidos'] * 0.1, 0.3)
    coherencia = max(round(coherencia_base - penalizacion, 2), 0.0)

    # Clasificar señal
    if coherencia >= 0.7:
        senal = 'on_track'
    elif coherencia >= 0.3:
        senal = 'en_riesgo'
    elif dias_inactivo > 30 and coherencia < 0.1:
        senal = 'abandonada'
    else:
        senal = 'desalineada'

    # Calcular días restantes si hay fecha_objetivo
    dias_restantes = None
    if meta.get('fecha_objetivo'):
        try:
            obj = datetime.strptime(meta['fecha_objetivo'], '%Y-%m-%d').date()
            dias_restantes = (obj - date.today()).days
        except (ValueError, TypeError):
            pass

    # Generar texto espejo (descriptivo, sin juicio)
    espejo = _generar_espejo(meta, actividad, pendientes, dias_inactivo, coherencia, senal, dias_restantes)

    return {
        'meta': {
            'id': meta['id'],
            'descripcion': meta['descripcion'],
            'area': meta['area'],
            'proyecto': meta.get('proyecto_nombre') or meta['area'],
            'prioridad': meta['prioridad']
        },
        'intencion': {
            'horas_semana_meta': meta.get('horas_semana_meta'),
            'prioridad': meta['prioridad'],
            'fecha_objetivo': meta.get('fecha_objetivo'),
            'dias_restantes': dias_restantes
        },
        'comportamiento': {
            'horas_semana': actividad['horas_semana'],
            'horas_totales': actividad['horas_totales'],
            'sesiones': actividad['sesiones'],
            'pendientes_abiertos': pendientes['abiertos'],
            'pendientes_vencidos': pendientes['vencidos'],
            'dias_sin_actividad': dias_inactivo,
            'ultima_actividad': actividad['ultima_actividad']
        },
        'coherencia': coherencia,
        'senal': senal,
        'espejo': espejo
    }


def _generar_espejo(meta, actividad, pendientes, dias_inactivo, coherencia, senal, dias_restantes):
    """Genera texto descriptivo sin juicio."""
    nombre = meta.get('proyecto_nombre') or meta['descripcion']
    lineas = []

    # Línea principal: horas
    hs_meta = meta.get('horas_semana_meta')
    hs_real = actividad['horas_semana']
    if hs_meta:
        lineas.append(f"{hs_real}hs/sem (meta: {hs_meta}hs)")
    else:
        lineas.append(f"{actividad['sesiones']} sesiones en {30} dias")

    # Inactividad
    if dias_inactivo > 7:
        if actividad['ultima_actividad']:
            lineas.append(f"{dias_inactivo} dias sin actividad (ultima: {actividad['ultima_actividad']})")
        else:
            lineas.append("Sin actividad registrada")

    # Pendientes
    if pendientes['vencidos'] > 0:
        lineas.append(f"{pendientes['vencidos']} pendientes vencidos")
    elif pendientes['abiertos'] > 0:
        lineas.append(f"{pendientes['abiertos']} pendientes abiertos")

    # Deadline
    if dias_restantes is not None:
        if dias_restantes < 0:
            lineas.append(f"Fecha objetivo vencida hace {abs(dias_restantes)} dias")
        elif dias_restantes < 30:
            lineas.append(f"Fecha objetivo en {dias_restantes} dias")

    return ' | '.join(lineas)


def reporte_coherencia(dias=30, imprimir=True):
    """
    Genera reporte completo de todas las metas activas.
    Muestra coherencia entre intención y comportamiento.

    Args:
        dias: período de análisis (default 30)
        imprimir: si True, imprime el reporte; si False, retorna datos

    Returns: lista de resultados de medir_coherencia_meta
    """
    import io
    if imprimir:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    metas = get_metas(solo_activas=True)
    if not metas:
        if imprimir:
            print("Sin metas registradas. Usar add_meta() para declarar intenciones.")
        return []

    resultados = []
    for meta in metas:
        resultado = medir_coherencia_meta(meta, dias)
        resultados.append(resultado)

    if not imprimir:
        return resultados

    # Agrupar por señal
    on_track = [r for r in resultados if r['senal'] == 'on_track']
    en_riesgo = [r for r in resultados if r['senal'] == 'en_riesgo']
    desalineadas = [r for r in resultados if r['senal'] == 'desalineada']
    abandonadas = [r for r in resultados if r['senal'] == 'abandonada']

    hoy = date.today().strftime('%d/%m/%Y')
    print(f"\n{'='*60}")
    print(f"  ESPEJO | Intencion vs Comportamiento")
    print(f"  Periodo: ultimos {dias} dias | {hoy}")
    print(f"{'='*60}")

    if on_track:
        print(f"\n  ON TRACK:")
        for r in on_track:
            m = r['meta']
            c = r['comportamiento']
            hs = r['intencion']['horas_semana_meta']
            hs_str = f"{c['horas_semana']}hs/sem (meta: {hs}hs)" if hs else f"{c['sesiones']} sesiones"
            print(f"    [OK] {m['proyecto']:25s} {hs_str:25s} coherencia {r['coherencia']}")

    if en_riesgo:
        print(f"\n  EN RIESGO:")
        for r in en_riesgo:
            m = r['meta']
            c = r['comportamiento']
            hs = r['intencion']['horas_semana_meta']
            hs_str = f"{c['horas_semana']}hs/sem (meta: {hs}hs)" if hs else f"{c['sesiones']} sesiones"
            print(f"    [~~] {m['proyecto']:25s} {hs_str:25s} coherencia {r['coherencia']}")
            if c['dias_sin_actividad'] > 7:
                print(f"         {c['dias_sin_actividad']} dias sin actividad")

    if desalineadas:
        print(f"\n  DESALINEADA:")
        for r in desalineadas:
            m = r['meta']
            c = r['comportamiento']
            hs = r['intencion']['horas_semana_meta']
            hs_str = f"{c['horas_semana']}hs/sem (meta: {hs}hs)" if hs else f"{c['sesiones']} sesiones"
            print(f"    [XX] {m['proyecto']:25s} {hs_str:25s} coherencia {r['coherencia']}")
            if c['ultima_actividad']:
                print(f"         Ultima actividad: {c['ultima_actividad']} ({c['dias_sin_actividad']} dias)")
            else:
                print(f"         Sin actividad registrada")
            if c['pendientes_abiertos'] > 0:
                print(f"         Pendientes abiertos: {c['pendientes_abiertos']}")

    if abandonadas:
        print(f"\n  ABANDONADA:")
        for r in abandonadas:
            m = r['meta']
            c = r['comportamiento']
            hs = r['intencion']['horas_semana_meta']
            hs_str = f"{c['horas_semana']}hs/sem (meta: {hs}hs)" if hs else "0 sesiones"
            print(f"    [!!] {m['proyecto']:25s} {hs_str:25s} coherencia {r['coherencia']}")
            if c['ultima_actividad']:
                print(f"         Ultima actividad: {c['ultima_actividad']} ({c['dias_sin_actividad']} dias)")
            else:
                print(f"         Sin actividad registrada en el periodo")

    print(f"\n{'='*60}")

    # Resumen
    total = len(resultados)
    coherencia_promedio = sum(r['coherencia'] for r in resultados) / total if total > 0 else 0
    print(f"  {total} metas activas | coherencia promedio: {coherencia_promedio:.2f}")
    print(f"  {len(on_track)} on track | {len(en_riesgo)} en riesgo | {len(desalineadas)} desalineadas | {len(abandonadas)} abandonadas")
    print(f"{'='*60}\n")

    return resultados


def seed_metas_hernan():
    """Poblar metas actuales de Hernan basadas en perfil y seguimiento."""
    init_db()

    # Verificar si ya hay metas
    existentes = get_metas(solo_activas=True)
    if existentes:
        print(f"Ya hay {len(existentes)} metas activas. No se hace seed.")
        return existentes

    metas = [
        {
            'descripcion': 'Hacer crecer AiControl como negocio propio',
            'area': 'desarrollo',
            'proyecto_id': 4,  # AiControl
            'prioridad': 'alta',
            'horas_semana_meta': 5,
            'indicador': 'horas',
            'notas': 'Seguridad electronica + ARGOS + desarrollos futuros'
        },
        {
            'descripcion': 'Salir de SBD - conseguir trabajo en tech',
            'area': 'laboral',
            'proyecto_id': 6,  # Busqueda laboral
            'prioridad': 'alta',
            'horas_semana_meta': 3,
            'indicador': 'horas',
            'notas': 'CV, LinkedIn, postulaciones, networking'
        },
        {
            'descripcion': 'Evolucionar ARGOS como producto vendible',
            'area': 'desarrollo',
            'proyecto_id': 7,  # ARGOS
            'prioridad': 'alta',
            'horas_semana_meta': 5,
            'indicador': 'horas',
            'notas': 'Tools, marketplace, comunidad, producto'
        },
        {
            'descripcion': 'Cumplir con Hospital Posadas',
            'area': 'laboral',
            'proyecto_id': 1,  # Posadas
            'prioridad': 'alta',
            'horas_semana_meta': 10,
            'indicador': 'horas',
            'notas': 'Trabajo principal actual. Informes, gestion, visitas'
        },
        {
            'descripcion': 'Recomposicion corporal - plan nutricional',
            'area': 'salud',
            'proyecto_id': None,
            'prioridad': 'media',
            'horas_semana_meta': 3,
            'indicador': 'horas',
            'notas': 'Entrenamiento + nutricion + registro de comidas'
        },
        {
            'descripcion': 'Organizar vida digital',
            'area': 'personal',
            'proyecto_id': None,
            'prioridad': 'baja',
            'horas_semana_meta': 1,
            'indicador': 'horas',
            'notas': 'OneDrive, archivos, backups, passwords'
        },
    ]

    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Seeding metas de Hernan...")
    for m in metas:
        mid = add_meta(**m)
        print(f"  [+] Meta {mid}: {m['descripcion']} ({m['area']}, {m['horas_semana_meta']}hs/sem)")

    print(f"\n{len(metas)} metas registradas.")
    return get_metas()


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == 'seed':
        seed_metas_hernan()
    else:
        reporte_coherencia()
