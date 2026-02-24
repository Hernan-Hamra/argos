"""
Seed de los 7 agentes del sistema multi-agente ARGOS.
Ejecutar una vez para poblar la tabla agentes en la DB.

Uso: python agents/seed_agentes.py
"""

import os
import sys

# Asegurar que tools/ esté en el path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from tools.tracker import init_db, add_agente, get_agentes


AGENTES = [
    {
        'codigo': 'neuro',
        'nombre': 'Dr. Neuro',
        'descripcion': 'Análisis de lenguaje, estados cognitivos/emocionales, carga mental',
        'prompt_file': 'agents/neuro.md',
        'capacidades': ['analisis_lenguaje', 'deteccion_emocional', 'carga_cognitiva',
                        'patrones_temporales', 'metricas_sesion'],
        'triggers': ['cierre_sesion', 'señal_estres', 'pedido_usuario']
    },
    {
        'codigo': 'comercial',
        'nombre': 'Estratega',
        'descripcion': 'Modelo de negocio, diferenciación, pricing, competencia, go-to-market',
        'prompt_file': 'agents/comercial.md',
        'capacidades': ['analisis_competitivo', 'pricing', 'go_to_market',
                        'evaluacion_funciones', 'narrativa_producto'],
        'triggers': ['funcion_nueva', 'tema_estrategia', 'review_mensual']
    },
    {
        'codigo': 'arquitecto',
        'nombre': 'Arquitecto',
        'descripcion': 'Diseño técnico, integración, APIs, viabilidad, escalabilidad',
        'prompt_file': 'agents/arquitecto.md',
        'capacidades': ['diseño_sistema', 'viabilidad_tecnica', 'trade_offs',
                        'estimacion_esfuerzo', 'review_codigo'],
        'triggers': ['propuesta_tecnica', 'cambio_schema', 'nuevo_modulo', 'decision_stack']
    },
    {
        'codigo': 'data',
        'nombre': 'Data Engineer',
        'descripcion': 'Predicción, métricas, ML, auto-mejora, calidad de datos',
        'prompt_file': 'agents/data.md',
        'capacidades': ['metricas', 'prediccion', 'clustering', 'feedback_loop',
                        'calidad_datos', 'reportes'],
        'triggers': ['cierre_sesion', 'datos_suficientes', 'pedido_metricas', 'review_semanal']
    },
    {
        'codigo': 'ux',
        'nombre': 'UX Lead',
        'descripcion': 'Experiencia de usuario, onboarding, flujos, usabilidad, copy',
        'prompt_file': 'agents/ux.md',
        'capacidades': ['evaluacion_ux', 'flujos', 'onboarding', 'copy',
                        'accesibilidad', 'progressive_disclosure'],
        'triggers': ['funcion_nueva', 'tema_onboarding', 'señal_confusion', 'review_mensual']
    },
    {
        'codigo': 'etico',
        'nombre': 'Ético',
        'descripcion': 'Privacidad, confianza, límites del asistente, compliance legal',
        'prompt_file': 'agents/etico.md',
        'capacidades': ['evaluacion_etica', 'consentimiento', 'anonimizacion',
                        'compliance', 'lineas_rojas'],
        'triggers': ['datos_sensibles', 'export_datos', 'review_trimestral', 'dato_nuevo']
    },
    {
        'codigo': 'dba',
        'nombre': 'DBA',
        'descripcion': 'Schema, queries, migraciones, integridad, arquitectura de datos',
        'prompt_file': 'agents/dba.md',
        'capacidades': ['schema_design', 'query_optimization', 'migraciones',
                        'integridad', 'backup', 'indices'],
        'triggers': ['cambio_schema', 'query_lenta', 'review_mensual', 'crecimiento_db']
    }
]


def seed():
    """Poblar la tabla agentes. Usa INSERT OR IGNORE para ser idempotente."""
    # Asegurar que las tablas existen
    init_db()

    creados = 0
    existentes = 0

    for agente in AGENTES:
        aid = add_agente(
            codigo=agente['codigo'],
            nombre=agente['nombre'],
            descripcion=agente['descripcion'],
            prompt_file=agente['prompt_file'],
            capacidades=agente['capacidades'],
            triggers=agente['triggers']
        )
        if aid:
            creados += 1
            print(f"  + {agente['nombre']:20s} (id={aid})")
        else:
            existentes += 1
            print(f"  = {agente['nombre']:20s} (ya existe)")

    print(f"\nResultado: {creados} creados, {existentes} ya existían")

    # Mostrar estado final
    print(f"\nAgentes en DB:")
    for a in get_agentes():
        print(f"  [{a['id']}] {a['codigo']:15s} {a['nombre']:20s} estado={a['estado']}")


if __name__ == '__main__':
    print("=" * 50)
    print("  ARGOS — Seed de agentes multi-agente")
    print("=" * 50)
    seed()
