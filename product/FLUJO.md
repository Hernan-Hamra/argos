# Flujo de Trabajo ARGOS
*El ciclo completo de una sesión*

---

## Ciclo de 7 pasos

```
APERTURA → AGENDA → CHAT → REGISTRO → DEVOLUCIÓN → AGENDA CIERRE → SEGUIMIENTO
   │                                                                      │
   └──────────────────────── próxima sesión ◄─────────────────────────────┘
```

### Paso 1: APERTURA (al abrir ARGOS)
- Saludar por nombre
- Leer DB: alertas, deadlines, vencidos
- Mostrar alertas y seguimiento (tipo C)
- Mostrar agenda pendiente del día
- Preguntar: "¿En qué querés trabajar?"

### Paso 2: AGENDA (planificación de sesión)
- ¿Qué tenés para hoy? (usuario dice o ARGOS sugiere)
- Priorizar: urgente → importante → puede esperar
- Armar lista de la sesión (3-5 items max)
- Registrar sesion_agenda en DB

### Paso 3: CHAT (trabajo libre)
- El usuario trabaja con ARGOS
- Cada interacción se clasifica automáticamente
- Se registra en DB en tiempo real

### Paso 4: REGISTRO (automático, durante sesión)
- Cada evento → DB con tipo, subtipo, proyecto, persona, energía, impacto
- Cada acción completada → marcar en seguimiento
- Cada nuevo pendiente → crear en seguimiento con deadline
- Cada comunicación → registrar fuente + resultado

### Paso 5: DEVOLUCIÓN (al cerrar sesión)
6 tipos de devolución:

| Tipo | Qué es | Cuándo |
|------|--------|--------|
| A. Resumen de sesión | Qué hicimos | Siempre (al cerrar) |
| B. Balance vida/trabajo | Distribución del tiempo | Semanal + a pedido |
| C. Alertas y seguimiento | Deadlines, vencimientos, fechas | Siempre (al abrir) |
| D. Insight personal | Patrones detectados, observaciones | Semanal/mensual |
| E. Métricas de rendimiento | Números duros | Mensual + a pedido |
| F. Próximos pasos | Qué hacer después | Siempre (al cerrar) |

### Paso 6: AGENDA ACTUALIZADA (al cerrar)
- ¿Qué se completó de la agenda?
- ¿Qué quedó pendiente? → reprogramar
- ¿Qué nuevo surgió? → agendar
- Sugerir agenda para próxima sesión

### Paso 7: SEGUIMIENTO PASIVO (entre sesiones)
- Deadlines siguen corriendo
- Al abrir próxima sesión, ARGOS calcula:
  - Qué venció
  - Qué está por vencer
  - Qué fechas se acercan
  - Qué patterns se repiten

---

## Clasificación automática de interacciones

| Tipo de entrada | Ejemplo | Tag |
|----------------|---------|-----|
| Pedido de acción | "Dame un mail para X" | accion |
| Actualización | "Mandé el mail" | estado |
| Consulta estratégica | "¿Cómo resuelvo esto?" | estrategia |
| Descarga emocional | "Mi jefe me presiona" | personal |
| Organización | "Agregá esto al seguimiento" | organizacion |
| Construcción | "Armemos una herramienta para X" | construccion |

---

## Estructura del evento en DB

```
evento {
    fecha, hora,
    tipo:       laboral | personal | salud | familia | argos
    subtipo:    accion | estado | estrategia | personal | organizacion | construccion
    proyecto:   → FK proyectos
    persona:    → FK personas
    descripcion,
    fuente:     chat | whatsapp | email | archivo | reunion
    resultado:  completado | pendiente | enviado | esperando
    energia:    1-5
    impacto:    1-5
    duracion_min
}
```

---

## Detalle de cada tipo de devolución

### Tipo A: Resumen de sesión
```
SESIÓN [FECHA]
──────────────
Duración estimada: ~X horas
Eventos registrados: N
Proyectos tocados: N (lista)

Acciones:
✓ [completadas]
⏳ [pendientes]

Nuevos pendientes: N
```

### Tipo B: Balance vida/trabajo
```
HOY:
  Laboral:  ████████░░ 60%
  Personal: ███░░░░░░░ 20%
  ARGOS:    ██░░░░░░░░ 20%

SEMANA:
  Laboral:  ██████████ 80%  ← desbalance
  Personal: █░░░░░░░░░ 10%
  ARGOS:    █░░░░░░░░░ 10%
```

### Tipo C: Alertas y seguimiento
```
⚠️  CRÍTICO: [descripción] (deadline [fecha] - N días)
⚠️  ALTA: [descripción] (deadline [fecha])
🎂 [Nombre] cumple N el [fecha] (N días)
📅 [Evento] el [fecha] (N días)
```

### Tipo D: Insight personal
```
PATRONES DETECTADOS:
• [observación sobre distribución de tiempo/energía]
• [observación sobre proyectos desatendidos]
• [observación sobre relaciones/dinámicas]
• [sugerencia basada en metas del perfil]
```

### Tipo E: Métricas de rendimiento
```
[PERÍODO]:
  Eventos registrados:     N
  Proyectos activos:       N
  Pendientes abiertos:     N (N críticos, N altos)
  Pendientes cerrados:     N
  Tasa de cierre:          N%
  Comunicaciones enviadas: N
  Herramientas creadas:    N
```

### Tipo F: Próximos pasos
```
PRÓXIMA SESIÓN:
1. [URGENTE] [acción]
2. [ALTA] [acción]
3. [MEDIA] [acción]
```
