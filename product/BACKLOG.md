# ARGOS - Backlog de Mejoras e Ideas
*Creado: 20 de febrero de 2026*
*Actualizado: 20 de febrero de 2026*

---

## Cómo usar este archivo
- **P0** = urgente / bloqueante
- **P1** = importante, hacer pronto
- **P2** = mejora valiosa, cuando haya tiempo
- **P3** = idea a futuro / explorar

Estado: `[ ]` pendiente, `[x]` hecho, `[~]` en progreso

---

## Integraciones externas

- [ ] **P1** Integración Google Calendar — sincronizar agenda ARGOS ↔ GCal (API gratis, OAuth2)
- [ ] **P2** Integración Outlook Calendar — para usuarios corporativos (Microsoft Graph API)
- [ ] **P2** Integración Apple Calendar — CalDAV protocol
- [ ] **P2** Integración calendario genérico — export/import iCal (.ics) como mínimo viable
- [ ] **P2** Integración WhatsApp Business API — enviar/recibir mensajes programáticamente
- [ ] **P1** Bot Telegram — Fase 1 lista (send/receive/STT/TTS). Fase 2: bot autónomo con Groq

## Herramientas de documentos

- [x] **P0** Generación masiva de docs Word desde templates (doc_generator.py)
- [x] **P0** Conversión docx → PDF (pdf_converter.py)
- [x] **P0** Foliación continua de PDFs (foliador.py)
- [x] **P0** Llenado automático de formularios PDF — PyMuPDF overlay sobre PDFs del pliego
- [x] **P0** Firma digital de documentos — imagen de firma con transparencia sobre PDF
- [ ] **P2** OCR de PDFs escaneados — extraer texto de documentos escaneados
- [ ] **P2** Comparador de pliegos — diff entre versiones de pliegos/documentos
- [ ] **P3** Generación automática de Memoria Técnica desde specs + pliego

## Tracking y métricas

- [x] **P1** Tracking de horas trabajadas — registrar_sesion(), imprimir_horas()
- [x] **P1** Tracking de entrenamientos — registrar_entrenamiento(), get_entrenamientos()
- [ ] **P1** Métricas automáticas — snapshot diario/semanal (tabla metricas existe pero no se usa)
- [ ] **P2** Dashboard visual — gráficos de horas, entrenamientos, pendientes (matplotlib o web)
- [ ] **P2** Tags en eventos — categorización flexible (tabla tags existe pero no se usa)
- [ ] **P2** Reportes exportables — PDF/Excel con resumen semanal/mensual

## Agenda y calendario

- [ ] **P1** Sincronización con calendarios externos (ver Integraciones)
- [ ] **P2** Recordatorios push — notificación por Telegram cuando se acerca un deadline
- [ ] **P2** Agenda recurrente inteligente — detectar patrones (ej: gym L-M-V)
- [ ] **P3** Vista calendario web — interfaz visual del mes/semana

## Comunicación

- [~] **P1** Bot Telegram Fase 1 — enviar/recibir texto y audio (LISTO, falta testear con Hernán)
- [ ] **P2** Bot Telegram Fase 2 — bot autónomo 24/7 con Groq como cerebro
- [ ] **P2** Resumen diario automático — Telegram con agenda del día + pendientes urgentes
- [ ] **P3** Integración email — leer/enviar emails desde ARGOS

## Licitaciones (módulo core)

- [x] **P0** Análisis de precios con IVA mix (cotizacion.py)
- [x] **P0** Manipulación Excel (excel_tools.py)
- [ ] **P1** Pipeline completo de licitación — de pliego a presentación en un comando
- [ ] **P2** Extractor de requisitos de pliego — parsear PDF del pliego y armar checklist automático
- [ ] **P2** Comparador de precios entre licitaciones — histórico de cotizaciones
- [ ] **P3** Estimador de probabilidad de ganar — basado en historial + competencia

## Salud y bienestar

- [x] **P1** Registro de turnos médicos y resultados (tabla salud)
- [x] **P1** Registro de entrenamientos con intensidad
- [x] **P1** Seguimiento nutricional — tabla nutricion en DB, registro de comidas, check proteina/vegetales/suplementos, adherencia al plan
- [x] **P1** Plan nutricional cargado — opciones del plan de la nutricionista como referencia en código (imprimir_plan())
- [x] **P1** Resumen nutricional diario — get_nutricion_dia() con check de suplementos y agua
- [x] **P1** Resumen nutricional semanal — get_nutricion_semana() con % adherencia
- [ ] **P1** Lista de compras semanal — generar lista de supermercado basada en el plan nutricional (proteinas, vegetales, legumbres, suplementos, snacks, marcas recomendadas)
- [ ] **P2** Plan de entrenamiento semanal — generado según objetivos y disponibilidad
- [ ] **P2** Sugerencia de menú semanal — rotar opciones del plan para no repetir
- [ ] **P3** Integración con apps de fitness (Strava, Google Fit, Apple Health)

## Producto y comercialización

- [ ] **P0** Onboarding Natalia (usuario #2) — primera sesión lunes 23/02 noche. Definir qué necesita, armar perfil, DB separada o compartida
- [ ] **P1** Demo grabada — video de 3-5 min mostrando capacidades reales
- [ ] **P1** Rol "secretario ejecutivo" — ARGOS como asistente que organiza agenda, sigue pendientes, recuerda deadlines, redacta, consulta. Automatizar al máximo.
- [ ] **P2** Onboarding automatizado — wizard de primera sesión para nuevo usuario
- [ ] **P2** Multi-usuario — separar perfiles, cada uno con su DB y memoria
- [ ] **P3** Pricing model — definir cómo se cobra (suscripción, por uso, por módulo)

## Comunidad y ecosistema (VISIÓN ESTRATÉGICA)

> **Concepto:** Cada usuario de ARGOS crea herramientas propias para resolver sus problemas.
> Esas herramientas se pueden exportar, compartir, calificar y reutilizar por otros usuarios.
> ARGOS crece exponencialmente con las contribuciones de su comunidad.
>
> **DECISIÓN ESTRATÉGICA (20/02/2026):** Este sistema NO depende de Claude ni de ningún LLM específico.
> La curación, validación, distribución y el marketplace son infraestructura propia de AiControl (Hernán Hamra).
> El proceso debe ser AUTOMÁTICO — no manual. Eso es lo que diferencia a ARGOS de Claude Code.
> Claude (o cualquier IA) es el motor, pero el producto es la plataforma + la comunidad.
> **AiControl / Hernán Hamra es dueño del ecosistema, no Anthropic ni SBD.**

- [ ] **P1** Export de tools — que un usuario pueda empaquetar un script/tool y exportarlo
- [ ] **P1** Import de tools — instalar una tool compartida por otro usuario
- [ ] **P2** Catálogo de herramientas comunitarias — repositorio central con búsqueda por categoría
- [ ] **P2** Sistema de calificación — usuarios califican las tools (estrellas, reviews, uso)
- [ ] **P2** Validación de tools — proceso de revisión antes de publicar (automático + manual)
- [ ] **P2** Feed de herramientas nuevas — que lleguen a Hernán (o al admin) para análisis
- [ ] **P2** Versionado de tools — que las herramientas tengan versiones y se puedan actualizar
- [ ] **P3** Curador de comunidad — rol que valida calidad, seguridad y utilidad de cada tool
- [ ] **P3** Métricas de adopción — cuántos usuarios instalaron/usaron cada tool
- [ ] **P3** Herramientas premium — tools pagas creadas por usuarios avanzados (revenue share)

### Flujo imaginado
```
Usuario A tiene un problema → ARGOS le genera un script → funciona
  → Usuario A exporta la tool al catálogo
  → Otros usuarios la encuentran, la instalan, la califican
  → Las mejores tools se incorporan al core de ARGOS
  → Hernán revisa las contribuciones y decide cuáles escalan
  → La comunidad crece, ARGOS mejora sin que el equipo core haga todo
```

### Por qué es exponencial
- Cada usuario es un generador de herramientas (no solo consumidor)
- Las tools resuelven problemas reales (validados por uso)
- El catálogo crece orgánicamente
- Los usuarios de la demo también aportan desde día 1
- ARGOS se diferencia: no es una app cerrada, es una plataforma viva

---

## Definición de producto (POR RESOLVER)

> **Insight clave (20/02/2026):** El valor de ARGOS no es una app ni una feature.
> Es la capacidad de **entender un problema y generar la herramienta que lo resuelve, casi en tiempo real.**
> Es el pensamiento sistémico (del mundo IT) aplicado a TODO: salud, familia, trabajo, finanzas, organización.
> Un "secretario ejecutivo" que no solo organiza — sino que **construye soluciones nuevas sobre la marcha.**

### Qué es ARGOS realmente (para definir el producto)
- [~] **P0** Definir el pitch en 1 oración — BORRADOR:
  > **ARGOS es un asistente IA personalizado de AiControl, gestionado desde la nube, con herramientas optimizadas por la comunidad y adaptadas a todas las necesidades. Ágil de usar.**
- [ ] **P0** Definir los 3 perfiles de usuario objetivo — ¿quién lo usa? (profesional independiente, PyME, familia organizada?)
- [ ] **P1** Definir el diferencial vs alternativas — ¿por qué ARGOS y no Notion + ChatGPT + Trello?
- [ ] **P1** Definir el modelo de entrega — ¿cómo llega al usuario? (CLI, bot Telegram, web, app?)
- [ ] **P1** Definir qué se vende — ¿la plataforma? ¿las tools? ¿el servicio de secretario? ¿todo junto?

### Capacidades core que son el producto
1. **Generación de herramientas on-demand** — el usuario describe un problema, ARGOS genera el script/tool
2. **Secretario ejecutivo** — agenda, pendientes, deadlines, seguimiento, redacción, consultas
3. **Tracking integral** — horas, salud, nutrición, entrenamientos, proyectos, personas
4. **Documentación automática** — Word, PDF, Excel, formularios, foliación
5. **Memoria persistente** — ARGOS recuerda todo, conecta información, detecta patrones
6. **Comunidad de tools** — marketplace donde los usuarios comparten y mejoran herramientas

### Decisiones tomadas (20/02/2026)
- [x] **B2C directo a usuario.** AiControl factura al cliente final. No es B2B.
- [x] **El usuario NO necesita saber código.** Caja negra. Si sabe, mejor — se le ofrece más. Pero no es requisito.
- [x] **Telegram automático como primera interfaz.** La sensación de charla es clave. El usuario habla con ARGOS por Telegram.
- [x] **Ambos perfiles para arrancar:** Natalia (no-técnica, familia) + Hernán (técnico, laboral). Ver diferencias en la práctica.
- [x] **Modelo:** Suscripción mensual. Cliente paga, descarga/configura, AiControl ayuda a configurar.

### Preguntas pendientes
- [ ] ¿Cuál es el "caso de uso killer"? = la primera cosa que probás y decís "wow, esto lo necesito". Puede ser: que te organice la semana, que te haga la lista del super, que te recuerde todo. Lo vamos a descubrir con Natalia.
- [ ] **Pricing:** Claude API cuesta ~USD 20/mes al usuario. Si AiControl cobra USD 10 encima, el margen es bajo. Opciones:
  - Cobrar USD 15-25/mes de fee (total cliente: USD 35-45/mes)
  - Explorar: ¿el usuario paga la API directo o AiControl absorbe el costo y cobra todo junto?
- [ ] **Constraint: dependencia de Opus.** La capacidad de generar herramientas nuevas, entender problemas complejos y mantener contexto largo es lo que hace a ARGOS valioso — y eso hoy solo lo hace bien Opus (el modelo más caro). Modelos más baratos (Sonnet, Haiku, GPT-4o) no generan tools con la misma calidad. Esto limita bajar costos con modelos baratos. Solución futura: router inteligente (Opus para crear, Sonnet/Haiku para operar). Pero hoy el motor es caro y hay que cobrarlo acorde.
- [ ] **Constraint: dependencia de acceso al filesystem.** ARGOS genera código y trabaja con los archivos del cliente (Word, PDF, Excel, carpetas de proyectos). Esa es la parte más valiosa. Sin acceso a archivos, solo queda el rol "secretario" (agenda, recordatorios). Opciones de entrega:
  - A) Instalación local en PC del cliente (máximo poder, difícil para no-técnicos)
  - B) Telegram + API de nube (Google Drive/OneDrive) — acceso parcial, tools limitadas
  - C) Telegram solo — fácil pero pierde el diferencial de generar herramientas
  - D) Servidor remoto que accede a la nube del cliente — potente pero complejo de armar
  - **PROPUESTA DE ARQUITECTURA (20/02/2026):**
  - AiControl vende suscripciones gestionadas (todo incluido para el cliente)
  - AiControl subcontrata API Anthropic (el cliente no interactúa con Anthropic)
  - Cada cliente tiene su VM/container en nube de AiControl (ahí corren scripts, DB, tools)
  - Dashboard propio (tipo chat/secretario) reemplaza VSCode — interfaz simple para no-técnicos
  - Archivos: cliente sube al dashboard o conecta su nube (Drive/OneDrive API)
  - Comunidad y marketplace: todo en la nube, centralizado
  - **Ventajas:** cliente no instala nada, AiControl controla todo, escala con containers, margen propio
  - **Por resolver:** costo de infra (VMs), desarrollo del dashboard, integración con nubes del cliente

---

## Planificación y gestión de proyectos

- [x] **P1** Onboarding de proyecto externo — incorporar proyecto a ARGOS sin mover código (Bernasconi = caso real)
- [x] **P1** Planificación cross-life — cronograma que cruza trabajo + salud + familia + desarrollo para encontrar horas reales
- [x] **P1** Estimación de esfuerzo por fase — desglose de horas por tarea con totales
- [x] **P1** Cronograma balanceado — plan semana a semana con horas disponibles reales (no teóricas)
- [x] **P1** Carga de hitos en agenda DB — milestones de proyecto como eventos planificados
- [ ] **P1** Portfolio multi-proyecto visual — dashboard con todos los proyectos, estado, % avance, próximo hito
- [ ] **P2** Sincronización de seguimiento externo — leer archivo .md de otro proyecto y cargar novedades automáticamente
- [ ] **P2** Alertas de conflicto de agenda — detectar cuando se solapan deadlines de proyectos distintos
- [ ] **P2** Replanificación automática — si un hito se atrasa, recalcular el resto del cronograma
- [ ] **P3** Burndown chart — gráfico de avance vs plan por proyecto

## Auto-aprendizaje y mejora continua

- [x] **P0** Tabla patrones en DB — registrar patrones detectados con tipo, categoría, frecuencia, confianza
- [x] **P0** Motor de detección (tools/patterns.py) — 6 detectores de comportamiento + catálogo de 15 capacidades
- [x] **P0** Detección de capacidades usadas/nuevas/dormidas — escaneo automático de eventos
- [x] **P0** Generalización automática de funciones — registrar_funcion_nueva() + sugerir_funciones_para_perfil()
- [x] **P0** Protocolo de sesión actualizado — reporte_patrones() se ejecuta al inicio de cada sesión
- [x] **P0** Protocolo de cierre — auto-generalización obligatoria antes de registrar horas
- [ ] **P1** Sugerencias proactivas en contexto — "La última vez que hiciste X funcionó bien, ¿usamos la misma estructura?"
- [ ] **P1** Catálogo central de funciones generalizadas — servidor donde se agregan procesos de todos los usuarios
- [ ] **P1** Distribución de funciones a nuevos usuarios — al abrir sesión, sugerir funciones del catálogo según perfil
- [ ] **P2** Feedback implícito — registrar si el usuario acepta/ignora/modifica sugerencias
- [ ] **P2** Métricas de efectividad — tiempo estimado vs real, iteraciones, tasa de éxito
- [ ] **P2** Versionado de funciones — si un usuario mejora una función generalizada, propagar la mejora
- [ ] **P3** A/B testing de métodos — probar distintas formas de resolver lo mismo y medir cuál funciona mejor

## Compliance y protección de datos

- [ ] **P1** Política de privacidad — definir qué datos se recolectan, cómo se usan, cómo se protegen
- [ ] **P1** Consentimiento explícito — opt-in para compartir métricas anónimas de uso
- [ ] **P1** Encriptación de datos por usuario — cada usuario tiene su key, ni AiControl puede leer sus datos
- [ ] **P2** Habeas Data (Argentina) — cumplimiento Ley 25.326 de Protección de Datos Personales
- [ ] **P2** GDPR compliance — para usuarios internacionales (UE)
- [ ] **P2** Derecho al olvido — el usuario puede pedir borrado total de sus datos
- [ ] **P2** Auditoría de acceso — log de quién accedió a qué dato y cuándo
- [ ] **P3** Certificación ISO 27001 — estándar de seguridad de la información (largo plazo)

---

## Historial de cambios
| Fecha | Cambio |
|---|---|
| 20/02/2026 | Creación inicial del backlog con ~35 items |
| 20/02/2026 | Agregada sección Comunidad y ecosistema — visión estratégica de crecimiento exponencial |
| 20/02/2026 | Nutrición: tabla DB + 4 funciones (registrar_comida, get_dia, get_semana, imprimir_plan). Pendiente: lista de compras |
| 20/02/2026 | Natalia como usuario #2. Onboarding agendado lunes 23/02 noche. Rol secretario ejecutivo agregado al backlog |
| 20/02/2026 | Seccion "Definicion de producto" con preguntas abiertas, capacidades core, y diferencial estrategico |
| 20/02/2026 | Arquitectura cloud: suscripcion gestionada + VM por cliente + dashboard propio + API subcontratada. Backup DB a OneDrive implementado |
| 22/02/2026 | Nuevas capacidades demostradas: planificación cross-life, cronograma balanceado, onboarding proyecto externo, portfolio multi-proyecto |
| 22/02/2026 | Secciones nuevas: Planificación y gestión de proyectos, Auto-aprendizaje, Compliance y protección de datos |
| 22/02/2026 | 7 ideas de arquitectura cloud registradas en tracker DB (VM, DB encriptada, marketplace, independencia LLM, métricas con consentimiento) |
| 22/02/2026 | Motor auto-aprendizaje implementado: tabla patrones + tools/patterns.py + 6 detectores + catálogo 15 capacidades |
| 22/02/2026 | Generalización automática: registrar_funcion_nueva(), sugerir_funciones_para_perfil(), 5 perfiles base |
| 22/02/2026 | ALCANCE.md expandido: 3 niveles de auto-aprendizaje, principio proceso vs data, 16 ejemplos generalizables, moderación ética |
| 22/02/2026 | Compliance: separación proceso/data, marco legal (Ley 25.326, GDPR, CCPA), moderación ética, capas de protección |
