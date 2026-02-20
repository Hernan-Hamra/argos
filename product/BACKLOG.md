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
- [ ] **P2** Plan de entrenamiento semanal — generado según objetivos y disponibilidad
- [ ] **P2** Seguimiento nutricional — registro de comidas, calorías estimadas
- [ ] **P3** Integración con apps de fitness (Strava, Google Fit, Apple Health)

## Producto y comercialización

- [ ] **P1** Demo grabada — video de 3-5 min mostrando capacidades reales
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

## Historial de cambios
| Fecha | Cambio |
|---|---|
| 20/02/2026 | Creación inicial del backlog con ~35 items |
| 20/02/2026 | Agregada sección Comunidad y ecosistema — visión estratégica de crecimiento exponencial |
