# ARGOS - Alcance del Producto
*Definido: 18 de febrero de 2026*

---

## Visión

ARGOS es un asistente personal con IA que te conoce, te organiza, te asesora, te entrena y construye herramientas a medida. No es una app con botones — es una conversación con alguien que sabe todo de vos y puede resolver lo que le pidas.

---

## Alcance completo (19 capacidades)

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

### Módulos especializados (futuros)
20. **Entrenamiento físico** — planes de entrenamiento, seguimiento de actividad, métricas deportivas (tipo Tup)
21. **Nutrición** — planes alimentarios, lista de compras, seguimiento de dieta, presupuesto
22. **Profesor / tutor** — charlas específicas sobre cualquier tema, explicaciones adaptadas al nivel del usuario
23. **Salud** — turnos médicos, estudios, tratamientos, seguimiento de evolución

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
