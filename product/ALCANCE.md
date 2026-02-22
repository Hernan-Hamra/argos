# ARGOS - Alcance del Producto
*Definido: 18 de febrero de 2026*

---

## Visión

ARGOS es un asistente personal con IA que te conoce, te organiza, te asesora, te entrena y construye herramientas a medida. No es una app con botones — es una conversación con alguien que sabe todo de vos y puede resolver lo que le pidas.

---

## Alcance completo (37 capacidades)

### Arquitectura y autonomía
1. **Sistema autónomo** — funciona de forma independiente, se adapta al usuario sin intervención del creador
2. **Multiplataforma y multidispositivo** — funciona en cualquier dispositivo al que accedas (PC, Mac, Linux), y lo puede configurar
3. **Activo todo el tiempo** — le podés dar notas desde el celular, recibe input en cualquier momento
4. **Multifuncional** — no está limitado a un dominio, cubre trabajo + vida personal + salud + formación

### Resolución de problemas
5. **Problema que le das, problema que resuelve** — si tiene acceso a los equipos/archivos, ejecuta la solución
6. **Iteración con el cliente** — depura la solución a través del chat, ajusta según feedback hasta llegar al resultado correcto
7. **Genera herramientas** — si no existe la herramienta que necesitás, la construye (Excel, scripts, docs, dashboards)
8. **Consultor generalista** — puede opinar y asesorar sobre cualquier tema con contexto

### Comunicación
9. **Se le puede hablar** — interfaz conversacional natural, le decís qué necesitás y lo hace
10. **Elabora estrategias** — analiza situaciones, detecta dinámicas, propone caminos de acción
11. **Redacción calibrada** — emails, WhatsApp, cartas, notas formales — calibra el tono al interlocutor

### Tracking y organización
12. **Te conoce perfectamente** — perfil profundo que crece con cada sesión (historia, personalidad, relaciones, metas)
13. **Agenda** — calendario con recordatorios, alertas, eventos, deadlines
14. **Seguimiento** — pendientes con prioridad, estado, persona responsable, fecha límite
15. **Métricas de rendimiento** — tanto para vida privada como laboral, las que pidas

### Documentos y archivos
16. **Generación de documentos formales** — Word con membrete, PDFs, foliación, carátulas
17. **Extracción de datos de fuentes variadas** — PDFs escaneados, chats WhatsApp, Excel, imágenes
18. **Organización de archivos y directorios** — mapeo, clasificación, estructura de carpetas
19. **Cálculos especializados** — IVA mix, análisis de precios, álgebra inversa, presupuestos

### Planificación y gestión de proyectos
20. **Planificación cross-life** — cronograma que cruza TODAS las áreas (trabajo, salud, familia, desarrollo, formación) para encontrar horas reales disponibles
21. **Estimación de esfuerzo** — desglose de horas por tarea/fase de un proyecto, con totales y subtotales
22. **Cronograma balanceado** — plan semana a semana considerando obligaciones, imprevistos y vida personal
23. **Portfolio multi-proyecto** — vista unificada de todos los frentes abiertos con estado, riesgo y próximo paso
24. **Onboarding de proyectos externos** — incorporar cualquier proyecto al seguimiento de ARGOS sin mover código

### Auto-aprendizaje y mejora continua

#### Capacidades
29. **Aprende del usuario** — detecta patrones de trabajo automáticamente y sugiere mejoras
30. **Se auto-perfecciona** — cada sesión mejora respuestas, prioridades y forma de organizar
31. **Aprende de la comunidad** — patrones anónimos compartidos entre usuarios (con consentimiento) mejoran a todos
32. **Sugerencias proactivas** — no espera que le pidas, propone mejoras basadas en lo que detecta

#### Detección automática de herramientas nuevas

ARGOS detecta cuándo generó una herramienta que podría ser reutilizable:

- **Trigger:** ARGOS crea un script/tool para resolver un problema del usuario
- **Evaluación automática:** ¿Es genérica? ¿Podría servir a otros usuarios? ¿Es similar a algo que ya generó antes?
- **Si es reutilizable:** ARGOS la propone para el catálogo comunitario
- **Si es similar a otra existente:** ARGOS sugiere usar/mejorar la existente en vez de crear una nueva
- **Si es específica del usuario:** queda en su instancia local como herramienta personal

Ejemplos:
- "Generé un script de foliación de PDFs → es genérico → proponer al catálogo"
- "Generé un Excel de análisis de precios con IVA mix → es genérico para Argentina → proponer al catálogo regional"
- "Generé un parser de WhatsApp para extraer datos → ya existe uno en el catálogo → sugerir usar ese"
- "Generé un script para la licitación 410/26 de Hernán → es muy específico → queda local"

#### Motor de detección automática de patrones

El auto-aprendizaje de ARGOS es **automático**. No requiere que el usuario haga nada. El motor funciona así:

**1. Qué datos se miden (automáticamente, en cada sesión):**
- Tiempo por tipo de tarea (redacción, búsqueda, cálculo, generación de docs, planificación)
- Secuencia de acciones (¿siempre arranca por X antes de Y?)
- Frecuencia de uso por módulo (¿usa más agenda, tracking, docs, comunicación?)
- Iteraciones hasta resultado final (¿cuántas vueltas necesitó?)
- Horarios de trabajo (¿trabaja mejor de mañana, de noche, fines de semana?)
- Tasa de aceptación de sugerencias (¿las toma, las ignora, las modifica?)

**2. Cómo detecta patrones (triggers automáticos):**
- **Por repetición:** si el usuario hace la misma secuencia de acciones 3+ veces, ARGOS la identifica como patrón
- **Por contraste:** si una sesión fue significativamente más rápida/lenta que el promedio, ARGOS analiza por qué
- **Por abandono:** si el usuario empieza algo y lo deja, ARGOS registra el punto de abandono
- **Por éxito:** si algo funcionó bien (pocas iteraciones, resultado aceptado rápido), ARGOS lo marca como patrón exitoso
- **Umbral:** no notifica por un dato aislado — necesita 3+ ocurrencias para considerar que es un patrón

**3. Clasificación de patrones:**

| Tipo | Descripción | Ejemplo | Se comparte? |
|------|-------------|---------|--------------|
| **General** | Aplica a cualquier usuario sin importar perfil | "Redactar en iteraciones cortas es más rápido que escribir todo de una" | Sí (anónimo) |
| **Por perfil** | Aplica a usuarios con perfil similar (rol, industria, uso) | "Los usuarios de licitaciones trabajan mejor con checklist previo" | Sí (anónimo, agrupado por perfil) |
| **Personal** | Específico del usuario (preferencias, estilo, horarios) | "Hernán prefiere versiones iterativas del WhatsApp, no mail directo" | NO — queda solo en su instancia |

**4. Cómo sugiere (automáticamente):**
- **Al inicio de sesión:** "Detecté que los martes te concentrás mejor en desarrollo. Hoy es martes. ¿Querés arrancar con Bernasconi?"
- **En contexto:** "La última vez que armaste una cotización tardaste 2hs. ¿Querés que use la misma estructura que funcionó?"
- **Proactivo:** "Llevas 3 sesiones sin revisar pendientes de Posadas. ¿Le damos una pasada?"
- **El usuario siempre puede ignorar** — ARGOS registra si la sugerencia fue útil o no (feedback implícito)

**5. Principio fundamental: SE COMPARTE EL PROCESO, NUNCA LA DATA**

> **El usuario propone mejoras para sí mismo** — pide que ARGOS cambie o mejore
> cómo interactúa con él. ARGOS implementa la mejora para ese usuario.
> Luego **ARGOS evalúa automáticamente** si esa mejora es generalizable.
> Si lo es, ARGOS la propone a otros usuarios del mismo perfil. **El usuario
> no propone a la comunidad — ARGOS lo hace solo.**
> La DATA del usuario (contenido, archivos, nombres, números) NUNCA sale de su instancia.
> Solo se comparte el PROCESO (los pasos, el método, la herramienta).

Lo que se comparte:
- "Para hacer seguimiento de peso: crear tabla con fecha+peso, registrar diario, generar gráfico semanal" ← **PROCESO**
- "Para planificar un proyecto: cruzar con todas las áreas de vida del usuario" ← **PROCESO**

Lo que NUNCA se comparte:
- Cuánto pesa el usuario ← **DATA PRIVADA**
- Los proyectos, nombres, fechas, archivos del usuario ← **DATA PRIVADA**
- Contenido de documentos, chats, emails ← **DATA PRIVADA**

**6. Cuándo detecta y generaliza:**
- **En cada ciclo de interacción** (no solo al cerrar sesión): usuario pide → ARGOS resuelve → si funcionó → ARGOS evalúa si es generalizable
- **Al cerrar sesión:** revisión final de todo lo que se hizo, registro de funciones nuevas
- **Al abrir sesión:** verificar si hay funciones nuevas de la comunidad para sugerir

**7. Flujo completo (dos niveles):**

```
NIVEL 1 — USUARIO MEJORA SU ARGOS:
  Usuario trabaja → detecta algo mejorable → pide cambio a ARGOS
    → "Quiero que el seguimiento de peso incluya gráfico semanal"
    → "Prefiero que me mandes el resumen por Telegram, no por pantalla"
    → "Agregame un campo de estado de ánimo al registro diario"
  ARGOS implementa la mejora para ESE usuario → funciona → queda en su instancia

NIVEL 2 — ARGOS GENERALIZA (automático, el usuario no interviene):
  ARGOS evalúa cada mejora implementada:
    → ¿Es nueva? (algo que no existía antes)
    → ¿Funcionó? (el usuario la aceptó y la usa)
    → ¿Es generalizable? (otro usuario con perfil similar podría quererla)
      → Sí → ARGOS extrae el PROCESO (sin data) y lo registra en el catálogo
      → No → Queda como mejora personal de ese usuario

NIVEL 3 — DISTRIBUCIÓN A OTROS USUARIOS:
  Próxima sesión de cualquier usuario:
    → ARGOS consulta catálogo de funciones generalizadas
    → Filtra por perfil del usuario
    → Sugiere: "Hay una nueva función: seguimiento de peso con gráfico. ¿Querés probarla?"
    → El usuario acepta o ignora (feedback implícito)
    → Si acepta → ARGOS crea la herramienta con los datos del nuevo usuario (data separada)
```

**8. Ejemplo real:**

| Paso | Qué pasa | Se comparte? |
|------|----------|-------------|
| Usuario A pide "quiero trackear mi peso" | ARGOS crea tabla, función de registro, gráfico | NO — es la interacción privada |
| ARGOS detecta: interacción exitosa | Extrae el proceso: "crear seguimiento con registro diario + gráfico" | Solo el PROCESO |
| ARGOS evalúa: ¿es generalizable? | Sí — cualquier usuario de perfil 'salud' o 'familia' podría quererlo | Se registra en catálogo |
| Usuario B (perfil salud) abre sesión | ARGOS sugiere: "Hay seguimiento de peso disponible. ¿Querés activarlo?" | Solo la sugerencia |
| Usuario B acepta | ARGOS crea la misma herramienta PERO con los datos de B en la DB de B | La data de B queda en B |

**9. El perfil del usuario es la clave**

ARGOS ya construye un perfil profundo de cada usuario desde la primera sesión (historia de vida, trabajo, familia, objetivos, preferencias, estilo de comunicación). Ese perfil es lo que permite:
- Saber **qué funciones le sirven** a cada usuario (no le sugerís nutrición a alguien que no le interesa)
- Clasificar **por perfil** las funciones generalizadas (profesional, familia, salud, técnico, pyme)
- Personalizar **cómo** se implementa cada función (misma herramienta, adaptada al contexto del usuario)

**10. Ejemplos de funciones generalizables (la comunidad crece con cada interacción exitosa):**

| Un usuario pide... | ARGOS resuelve... | Se generaliza como... | Sirve para perfil... |
|---------------------|--------------------|-----------------------|---------------------|
| "Quiero trackear mi peso" | Tabla + registro diario + gráfico semanal | Seguimiento de peso | salud, familia |
| "Organizame las comidas de la semana" | Menú semanal + lista de compras + presupuesto | Planificador nutricional semanal | familia, salud |
| "Necesito facturar a mis clientes" | Pipeline de facturas + seguimiento de cobros + alertas | Gestión de facturación simple | pyme, profesional |
| "Ayudame a preparar la entrevista" | Análisis del puesto + preguntas + respuestas personalizadas | Preparador de entrevistas | profesional |
| "Haceme un CV para este puesto" | CV adaptado al puesto + cover letter + seguimiento | Generador de CV adaptativo | profesional |
| "Quiero controlar gastos del mes" | Registro de gastos + categorías + reporte mensual | Control de gastos personal | familia, profesional |
| "Recordame los turnos médicos" | Agenda de salud + alertas + historial | Seguimiento médico familiar | salud, familia |
| "Ayudame con el reclamo a la empresa" | Análisis de situación + estrategia + redacción calibrada | Asistente de reclamos laborales | profesional |
| "Necesito armar un presupuesto" | Plantilla + cálculos + PDF profesional | Generador de presupuestos | pyme, técnico |
| "Quiero aprender inglés 30 min/día" | Plan de estudio + seguimiento + recordatorios | Rutina de estudio con seguimiento | profesional, familia |
| "Organizame los archivos de la PC" | Mapeo + clasificación + estructura de carpetas | Organizador de archivos | todos |
| "Seguimiento del colegio de mis hijos" | Notas + reuniones + pendientes + calendario escolar | Seguimiento escolar | familia |
| "Cotización para instalar cámaras" | Relevamiento + materiales + mano de obra + PDF | Cotizador de instalaciones | técnico, pyme |
| "Quiero meditar todos los días" | Registro + racha + sugerencias + estadísticas | Seguimiento de hábitos | salud, todos |
| "Control de stock del negocio" | Inventario + alertas de mínimo + reposición | Control de inventario simple | pyme |
| "Planificar las vacaciones" | Presupuesto + itinerario + checklist + reservas | Planificador de viajes | familia, todos |

Cada una de estas es una interacción real que UN usuario tuvo con ARGOS. Si funcionó, ARGOS la generaliza automáticamente y la ofrece a otros usuarios del mismo perfil. El catálogo crece con cada sesión de cada usuario.

**11. Lo que el usuario sabe (transparencia):**
- Al registrarse, se le informa: "ARGOS aprende de cómo trabajás. Las interacciones exitosas se generalizan como procesos reutilizables para otros usuarios. Tus datos personales NUNCA se comparten — solo el método."
- Puede ver qué procesos se generalizaron de sus interacciones
- Puede pedir que un proceso NO se comparta (opt-out por proceso)
- Puede desactivar la generalización completamente (pierde acceso a funciones comunitarias)

### Cumplimiento normativo (compliance) y protección de datos

> **Traducción:** "Compliance" en español = **cumplimiento normativo** (o cumplimiento regulatorio). En protección de datos: **cumplimiento de protección de datos personales**.

#### Principio de separación: proceso vs data

| Concepto | Ejemplo | Se comparte? | Dónde vive? |
|----------|---------|-------------|-------------|
| **PROCESO** | "Para seguimiento de peso: tabla fecha+peso, registro diario, gráfico semanal" | Sí (anónimo) | Catálogo central AiControl |
| **DATA** | "Juan pesa 85kg el 22/02" | NUNCA | DB encriptada del usuario |
| **HERRAMIENTA** | Script/función que implementa el proceso | Sí (código genérico) | Catálogo central |
| **ARCHIVOS** | Excel, Word, PDF generados para el usuario | NUNCA | Carpeta privada del usuario |

#### Capacidades
33. **Encriptación por usuario** — cada usuario tiene su key de encriptación. Ni AiControl puede leer sus datos personales.
34. **Consentimiento explícito** — al registrarse se le informa del modelo de generalización. Opt-out disponible.
35. **Separación total** — PROCESO genérico (compartible) vs DATA personal (encriptada, privada, local).
36. **Cumplimiento legal** — Habeas Data (Ley 25.326 Argentina), GDPR (UE), derecho al olvido, auditoría de acceso
37. **Transparencia** — el usuario puede ver qué procesos se generalizaron, pedir opt-out, exportación o borrado total

#### Marco legal aplicable
| Normativa | Jurisdicción | Qué exige |
|-----------|-------------|-----------|
| Ley 25.326 (Habeas Data) | Argentina | Consentimiento, acceso, rectificación, supresión de datos personales |
| GDPR | Unión Europea | Consentimiento explícito, portabilidad, derecho al olvido, DPO |
| CCPA | California, EEUU | Derecho a saber qué datos se recolectan, derecho a borrado, opt-out de venta |

#### Garantías de privacidad
- **La DATA nunca sale de la instancia del usuario** — DB encriptada + archivos en carpeta privada
- **Solo se comparte el PROCESO** — los pasos, el método, la herramienta genérica (sin datos)
- **El usuario es informado** al registrarse de cómo funciona el modelo
- **Opt-out por proceso** — puede pedir que una interacción específica no se generalice
- **Opt-out total** — puede desactivar toda generalización (pierde acceso a funciones comunitarias)
- **Auditable** — puede ver exactamente qué procesos se generalizaron de sus interacciones
- **Derecho al olvido** — borrado total de todo lo asociado a su cuenta

#### Moderación y filtrado ético
- **El LLM rechaza interacciones ilegales o dañinas** — los modelos de IA (Claude, GPT, etc.) tienen filtros éticos incorporados. ARGOS hereda esos filtros.
- **Interacciones bloqueadas NO se generalizan** — si el LLM rechaza algo, ese proceso NUNCA entra al catálogo comunitario
- **Registro de intentos** — se registra que hubo un intento bloqueado (sin contenido específico, solo la categoría de bloqueo)
- **Política de uso aceptable** — al registrarse, el usuario acepta los términos. Intentos reiterados de uso indebido → suspensión de cuenta.
- **AiControl no modera contenido** — no leemos las interacciones de los usuarios. El filtro ético es del motor IA. AiControl solo ve métricas anónimas de bloqueos.
- **Capas de protección:** 1) Filtro del LLM → 2) No generalización → 3) Registro anónimo → 4) Suspensión si reiterado

### Módulos especializados (futuros)
25. **Entrenamiento físico** — planes de entrenamiento, seguimiento de actividad, métricas deportivas (tipo Tup)
26. **Nutrición** — planes alimentarios, lista de compras, seguimiento de dieta, presupuesto
27. **Profesor / tutor** — charlas específicas sobre cualquier tema, explicaciones adaptadas al nivel del usuario
28. **Salud** — turnos médicos, estudios, tratamientos, seguimiento de evolución

---

## Lo que YA funciona (probado en producción)

| Capacidad | Caso real |
|-----------|----------|
| Resolución de problemas | Licitación 384 folios, 4 carpetas, 26 scripts |
| Generación de documentos | DDJJs, notas membretadas, CVs, memorias técnicas |
| Tracking + seguimiento | 27 eventos, 8 pendientes, 6 agenda en DB SQLite |
| Métricas | Dashboard visual generado con matplotlib |
| Te conoce | Perfil de 567 líneas, cronología visual de vida |
| Estrategias | Análisis de dinámica jefe-empleado, reclamo con evidencia |
| Redacción calibrada | 6 versiones iterativas hasta el tono justo |
| Extracción de datos | 5 remitos escaneados → datos estructurados |
| Herramientas a medida | Excel materiales 3 hojas con colores y cruce de datos |
| Cálculos especializados | IVA mix 21%+10.5%, álgebra inversa desde total |
| Organización archivos | Estructura carpetas Posadas, mapeo OneDrive completo |
| Planificación cross-life | Cronograma Bernasconi: 14 semanas, cruzando 5 áreas de vida |
| Portfolio multi-proyecto | Vista unificada: Posadas + SBASE + Bernasconi + AiControl + salud |
| Onboarding externo | Bernasconi incorporado a ARGOS en 5 min sin mover código |

---

## Arquitectura: decisión

### NO hacer (por ahora)
- NO construir SaaS
- NO usar NestJS / framework web
- NO resolver escala antes de tener usuarios pagos
- NO construir antes de vender

### SÍ hacer
- Empaquetar lo que funciona como kit descargable
- Vender el MÉTODO, no la plataforma
- Validar con 3-5 usuarios piloto
- Escalar solo cuando la demanda lo justifique

### Razón
El producto es el método + la estructura + las herramientas. La plataforma es Claude Code (ya existe, la mantiene Anthropic). Construir infraestructura propia antes de validar el mercado es el error #1 de los startups.

---

## Fases de desarrollo

### Fase 1: KIT VENDIBLE (febrero - marzo 2026)
- [ ] setup.py — wizard de onboarding guiado
- [ ] Templates genéricos (CLAUDE.md, MEMORY.md, perfil)
- [ ] Tracker.py limpio (sin datos hardcodeados)
- [ ] Documentación usuario (GUIA_RAPIDA.md, FAQ.md)
- [ ] 3-5 usuarios piloto
- **Precio: USD 50 setup + USD 10-15/mes**

### Fase 2: MOBILE + SIEMPRE ACTIVO (abril - junio 2026)
- [ ] Bot Telegram — notas rápidas desde celular
- [ ] Alertas push (deadlines, cumpleaños, pendientes)
- [ ] Sincronización celular ↔ PC
- [ ] 10+ usuarios pagos

### Fase 3: MÓDULOS ESPECIALIZADOS (julio - septiembre 2026)
- [ ] Módulo entrenamiento físico
- [ ] Módulo nutrición
- [ ] Módulo profesor/tutor
- [ ] WhatsApp parser generalizado
- [ ] 20+ usuarios

### Fase 4: ESCALAR (solo si hay demanda) (2027)
- [ ] Evaluar arquitectura según usuarios reales
- [ ] SaaS / panel web / multi-tenant (solo si se justifica)
- [ ] WhatsApp Business API
- [ ] Modelo de franquicia (otros consultores usan ARGOS con sus clientes)

---

## Riesgo principal

**La dependencia de Claude Code.** ARGOS corre sobre Claude Code, que es de Anthropic. Si Anthropic cambia pricing, API, o lanza algo similar, impacta. Mitigación: el valor está en el método y la estructura, no en la plataforma. El método es migrable.

---

## Opinión del sistema (ARGOS, 18/02/2026)

> Todo lo que listaste es alcanzable porque ya lo estamos haciendo. Los 19 puntos base están probados en producción real. Los módulos 20-23 son extensiones naturales del mismo patrón.
>
> El error sería construir infraestructura (NestJS, SaaS) antes de tener un solo usuario pago. El producto ya vuela — solo falta empaquetarlo.
>
> Recomendación: definir el MVP mínimo vendible (Fase 1), construirlo en 5-6 sesiones, y salir a vender. Con feedback real de usuarios, la arquitectura se define sola.
