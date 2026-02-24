"""
Orquestador del sistema multi-agente ARGOS.
Decide qué agentes activar según el contexto de la sesión.
"""

import os
import json
from datetime import date, datetime

# Path al directorio de agentes
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Importar tracker con path correcto
import sys
sys.path.insert(0, os.path.join(AGENTS_DIR, '..'))
from tools.tracker import (get_agentes, get_agente, get_consultas_agente,
                            registrar_consulta_agente, get_resumen_agentes)


def cargar_prompt(agente_codigo):
    """Carga el system prompt de un agente desde su .md"""
    path = os.path.join(AGENTS_DIR, f"{agente_codigo}.md")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def evaluar_triggers(contexto_sesion):
    """
    Dado el contexto de una sesión, devuelve qué agentes deberían activarse.

    contexto_sesion = {
        'momento': 'apertura' | 'durante' | 'cierre',
        'tema': str | None,
        'funcion_nueva': bool,
        'datos_sensibles': bool,
        'schema_change': bool,
        'errores_tipeo': int,
        'longitud_mensajes_promedio': float,
    }

    Returns: lista de códigos de agentes a activar
    """
    agentes = []
    momento = contexto_sesion.get('momento', 'durante')
    tema = contexto_sesion.get('tema', '')

    # DR. NEURO: al cierre siempre, durante si hay señales de estrés
    if momento == 'cierre':
        agentes.append('neuro')
    elif contexto_sesion.get('errores_tipeo', 0) > 5:
        agentes.append('neuro')

    # ESTRATEGA: cuando hay función nueva o tema de negocio
    if contexto_sesion.get('funcion_nueva'):
        agentes.append('comercial')
    if tema in ('estrategia', 'pricing', 'competencia', 'negocio', 'mercado'):
        agentes.append('comercial')

    # ARQUITECTO: propuestas técnicas o cambios de schema
    if contexto_sesion.get('schema_change'):
        agentes.append('arquitecto')
    if tema in ('arquitectura', 'stack', 'infraestructura', 'diseño_tecnico'):
        agentes.append('arquitecto')

    # DATA ENGINEER: al cierre para métricas
    if momento == 'cierre':
        agentes.append('data')
    if tema in ('metricas', 'datos', 'patrones', 'prediccion', 'ml'):
        agentes.append('data')

    # UX LEAD: cuando se diseña algo para el usuario
    if tema in ('onboarding', 'flujo', 'ux', 'interfaz', 'usuario'):
        agentes.append('ux')
    if contexto_sesion.get('funcion_nueva'):
        agentes.append('ux')

    # ÉTICO: datos sensibles
    if contexto_sesion.get('datos_sensibles'):
        agentes.append('etico')
    if tema in ('privacidad', 'etica', 'compliance', 'datos_personales'):
        agentes.append('etico')

    # DBA: cambios de schema
    if contexto_sesion.get('schema_change'):
        agentes.append('dba')
    if tema in ('database', 'schema', 'migracion', 'indices', 'query'):
        agentes.append('dba')

    # Eliminar duplicados manteniendo orden
    vistos = set()
    resultado = []
    for a in agentes:
        if a not in vistos:
            vistos.add(a)
            resultado.append(a)

    return resultado


def preparar_consulta(agente_codigo, contexto):
    """
    Prepara el prompt completo para consultar a un agente.

    Returns: dict con system prompt, contexto y historial reciente.
    """
    prompt_base = cargar_prompt(agente_codigo)
    if not prompt_base:
        return None

    historial = get_consultas_agente(agente_codigo, limit=5)
    agente_info = get_agente(agente_codigo)

    return {
        'agente': agente_info,
        'system_prompt': prompt_base,
        'contexto': contexto,
        'historial_reciente': historial,
        'fecha': date.today().isoformat(),
        'hora': datetime.now().strftime('%H:%M')
    }


def registrar_resultado(agente_codigo, tipo, contexto, resultado, confianza=0.8):
    """Registra la intervención de un agente en la DB."""
    return registrar_consulta_agente(agente_codigo, tipo, contexto, resultado, confianza)


def panel_agentes():
    """
    Genera resumen de actividad de agentes para el reporte de sesión.
    Pensado para ejecutarse al inicio de sesión (después de reporte_patrones).
    """
    try:
        agentes = get_resumen_agentes()
    except Exception:
        # Si las tablas no existen todavía
        return "Sistema multi-agente: no inicializado. Ejecutar seed_agentes.py."

    if not agentes:
        return "Sistema multi-agente: sin agentes registrados."

    lineas = []
    lineas.append("=" * 60)
    lineas.append("  ARGOS MULTI-AGENTE | Panel de equipo")
    lineas.append("=" * 60)

    activos = [a for a in agentes if a['estado'] == 'activo']
    lineas.append(f"  Agentes activos: {len(activos)}")
    lineas.append("")

    for a in agentes:
        total = a.get('total_consultas', 0) or 0
        aceptadas = a.get('aceptadas', 0) or 0
        rechazadas = a.get('rechazadas', 0) or 0
        ultima = a.get('ultima_actividad') or 'nunca'

        if total > 0:
            tasa = f"{aceptadas}/{total} aceptadas"
        else:
            tasa = "sin consultas"

        estado_icon = '+' if a['estado'] == 'activo' else '-'
        lineas.append(f"  [{estado_icon}] {a['nombre']:20s} | {tasa:20s} | última: {ultima}")

    # Sugerencias pendientes (consultas sin aceptar/rechazar)
    lineas.append("")
    lineas.append("=" * 60)

    return '\n'.join(lineas)


if __name__ == '__main__':
    # Test rápido
    print(panel_agentes())
    print()
    print("Triggers al cierre:", evaluar_triggers({'momento': 'cierre'}))
    print("Triggers con función nueva:", evaluar_triggers({'momento': 'durante', 'funcion_nueva': True}))
    print("Triggers con datos sensibles:", evaluar_triggers({'momento': 'durante', 'datos_sensibles': True}))
