"""
ARGOS Alertas Automáticas
Motor de alertas que detecta situaciones urgentes y las presenta al usuario.
BUG-01: que NUNCA más se olvide un seguimiento vencido.

Tipos de alerta:
  - ROJA: seguimientos vencidos, fechas límite hoy
  - AMARILLA: seguimientos que vencen mañana, prioridad crítica
  - INFO: recordatorios, agenda del día

Reutilizable: funciona en Claude Code (hoy) y en la app web (mañana).

Uso:
    from tools.alertas import generar_alertas, alertas_criticas
"""

import os
import sys
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tracker import get_connection, get_pendientes, get_agenda_dia


def _seguimientos_vencidos():
    """Obtiene seguimientos vencidos con días de atraso."""
    hoy = date.today().isoformat()
    pendientes = get_pendientes(incluir_vencidos=True)
    vencidos = []
    for p in pendientes:
        p = dict(p)
        if p.get('fecha_limite') and p['fecha_limite'] < hoy:
            fecha_lim = datetime.strptime(p['fecha_limite'], '%Y-%m-%d').date()
            p['dias_vencido'] = (date.today() - fecha_lim).days
            p['nivel'] = 'roja'
            vencidos.append(p)
    # Ordenar por más vencidos primero
    vencidos.sort(key=lambda x: -x['dias_vencido'])
    return vencidos


def _seguimientos_por_vencer(dias=2):
    """Seguimientos que vencen en los próximos N días."""
    hoy = date.today()
    limite = (hoy + timedelta(days=dias)).isoformat()
    pendientes = get_pendientes(incluir_vencidos=False)
    por_vencer = []
    for p in pendientes:
        p = dict(p)
        fl = p.get('fecha_limite')
        if fl and hoy.isoformat() <= fl <= limite:
            fecha_lim = datetime.strptime(fl, '%Y-%m-%d').date()
            p['dias_restantes'] = (fecha_lim - hoy).days
            p['nivel'] = 'amarilla' if p['dias_restantes'] <= 1 else 'info'
            por_vencer.append(p)
    por_vencer.sort(key=lambda x: x['dias_restantes'])
    return por_vencer


def _seguimientos_criticos():
    """Seguimientos de prioridad crítica sin importar fecha."""
    pendientes = get_pendientes(incluir_vencidos=True)
    criticos = []
    for p in pendientes:
        p = dict(p)
        if p.get('prioridad') == 'critica' and p.get('estado') not in ('completado', 'cerrado', 'cancelado'):
            p['nivel'] = 'amarilla'
            criticos.append(p)
    return criticos


def generar_alertas():
    """
    Genera todas las alertas activas, priorizadas por urgencia.

    Returns:
        dict con:
        - rojas: list (vencidos, DEBEN atenderse)
        - amarillas: list (próximos a vencer o prioridad crítica)
        - info: list (recordatorios, agenda)
        - total: int
        - resumen: str (texto resumido para mostrar)
    """
    rojas = []
    amarillas = []
    info = []

    # 1. Seguimientos vencidos → ROJA
    vencidos = _seguimientos_vencidos()
    for v in vencidos:
        rojas.append({
            'tipo': 'vencido',
            'nivel': 'roja',
            'dias': v['dias_vencido'],
            'accion': v['accion'],
            'proyecto': v.get('proyecto', ''),
            'persona': v.get('persona', ''),
            'id': v['id'],
        })

    # 2. Seguimientos por vencer → AMARILLA
    por_vencer = _seguimientos_por_vencer(dias=2)
    for pv in por_vencer:
        nivel = pv['nivel']
        alerta = {
            'tipo': 'por_vencer',
            'nivel': nivel,
            'dias': pv['dias_restantes'],
            'accion': pv['accion'],
            'proyecto': pv.get('proyecto', ''),
            'persona': pv.get('persona', ''),
            'id': pv['id'],
        }
        if nivel == 'amarilla':
            amarillas.append(alerta)
        else:
            info.append(alerta)

    # 3. Agenda del día → INFO
    agenda = get_agenda_dia()
    for a in agenda:
        info.append({
            'tipo': 'agenda',
            'nivel': 'info',
            'titulo': a.get('titulo', ''),
            'hora': a.get('hora', ''),
            'proyecto': a.get('proyecto', ''),
        })

    # Resumen
    partes = []
    if rojas:
        partes.append(f"ALERTA: {len(rojas)} seguimiento{'s' if len(rojas) != 1 else ''} vencido{'s' if len(rojas) != 1 else ''}")
    if amarillas:
        partes.append(f"{len(amarillas)} próximo{'s' if len(amarillas) != 1 else ''} a vencer")
    if agenda:
        partes.append(f"{len(agenda)} en agenda hoy")

    return {
        'rojas': rojas,
        'amarillas': amarillas,
        'info': info,
        'total': len(rojas) + len(amarillas) + len(info),
        'resumen': ' | '.join(partes) if partes else 'Sin alertas',
        'hay_criticas': len(rojas) > 0,
    }


def alertas_criticas():
    """
    Shortcut: solo devuelve alertas rojas (vencidos).
    Retorna lista vacía si no hay nada urgente.
    """
    return _seguimientos_vencidos()


def formato_alertas(alertas):
    """Formatea alertas como texto legible."""
    lines = []

    if alertas['rojas']:
        lines.append(f"{'='*50}")
        lines.append(f"  ALERTAS ROJAS — {len(alertas['rojas'])} seguimientos vencidos")
        lines.append(f"{'='*50}")
        for a in alertas['rojas']:
            proyecto = f" [{a['proyecto']}]" if a['proyecto'] else ""
            persona = f" → {a['persona']}" if a['persona'] else ""
            lines.append(f"  [{a['dias']}d] {a['accion'][:60]}{proyecto}{persona}")
        lines.append("")

    if alertas['amarillas']:
        lines.append(f"--- Próximos a vencer ({len(alertas['amarillas'])}) ---")
        for a in alertas['amarillas']:
            dias_txt = "HOY" if a['dias'] == 0 else f"en {a['dias']}d"
            lines.append(f"  [{dias_txt}] {a['accion'][:60]}")
        lines.append("")

    if not alertas['rojas'] and not alertas['amarillas']:
        lines.append("Sin alertas urgentes.")

    return "\n".join(lines)


if __name__ == '__main__':
    alertas = generar_alertas()
    print(formato_alertas(alertas))
    print(f"\nResumen: {alertas['resumen']}")
