# El Método ARGOS
*Cómo convertir a Claude en tu asesor personal*

---

## Filosofía

ARGOS no es un software que usás. Es un asistente que te conoce. La diferencia es fundamental:
- Un software tiene funciones fijas → vos te adaptás a él
- ARGOS se adapta a vos → le decís qué necesitás y lo construye

El método tiene 5 fases. Las primeras 2 se hacen una vez (onboarding). Las otras 3 son el uso diario.

---

## Fase 1: Conocerte (onboarding, sesión 1)

### Qué pasa
ARGOS te hace preguntas para armar tu perfil:
- ¿Quién sos? (nombre, edad, ubicación, familia)
- ¿A qué te dedicás? (trabajo actual, historia laboral)
- ¿Qué proyectos tenés activos? (laborales y personales)
- ¿Qué querés lograr? (metas, aspiraciones)
- ¿Qué te preocupa? (problemas, pendientes, reclamos)

### Qué se genera
- **perfil.md** — tu perfil completo (se va enriqueciendo con cada sesión)
- **CLAUDE.md** — las reglas de tu proyecto (personalizadas a tu contexto)
- **MEMORY.md** — índice de memoria para que ARGOS te recuerde siempre

### Ejemplo real
> "Soy Hernán, tengo 52 años, trabajo en una empresa de IT armando licitaciones. Tengo un emprendimiento de seguridad. Estoy casado, tengo 3 hijos."
>
> A partir de esto, ARGOS armó un perfil de 567 líneas con historia laboral, familia, formación, aspiraciones, áreas de mejora y cronología visual.

---

## Fase 2: Mapear tu mundo (onboarding, sesión 1-2)

### Qué pasa
ARGOS escanea tu entorno digital:
- ¿Dónde guardás tus archivos? (carpetas, OneDrive, Google Drive)
- ¿Qué herramientas usás? (Office, WhatsApp, email)
- ¿Qué estructura tiene tu trabajo?

### Qué se genera
- **directorio.md** — mapa completo de tus archivos y carpetas
- **Base de datos** — proyectos, personas, fechas importantes cargados en SQLite

### Por qué importa
Si ARGOS no sabe dónde están tus cosas, no puede ayudarte a encontrarlas ni organizarlas. El mapeo es la base de todo lo que viene después.

---

## Fase 3: Trackear (uso diario)

### Qué pasa
Cada vez que hacés algo relevante, ARGOS lo registra:
- Enviaste un mail → queda registrado con fecha y destinatario
- Tuviste una reunión → queda el resumen
- Te pidieron algo → queda como pendiente con deadline
- Pasó algo importante → queda en el registro de eventos

### Qué se genera
- **Eventos** en la DB con fecha, tipo, proyecto, persona, resultado
- **Seguimiento** de pendientes con alertas y deadlines
- **Métricas** de actividad (por proyecto, por tipo, por período)

### Ejemplo real
> ARGOS detectó que el cumpleaños de un hijo es en 8 días, que un reclamo laboral tiene deadline en 48 horas, y que hay materiales pendientes de entrega para un proyecto.

---

## Fase 4: Asesorar (bajo demanda)

### Qué pasa
Le pedís opinión, ayuda con una comunicación, o análisis de una situación.

ARGOS lee tu perfil completo, el contexto del proyecto, el historial con la persona involucrada, y te da una respuesta calibrada.

### Capacidades
1. **Redacción de mensajes** — WhatsApp, email, cartas. Calibra el tono al interlocutor.
2. **Análisis de situaciones** — detecta dinámicas de poder, evalúa tu posición, identifica riesgos.
3. **Opiniones honestas** — si pedís que no sea condescendiente, va directo.
4. **Construcción de casos** — arma evidencia verificable desde chats, archivos, timestamps.

### Principios
- Honesto cuando se pide
- Nunca fabrica datos ni evidencia
- Itera rápido con feedback del usuario
- Desaconseja lo que debilita tu posición
- Respeta tu decisión final

### Ejemplo real
> Un usuario necesitaba reclamar un pago a su jefe. ARGOS:
> 1. Leyó 567 líneas de perfil personal
> 2. Analizó el patrón de comportamiento del jefe (controla con dinero)
> 3. Extrajo 68 registros de actividad como evidencia
> 4. Dio opinión honesta sobre la relación laboral
> 5. Redactó 6 versiones iterativas del mensaje hasta llegar al tono justo
> 6. Armó email formal + WhatsApp de refuerzo
> 7. Registró todo para seguimiento con deadline

---

## Fase 5: Construir (cuando lo necesitás)

### Qué pasa
Le pedís una herramienta y ARGOS la construye. No necesitás saber programar.

### Ejemplos de lo que se puede crear
- "Necesito trackear mis pacientes" → tabla en DB + consultas
- "Quiero ver cuánto trabajé este mes" → gráfico de actividad
- "Armame una cotización con IVA" → planilla con cálculos automáticos
- "Generame un Word con membrete" → documento formateado listo para imprimir
- "Organizame esta carpeta" → clasifica y mueve archivos
- "Parseame este chat de WhatsApp" → extrae datos estructurados

### La magia
El usuario dice QUÉ quiere. ARGOS decide CÓMO hacerlo. Claude Code escribe el código, lo ejecuta, y entrega el resultado.

---

## Ciclo de sesión típico

```
1. Abrís ARGOS
2. Te saluda por nombre
3. Te muestra alertas (deadlines, cumpleaños, pendientes vencidos)
4. Te pregunta en qué querés trabajar
5. Trabajás (tracking, asesoría, construcción, organización)
6. Al cerrar, todo queda registrado automáticamente
7. La próxima vez, ARGOS recuerda todo y retoma donde dejaste
```

---

## Perfiles de usuario

ARGOS se adapta al perfil del usuario. Cada perfil activa módulos y flujos distintos:

| Perfil | Módulos principales | Ejemplo real |
|--------|--------------------|----|
| **Project Manager** | Estructura de obra, materiales (pedido/entregado/stock), avance por etapa, subcontratistas, proveedores, alertas de tiempos, cobranzas | Posadas: 8 pisos, 28 items materiales, 3 proveedores |
| **Psicólogo** | Pacientes, sesiones, evolución, turnos, facturación, notas privadas | Seguimiento de 20 pacientes con alertas de asistencia |
| **Secretaria/Admin** | Agenda, comunicaciones, trámites, archivo, recordatorios | Gestión de turnos + correspondencia + seguimiento |
| **Emprendedor** | Pipeline ventas, cotizaciones, clientes, cobros, métricas | AiControl: presupuestos + seguimiento comercial |
| **Personal** | Organización digital, fechas, salud, familia, búsqueda laboral | Balance vida/trabajo + tracking multidimensional |

Los perfiles no son excluyentes. Un usuario puede ser Project Manager en lo laboral y Personal en lo privado (como el caso piloto).

---

## Lo que hace único al método

1. **No es una app con botones.** Es una conversación con un asistente que te conoce.
2. **No tiene funciones fijas.** Construye lo que necesitás cuando lo necesitás.
3. **No pierde contexto.** La memoria persiste entre sesiones.
4. **No juzga.** Pero tampoco miente si le pedís honestidad.
5. **Crece con vos.** Cada sesión lo hace más útil.
6. **Se adapta a tu perfil.** No es lo mismo un psicólogo que un director de obra.
