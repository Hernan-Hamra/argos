# ARGOS - Catálogo de Funciones
*Generado desde DB sistema | 32 capacidades | 22 de febrero de 2026*

---

## Resumen

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| **CON TOOL** | 20 | Usa scripts Python, librerías o APIs dedicadas |
| **SIN TOOL (LLM)** | 12 | El LLM resuelve directo sin script — análisis, redacción, estrategia |
| **Total** | **32** | Catálogo dinámico — crece con cada interacción exitosa |

---

## 1. ANÁLISIS (8 funciones)

### 1.1 Análisis de precios — CON TOOL
- **Herramienta:** `tools/cotizacion.py`
- **Protocolo:**
  1. Leer estructura de costos
  2. Calcular IVA mix 21% / 10.5%
  3. Álgebra inversa desde total
  4. Generar Excel
- **Cuándo se usa:** Licitaciones, presupuestos, Anexo VII
- **Perfiles:** pyme, técnico

### 1.2 Herramientas Excel — CON TOOL
- **Herramienta:** `tools/excel_tools.py` (openpyxl)
- **Protocolo:**
  1. Leer con openpyxl (data_only para valores, False para fórmulas)
  2. Cruce de datos entre hojas/archivos
  3. Escribir con formato y colores
- **Cuándo se usa:** Cualquier planilla, comparativos, materiales, presupuestos
- **Perfiles:** pyme, técnico

### 1.3 Extracción de datos — CON TOOL
- **Herramienta:** `tools/pdf_converter.py` + pymupdf
- **Protocolo:**
  1. Extraer texto de PDF
  2. Parsear estructura (tablas, listas)
  3. Normalizar datos
- **Cuándo se usa:** Remitos escaneados, pliegos, documentos de terceros
- **Perfiles:** pyme, técnico

### 1.4 Análisis de cadenas WhatsApp — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Recibir texto del chat (copy-paste o export)
  2. Identificar participantes
  3. Extraer cronología de hechos
  4. Detectar pendientes y decisiones
  5. Generar resumen ejecutivo
- **Cuándo se usa:** Reconstruir qué pasó en un grupo/chat, detectar compromisos
- **Perfiles:** profesional independiente, pyme

### 1.5 Lectura y análisis de pliegos — CON TOOL
- **Herramienta:** LLM + pymupdf
- **Protocolo:**
  1. Leer PDF del pliego completo
  2. Identificar requisitos obligatorios vs opcionales
  3. Detectar excluyentes
  4. Armar checklist de cumplimiento
- **Cuándo se usa:** Evaluación de licitaciones antes de decidir si presentarse
- **Perfiles:** técnico, pyme

### 1.6 Lectura de remitos escaneados — CON TOOL
- **Herramienta:** LLM + pymupdf
- **Protocolo:**
  1. Recibir PDF/imagen escaneado
  2. Extraer texto (OCR visual)
  3. Parsear ítems y cantidades
  4. Cruzar con pedido original
  5. Generar tabla comparativa
- **Cuándo se usa:** Control de entregas, verificar que llegó lo pedido
- **Perfiles:** técnico, pyme

### 1.7 Dashboard y gráficos — CON TOOL
- **Herramienta:** matplotlib + seaborn
- **Protocolo:**
  1. Consultar datos de DB
  2. Definir métricas clave
  3. Generar gráficos (barras, líneas, pie)
  4. Exportar como imagen
- **Cuándo se usa:** Visualizar métricas, informes con gráficos
- **Perfiles:** profesional independiente, pyme

### 1.8 Investigación técnica — SIN TOOL
- **Herramienta:** LLM + web search
- **Protocolo:**
  1. Identificar producto/tecnología a investigar
  2. Buscar specs reales de fabricante
  3. Comparar opciones
  4. Recomendar con fundamento
- **Cuándo se usa:** Elegir equipamiento, verificar compatibilidad, armar specs
- **Perfiles:** técnico, pyme
- **REGLA:** No inventar datasheets — solo datos reales de fabricante

---

## 2. ASESORÍA (4 funciones)

### 2.1 Elaboración de estrategias — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Mapear actores y sus dinámicas
  2. Analizar posiciones e intereses
  3. Proponer acciones concretas
  4. Evaluar riesgos de cada opción
- **Cuándo se usa:** Conflictos laborales, negociaciones, decisiones complejas
- **Perfiles:** profesional independiente

### 2.2 Planificación cross-life — SIN TOOL
- **Herramienta:** LLM + tracker.py (consulta)
- **Protocolo:**
  1. Relevar todas las áreas de vida (trabajo, salud, familia, desarrollo)
  2. Asignar horas disponibles por semana
  3. Cruzar compromisos y prioridades
  4. Generar cronograma balanceado
- **Cuándo se usa:** Organización semanal, cuando hay muchas cosas encima
- **Perfiles:** profesional independiente

### 2.3 Análisis de dinámicas interpersonales — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Relevar actores involucrados
  2. Mapear dinámicas de poder
  3. Detectar patrones de comportamiento recurrentes
  4. Proponer estrategia de acción
- **Cuándo se usa:** Relaciones laborales complicadas, entender motivaciones
- **Perfiles:** profesional independiente

### 2.4 Apoyo en toma de decisiones — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Presentar opciones claras
  2. Analizar pros/contras de cada una
  3. Evaluar riesgos
  4. Recomendar con fundamento
  5. Dejar decisión final al usuario
- **Cuándo se usa:** Antes de decisiones importantes (cambio laboral, inversión, proyecto)
- **Perfiles:** profesional independiente, pyme

---

## 3. COMUNICACIÓN (5 funciones)

### 3.1 Redacción calibrada (general) — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Analizar contexto y relación con destinatario
  2. Calibrar tono (formal/firme/cordial/informal)
  3. Generar versiones (suave → firme)
  4. Confirmar con usuario antes de enviar
- **Cuándo se usa:** Cualquier comunicación que requiera tacto
- **Perfiles:** profesional independiente, pyme

### 3.2 Redacción de emails formales — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Analizar contexto y destinatario
  2. Calibrar tono según situación
  3. Redactar con estructura (asunto, cuerpo, cierre)
  4. Ofrecer versiones
  5. Confirmar
- **Cuándo se usa:** Pedidos formales, reclamos, informes, seguimiento
- **Perfiles:** profesional independiente, pyme

### 3.3 Redacción de WhatsApp — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Identificar destinatario y relación
  2. Adaptar tono (informal/profesional/grupal)
  3. Redactar conciso y directo
  4. Confirmar
- **Cuándo se usa:** Mensajes individuales o grupos, coordinación, pedidos
- **Perfiles:** profesional independiente, pyme, familia

### 3.4 Cotización a proveedores — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Identificar ítems a cotizar
  2. Redactar pedido formal
  3. Incluir specs técnicas
  4. Solicitar plazo y condiciones
- **Cuándo se usa:** Pedir precios a proveedores para licitaciones o compras
- **Perfiles:** pyme, técnico

### 3.5 Bot Telegram — CON TOOL
- **Herramienta:** `tools/telegram_bot.py`
- **Protocolo:**
  1. Recibir mensaje (texto o audio)
  2. STT si es audio (Groq/Whisper)
  3. Procesar con LLM
  4. Responder texto + TTS
- **Cuándo se usa:** Interacción desde celular, manos libres, en movimiento
- **Perfiles:** profesional independiente

---

## 4. DOCUMENTOS (7 funciones)

### 4.1 Generación de documentos Word — CON TOOL
- **Herramienta:** `tools/doc_generator.py` (python-docx)
- **Protocolo:**
  1. Cargar template .docx con membrete
  2. Reemplazar placeholders en runs (no en p.text)
  3. Generar PDF via Word COM
- **Variantes por plataforma:**
  - **Windows:** Word COM (win32com) para docx→PDF
  - **Mac:** LibreOffice CLI o Pages export
  - **Linux:** LibreOffice headless
- **Cuándo se usa:** DDJJs, notas, CVs, carátulas, cualquier doc formal
- **Perfiles:** pyme, técnico, profesional independiente

### 4.2 Foliación de PDFs — CON TOOL
- **Herramienta:** `tools/foliador.py` (pymupdf)
- **Protocolo:**
  1. Merge PDFs por carpeta (A1→A2→B→C)
  2. Agregar overlay "Folio: N" en bottom-right
  3. Numeración continua entre carpetas
  4. Skip archivos vacíos (0 bytes)
- **Cuándo se usa:** Licitaciones (obligatorio foliar toda la presentación)
- **Perfiles:** técnico

### 4.3 PDF overlay (formularios) — CON TOOL
- **Herramienta:** pymupdf directo
- **Protocolo:**
  1. Leer PDF base (formulario del pliego)
  2. Insertar texto en coordenadas x,y
  3. Guardar PDF con overlay
- **Cuándo se usa:** Completar formularios del pliego sin editarlos
- **Perfiles:** técnico

### 4.4 Notas con membrete — CON TOOL
- **Herramienta:** `tools/doc_generator.py`
- **Protocolo:**
  1. Cargar template con membrete de empresa
  2. Completar datos del destinatario
  3. Redactar cuerpo
  4. Generar PDF
- **Cuándo se usa:** Autorizaciones, notas formales, declaraciones
- **Perfiles:** pyme, técnico

### 4.5 Documentación de producto — SIN TOOL
- **Herramienta:** LLM directo
- **Protocolo:**
  1. Relevar estado actual del producto/proyecto
  2. Estructurar documento (secciones)
  3. Redactar en markdown
  4. Iterar con usuario hasta aprobación
- **Cuándo se usa:** README, plan de negocio, competencia, método, backlog
- **Perfiles:** profesional independiente, pyme

### 4.6 Firma automática en PDFs — CON TOOL
- **Herramienta:** pymupdf directo
- **Protocolo:**
  1. Recibir imagen de firma (JPG/PNG)
  2. Convertir a PNG transparente si necesario
  3. Insertar en coordenadas del PDF
  4. Guardar PDF firmado
- **Cuándo se usa:** Firmar documentos masivamente sin imprimir
- **Perfiles:** profesional independiente, pyme, técnico

### 4.7 Informes de gestión — CON TOOL
- **Herramienta:** LLM + `tools/excel_tools.py`
- **Protocolo:**
  1. Definir período del informe
  2. Consultar eventos del período (tracker DB)
  3. Estructurar informe (resumen, detalle, métricas)
  4. Generar documento (Word/Excel/markdown)
- **Cuándo se usa:** Informes mensuales, reportes de avance de obra
- **Perfiles:** profesional independiente, pyme, técnico

---

## 5. TRACKING (4 funciones)

### 5.1 Tracking y seguimiento — CON TOOL
- **Herramienta:** `tools/tracker.py`
- **Protocolo:**
  1. Registrar evento en DB (fecha, tipo, subtipo, descripción)
  2. Clasificar por tipo/subtipo
  3. Vincular a proyecto y persona
- **Cuándo se usa:** Todo el tiempo — cada interacción relevante se registra
- **Perfiles:** todos

### 5.2 Agenda y calendario — CON TOOL
- **Herramienta:** `tools/tracker.py::add_agenda`
- **Protocolo:**
  1. Registrar evento futuro
  2. Calcular recordatorios (N días antes)
  3. Alertar al inicio de sesión
- **Cuándo se usa:** Turnos médicos, deadlines, reuniones, compromisos
- **Perfiles:** todos

### 5.3 Onboarding de proyectos — CON TOOL
- **Herramienta:** `tools/tracker.py::add_proyecto`
- **Protocolo:**
  1. Relevar proyecto existente (qué es, estado, personas)
  2. Crear en DB
  3. Vincular personas y seguimiento
- **Cuándo se usa:** Incorporar un proyecto nuevo al seguimiento de ARGOS
- **Perfiles:** profesional independiente, pyme

### 5.4 Gestión de materiales (obra) — CON TOOL
- **Herramienta:** `tools/excel_tools.py` + LLM
- **Protocolo:**
  1. Leer pedido original (Excel/PDF)
  2. Leer remitos de entrega
  3. Cruzar cantidades
  4. Detectar faltantes
  5. Generar Excel comparativo con colores
- **Cuándo se usa:** Control de entregas en obra, verificar que no falte nada
- **Perfiles:** técnico

---

## 6. SALUD (1 función)

### 6.1 Seguimiento nutricional — CON TOOL
- **Herramienta:** `tools/tracker.py::registrar_comida`
- **Protocolo:**
  1. Registrar comida del día (desayuno/almuerzo/merienda/cena/snack)
  2. Evaluar adherencia al plan (del plan sí/no, proteína, vegetales)
  3. Reportes diarios y semanales
- **Cuándo se usa:** Seguimiento diario de alimentación
- **Perfiles:** salud, familia

---

## 7. SISTEMA (2 funciones)

### 7.1 Backup automático — CON TOOL
- **Herramienta:** `tools/backup.py`
- **Protocolo:**
  1. Copiar DBs a OneDrive
  2. Rotación de backups (mantener últimos N)
  3. Verificar integridad
- **Variantes por plataforma:**
  - **Windows:** Copia a OneDrive personal
  - **Mac:** Copia a iCloud Drive o carpeta local
  - **Linux:** Copia a carpeta configurada
- **Cuándo se usa:** Al cierre de cada sesión (obligatorio)
- **Perfiles:** todos

### 7.2 Creación de estructura de carpetas — SIN TOOL
- **Herramienta:** LLM + bash/python (os.makedirs)
- **Protocolo por plataforma:**
  - **Windows:** Diseñar → Crear con os.makedirs() → Verificar en OneDrive
  - **Mac:** Diseñar → Crear con os.makedirs() → Verificar en iCloud
  - **Linux:** Diseñar → Crear con os.makedirs()
- **Cuándo se usa:** Nuevo proyecto, organizar documentación
- **Perfiles:** profesional independiente, pyme, técnico

---

## 8. FINANZAS (1 función)

### 8.1 Control de gastos familiares — CON TOOL
- **Herramienta:** `tools/tracker.py` + nuevo módulo
- **Protocolo:**
  1. Definir categorías de gasto
  2. Registrar gasto con fecha + monto + categoría
  3. Reporte semanal/mensual
- **Estado:** propuesta (no implementada aún)
- **Perfiles:** familia, profesional independiente

---

## Resumen por tipo de herramienta

### Tools Python dedicados
| Tool | Funciones que lo usan |
|------|----------------------|
| `tools/tracker.py` | Tracking, Agenda, Onboarding, Nutrición, Gastos |
| `tools/doc_generator.py` | Generación docs, Notas membrete |
| `tools/excel_tools.py` | Excel, Materiales, Informes |
| `tools/cotizacion.py` | Análisis de precios |
| `tools/foliador.py` | Foliación PDFs |
| `tools/pdf_converter.py` | Extracción de datos |
| `tools/backup.py` | Backup |
| `tools/telegram_bot.py` | Bot Telegram |
| `tools/patterns.py` | Auto-aprendizaje (detección patrones) |
| `tools/db_manager.py` | Gestión DBs sistema/usuario |

### Librerías externas
| Librería | Funciones que la usan |
|----------|----------------------|
| pymupdf (fitz) | Foliación, PDF overlay, Firma PDF, Extracción |
| openpyxl | Excel, Materiales, Informes, Precios |
| python-docx | Generación docs, Notas |
| win32com | Conversión docx→PDF (solo Windows) |
| matplotlib | Dashboard y gráficos |

### LLM directo (sin tool)
| Función | Qué hace el LLM solo |
|---------|----------------------|
| Redacción calibrada | Escribe con tono adecuado |
| Redacción emails | Emails formales con estructura |
| Redacción WhatsApp | Mensajes directos y concisos |
| Análisis WhatsApp | Parsea chats, extrae info |
| Cotización proveedores | Pedidos formales |
| Estrategias | Mapea actores, propone acciones |
| Dinámicas interpersonales | Analiza relaciones |
| Toma de decisiones | Evalúa opciones |
| Planificación cross-life | Balancea vida |
| Documentación producto | Redacta docs técnicos |
| Investigación técnica | Busca specs reales |
| Estructura carpetas | Diseña organización |

---

## Ciclo de vida de una función

```
PEDIDO USUARIO → ARGOS detecta si es NUEVA / CONOCIDA / MEJORA
         ↓
    [NUEVA] → Registra en catálogo con herramienta + protocolo
    [CONOCIDA] → Incrementa contador de uso
    [MEJORA] → Crea nueva versión, conserva historial
         ↓
  Al cierre de sesión:
    - Documenta interacción
    - Evalúa si es generalizable
    - Si sí → Disponible para otros usuarios del mismo perfil
    - SE COMPARTE EL PROCESO, NUNCA LA DATA
```

---

*Este documento se genera dinámicamente desde la tabla `capacidades` en `argos_sistema.db`.*
*Catálogo vivo: crece con cada sesión exitosa.*
