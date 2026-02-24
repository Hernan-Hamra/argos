"""
ARGOS Multi-Agent System
========================
7 agentes especializados + orquestador.

Agentes:
  neuro      - Dr. Neuro: análisis de lenguaje, cognición, carga mental
  comercial  - Estratega: negocio, pricing, competencia, go-to-market
  arquitecto - Arquitecto: diseño técnico, viabilidad, integración
  data       - Data Engineer: métricas, predicción, ML, auto-mejora
  ux         - UX Lead: experiencia de usuario, onboarding, flujos
  etico      - Ético: privacidad, confianza, compliance, límites
  dba        - DBA: schema, queries, migraciones, integridad de datos

Uso:
  from agents.orquestador import cargar_prompt, evaluar_triggers, panel_agentes
"""

AGENTES_DISPONIBLES = ['neuro', 'comercial', 'arquitecto', 'data', 'ux', 'etico', 'dba']
