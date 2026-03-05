"""
ARGOS Resumen Periódico
Genera reportes de bienestar, coherencia y productividad por semana o mes.

Uso:
    from tools.resumen_periodico import resumen_semanal, resumen_mensual
"""

import os
import sys
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tracker import get_connection


def _promedios_bienestar(fecha_desde, fecha_hasta):
    """Calcula promedios de bienestar en un período."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT
        COUNT(*) as registros,
        AVG(humor) as humor_avg,
        AVG(energia) as energia_avg,
        AVG(estres) as estres_avg,
        AVG(horas_sueno) as sueno_avg,
        AVG(ejercicio_min) as ejercicio_avg,
        MIN(humor) as humor_min,
        MAX(humor) as humor_max,
        MIN(estres) as estres_min,
        MAX(estres) as estres_max,
        SUM(ejercicio_min) as ejercicio_total
        FROM bienestar WHERE fecha BETWEEN ? AND ?""",
              (fecha_desde, fecha_hasta))
    row = c.fetchone()
    conn.close()
    if not row or row['registros'] == 0:
        return None
    return dict(row)


def _actividad_periodo(fecha_desde, fecha_hasta):
    """Cuenta eventos, seguimientos, sesiones en un período."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as n FROM eventos WHERE fecha BETWEEN ? AND ?",
              (fecha_desde, fecha_hasta))
    eventos = c.fetchone()['n']

    c.execute("""SELECT COUNT(*) as n FROM seguimiento
                 WHERE completed_at IS NOT NULL
                 AND date(completed_at) BETWEEN ? AND ?""",
              (fecha_desde, fecha_hasta))
    completados = c.fetchone()['n']

    c.execute("SELECT COUNT(*) as n FROM sesiones WHERE fecha BETWEEN ? AND ?",
              (fecha_desde, fecha_hasta))
    sesiones = c.fetchone()['n']

    c.execute("""SELECT COUNT(*) as n FROM mensajes
                 WHERE date(timestamp) BETWEEN ? AND ?
                 AND rol='user'""",
              (fecha_desde, fecha_hasta))
    mensajes = c.fetchone()['n']

    c.execute("""SELECT COUNT(*) as n FROM seguimiento
                 WHERE estado NOT IN ('completado','cerrado','cancelado')
                 AND fecha_limite < ?""",
              (fecha_hasta,))
    vencidos = c.fetchone()['n']

    conn.close()
    return {
        'eventos': eventos,
        'seguimientos_completados': completados,
        'sesiones': sesiones,
        'mensajes_usuario': mensajes,
        'seguimientos_vencidos': vencidos,
    }


def _rutinas_periodo(fecha_desde, fecha_hasta):
    """Estadísticas de rutinas en el período."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""SELECT nombre, veces_ejecutada, veces_omitida,
                     racha_dias, max_racha
                     FROM rutinas WHERE estado='activa'""")
        rutinas = [dict(r) for r in c.fetchall()]
    except Exception:
        rutinas = []
    conn.close()
    return rutinas


def resumen_semanal(fecha_fin=None):
    """
    Genera resumen de la última semana.

    Args:
        fecha_fin: fecha final (default: hoy)

    Returns:
        dict con bienestar, actividad, rutinas, insights
    """
    if fecha_fin is None:
        fecha_fin = date.today()
    elif isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    fecha_inicio = fecha_fin - timedelta(days=7)
    desde = fecha_inicio.isoformat()
    hasta = fecha_fin.isoformat()

    bienestar = _promedios_bienestar(desde, hasta)
    actividad = _actividad_periodo(desde, hasta)
    rutinas = _rutinas_periodo(desde, hasta)

    # Generar insights automáticos
    insights = []
    if bienestar:
        if bienestar['estres_avg'] and bienestar['estres_avg'] > 6:
            insights.append("Estrés alto esta semana. Revisar carga laboral.")
        if bienestar['sueno_avg'] and bienestar['sueno_avg'] < 6:
            insights.append("Promedio de sueño bajo (<6hs). Priorizar descanso.")
        if bienestar['ejercicio_total'] and bienestar['ejercicio_total'] < 90:
            insights.append("Poco ejercicio esta semana (<90 min total).")
        if bienestar['humor_avg'] and bienestar['humor_avg'] >= 7:
            insights.append("Buen humor promedio. Semana positiva.")
        if bienestar['registros'] < 3:
            insights.append(f"Solo {bienestar['registros']} registros de bienestar. Registrar más seguido.")

    if actividad['seguimientos_vencidos'] > 3:
        insights.append(f"{actividad['seguimientos_vencidos']} seguimientos vencidos. Revisar.")

    return {
        'periodo': f"{desde} a {hasta}",
        'tipo': 'semanal',
        'bienestar': bienestar,
        'actividad': actividad,
        'rutinas': rutinas,
        'insights': insights,
    }


def resumen_mensual(mes=None, anio=None):
    """
    Genera resumen del mes.

    Args:
        mes: número de mes (default: mes actual)
        anio: año (default: año actual)

    Returns:
        dict con bienestar, actividad, tendencias, insights
    """
    hoy = date.today()
    if mes is None:
        mes = hoy.month
    if anio is None:
        anio = hoy.year

    fecha_inicio = date(anio, mes, 1)
    if mes == 12:
        fecha_fin = date(anio + 1, 1, 1) - timedelta(days=1)
    else:
        fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)

    desde = fecha_inicio.isoformat()
    hasta = fecha_fin.isoformat()

    bienestar = _promedios_bienestar(desde, hasta)
    actividad = _actividad_periodo(desde, hasta)
    rutinas = _rutinas_periodo(desde, hasta)

    # Comparar con mes anterior
    mes_ant_fin = fecha_inicio - timedelta(days=1)
    mes_ant_inicio = date(mes_ant_fin.year, mes_ant_fin.month, 1)
    bienestar_anterior = _promedios_bienestar(
        mes_ant_inicio.isoformat(), mes_ant_fin.isoformat()
    )

    # Tendencias
    tendencias = {}
    if bienestar and bienestar_anterior:
        for campo in ['humor_avg', 'energia_avg', 'estres_avg', 'sueno_avg']:
            actual = bienestar.get(campo)
            anterior = bienestar_anterior.get(campo)
            if actual and anterior:
                diff = actual - anterior
                if abs(diff) > 0.5:
                    tendencias[campo] = 'subió' if diff > 0 else 'bajó'
                else:
                    tendencias[campo] = 'estable'

    # Insights mensuales
    insights = []
    if bienestar and bienestar['registros'] > 0:
        dias_mes = (fecha_fin - fecha_inicio).days + 1
        cobertura = bienestar['registros'] / dias_mes * 100
        insights.append(f"Cobertura bienestar: {cobertura:.0f}% ({bienestar['registros']}/{dias_mes} días)")

    for campo, tendencia in tendencias.items():
        nombre = campo.replace('_avg', '').replace('_', ' ')
        if tendencia != 'estable':
            insights.append(f"{nombre} {tendencia} vs mes anterior")

    return {
        'periodo': f"{anio}-{mes:02d}",
        'tipo': 'mensual',
        'bienestar': bienestar,
        'actividad': actividad,
        'rutinas': rutinas,
        'tendencias': tendencias,
        'comparacion_anterior': bienestar_anterior,
        'insights': insights,
    }


def formato_resumen(resumen):
    """Formatea resumen como texto legible."""
    lines = []
    lines.append(f"{'='*50}")
    lines.append(f"  RESUMEN {resumen['tipo'].upper()} — {resumen['periodo']}")
    lines.append(f"{'='*50}")

    b = resumen.get('bienestar')
    if b and b.get('registros', 0) > 0:
        lines.append(f"\n  Bienestar ({b['registros']} registros):")
        if b.get('humor_avg'):
            lines.append(f"    Humor:    {b['humor_avg']:.1f}/10 (min {b['humor_min']}, max {b['humor_max']})")
        if b.get('energia_avg'):
            lines.append(f"    Energía:  {b['energia_avg']:.1f}/10")
        if b.get('estres_avg'):
            lines.append(f"    Estrés:   {b['estres_avg']:.1f}/10 (min {b['estres_min']}, max {b['estres_max']})")
        if b.get('sueno_avg'):
            lines.append(f"    Sueño:    {b['sueno_avg']:.1f}hs promedio")
        if b.get('ejercicio_total'):
            lines.append(f"    Ejercicio: {b['ejercicio_total']} min total")
    else:
        lines.append("\n  Sin registros de bienestar en este período.")

    a = resumen.get('actividad', {})
    lines.append(f"\n  Actividad:")
    lines.append(f"    Eventos:     {a.get('eventos', 0)}")
    lines.append(f"    Completados: {a.get('seguimientos_completados', 0)}")
    lines.append(f"    Sesiones:    {a.get('sesiones', 0)}")
    lines.append(f"    Mensajes:    {a.get('mensajes_usuario', 0)}")
    if a.get('seguimientos_vencidos', 0) > 0:
        lines.append(f"    Vencidos:    {a['seguimientos_vencidos']}")

    if resumen.get('insights'):
        lines.append(f"\n  Insights:")
        for i in resumen['insights']:
            lines.append(f"    - {i}")

    lines.append(f"{'='*50}")
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == 'mensual':
        r = resumen_mensual()
    else:
        r = resumen_semanal()
    print(formato_resumen(r))
