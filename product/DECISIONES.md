# ARGOS - Decisiones Estrategicas
*Creado: 24 de febrero de 2026*

---

## Decision 1: ARGOS es ESPEJO, no COACH (24/02/2026)

### Contexto
Se consulto a 4 agentes (Neuro, Comercial, UX, Etico) sobre como ARGOS debe servir a los usuarios finales. La pregunta central: necesitamos agentes especializados visibles (doctor, coach, asesor financiero) o el metodo generico + contexto profundo es suficiente?

### Consenso de los agentes

**Dr. Neuro:**
- ARGOS funciona mejor como ESPEJO que como COACH
- Mostrar patrones sin empujar cambio. "Llevas 3 semanas sin actividad en busqueda laboral" vs "Deberias buscar trabajo"
- Riesgo Goodhart: si medis algo, la gente optimiza la metrica, no el objetivo real
- Herramienta mas impactante: detector de coherencia intencion/comportamiento (IMPLEMENTADO)

**Estratega Comercial:**
- Enfoque hibrido: arrancar generico, verticalizar despues
- Killer feature: "el unico asistente que no te hace repetir tu historia"
- NO crear agentes visibles para usuarios — complejidad prematura
- Monetizar: suscripcion mensual, no por agente

**UX Lead:**
- Onboarding en 10 preguntas, resultado tangible en 20 minutos
- Flujo visible: INICIO → TRABAJO → CIERRE (simple, predecible)
- Los agentes deben ser invisibles para el usuario final
- El usuario habla con ARGOS, no con "el Dr. Neuro" ni "el Estratega"

**Etico:**
- ALERTA: Dr. Neuro + tracking psicologico sin marco legal = riesgo
- ALERTA: backup OneDrive expone datos sensibles sin encriptacion
- El analisis emocional requiere consentimiento explicito
- Datos de menores (hijos) requieren tratamiento especial

### Decision
- **ARGOS es UNA entidad para el usuario.** No hay agentes visibles.
- **Espejo, no coach.** Mostrar datos, no prescribir acciones.
- **Metodo generico + contexto profundo = el producto.** No necesitamos especialistas visibles.
- **Los agentes internos (dev team) existen pero son invisibles** — mejoran el producto, no interactuan con el usuario.

### Implicaciones
- No construir interfaz de agentes para usuarios
- El reporte de coherencia es descriptivo ("0hs en busqueda laboral") no prescriptivo ("deberias buscar trabajo")
- El analisis de Dr. Neuro alimenta metricas internas, no se muestra como "diagnostico"
- Pendiente: resolver alertas del agente Etico (marco legal, encriptacion)

---

## Decision 2: Sistema Multi-Agente para desarrollo (24/02/2026)

### Contexto
ARGOS necesita multiples perspectivas para evolucionar como producto. En vez de depender de una sola vision, se creo un equipo de 7 agentes especializados que evaluan cada cambio desde su area.

### Los 7 agentes

| Codigo | Nombre | Rol | Activacion |
|--------|--------|-----|------------|
| neuro | Dr. Neuro | Neurociencia, cognicion, carga mental | Cierre sesion, estres |
| comercial | Estratega | Negocio, pricing, go-to-market | Funcion nueva, estrategia |
| arquitecto | Arquitecto | Diseno tecnico, viabilidad | Cambios tecnicos, schema |
| data | Data Engineer | Metricas, ML, prediccion | Cierre sesion, metricas |
| ux | UX Lead | Experiencia usuario, onboarding | Funcion nueva, interfaz |
| etico | Etico | Privacidad, compliance, limites | Datos sensibles, exportacion |
| dba | DBA | Schema, queries, migraciones | Cambios schema, review |

### Como funcionan
- Son prompts especializados (agents/*.md) invocados como subagentes de Claude Code
- Comparten la misma DB SQLite (tabla consultas_agente para log)
- El orquestador (agents/orquestador.py) decide cuando activar cada uno
- Las consultas se registran con tipo, resultado, confianza y aceptacion (feedback loop)

### Integracion entre agentes
- **Neuro → Data:** analisis emocional alimenta metricas de bienestar
- **Comercial → UX:** estrategia de mercado define prioridades de interfaz
- **Arquitecto → DBA:** cambios tecnicos requieren evaluacion de schema
- **Data → Neuro:** metricas de uso alimentan deteccion de patrones cognitivos
- **Etico → Todos:** cualquier dato sensible pasa por evaluacion etica
- **DBA → Data:** estado de indices y queries optimas para metricas
- **UX → Comercial:** experiencia de usuario informa diferencial competitivo

### Primera consulta real (24/02/2026)
Se consulto a Neuro, Comercial, UX y Etico sobre estrategia de producto para usuarios finales. Resultados registrados en DB (5 consultas_agente). El Arquitecto evaluo viabilidad tecnica del sistema multi-agente: ALTA (10 archivos, 2 modificados, schema limpio).

---

## Decision 3: Detector de Coherencia implementado (24/02/2026)

### Contexto
Dr. Neuro identifico que la herramienta mas impactante es un "espejo" que muestre la diferencia entre lo que el usuario dice querer y lo que realmente hace. Ejemplo: Hernan declaro "salir de SBD" como meta, pero tiene 0hs de actividad en busqueda laboral.

### Implementacion
- **Tabla metas** en tracker.py — intenciones declaradas con area, proyecto, prioridad, horas/semana meta
- **tools/coherencia.py** — cruza metas con actividad real (eventos + seguimiento)
- **Senales:** on_track (>=0.7), en_riesgo (0.3-0.7), desalineada (<0.3), abandonada (<0.1 + 30 dias inactivo)
- **Primer reporte real (24/02/2026):**

| Meta | Senal | Coherencia | Detalle |
|------|-------|------------|---------|
| ARGOS | on_track | 0.76 | 3.8 de 5 hs/sem |
| Organizacion digital | on_track | 1.0 | 2.7 de 1 hs/sem |
| Posadas | desalineada | 0.0 | 0.3 de 10 hs/sem, 6 pendientes |
| AiControl | abandonada | 0.0 | Sin actividad |
| Busqueda laboral | abandonada | 0.0 | Sin actividad |
| Salud | abandonada | 0.0 | Sin actividad |

**Coherencia promedio: 0.29** — energia concentrada en ARGOS, metas declaradas como "alta prioridad" sin actividad.

### Principio
El reporte es descriptivo, no prescriptivo. Muestra numeros, no dice que hacer. El usuario decide.

---

## Decision 4: Proximos pasos segun agentes (24/02/2026)

### Tier 1 — Implementar ahora (impacto alto, esfuerzo bajo)

| Item | Agente origen | Estado |
|------|--------------|--------|
| Detector coherencia intencion/comportamiento | Neuro | IMPLEMENTADO |
| Reporte de energia/carga mental al cierre | Neuro | Pendiente |
| Primer reporte de coherencia real | Neuro + Data | IMPLEMENTADO |

### Tier 2 — Implementar proximo (impacto alto, esfuerzo medio)

| Item | Agente origen | Estado |
|------|--------------|--------|
| Onboarding en 10 preguntas | UX | Pendiente |
| Resultado tangible en 20 min (primera sesion) | UX | Pendiente |
| Marco legal para analisis emocional | Etico | Pendiente |
| Encriptacion de backup DB | Etico | Pendiente |
| Verticales ligeras (secretario ejecutivo, salud) | Comercial | Pendiente |

### Tier 3 — Explorar despues (impacto medio, esfuerzo alto)

| Item | Agente origen | Estado |
|------|--------------|--------|
| ML sobre consultas_agente (feedback loop real) | Data | Pendiente |
| Metricas de bienestar desde lenguaje | Neuro + Data | Pendiente |
| Dashboard web simple | UX + Arquitecto | Pendiente |
| Pricing basado en valor medido | Comercial + Data | Pendiente |
| Separacion DB sistema/usuario | DBA + Arquitecto | Pendiente |

### Alertas activas (Agente Etico)
1. Dr. Neuro + tracking psicologico: requiere consentimiento explicito y marco legal antes de activar para usuarios externos
2. Backup OneDrive: datos sensibles (salud, finanzas, emociones) sin encriptacion
3. Datos de menores: si ARGOS registra info de hijos, requiere tratamiento especial

---

## Historial de decisiones previas (contexto)

| Fecha | Decision | Fuente |
|-------|----------|--------|
| 18/02/2026 | Kit vendible > SaaS. Vender metodo, no plataforma | ALCANCE.md |
| 20/02/2026 | B2C directo. AiControl factura al cliente | BACKLOG.md |
| 20/02/2026 | Telegram como primera interfaz mobile | BACKLOG.md |
| 20/02/2026 | Proceso se comparte, data nunca | ALCANCE.md |
| 20/02/2026 | Ecosistema propio de AiControl, independiente de Anthropic | BACKLOG.md |
| 22/02/2026 | Auto-aprendizaje automatico con 6 detectores | BACKLOG.md |
| 24/02/2026 | Espejo no coach — agentes invisibles para usuario | Esta sesion |
| 24/02/2026 | Sistema multi-agente de 7 para desarrollo | Esta sesion |
| 24/02/2026 | Detector de coherencia como primera herramienta de espejo | Esta sesion |
