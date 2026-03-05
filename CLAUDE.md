# ARGOS - Asistente Personal Inteligente + Gestión de Licitaciones

## Qué es ARGOS
Sistema dual: (1) Asistente personal inteligente con tracking integral de vida y trabajo, (2) Automatización de licitaciones públicas/privadas en Argentina.
Espejo, no coach: muestra patrones, no empuja cambio. El usuario habla con ARGOS, no con agentes individuales.
Desarrollado por y para **Hernán Hamra** dentro de **Software By Design S.A.**

## Empresa
- **Razón social:** SOFTWARE BY DESIGN S.A.
- **CUIT:** 30-70894532-0
- **Domicilio legal:** Uspallata 2977 1°G, CP 1435, CABA
- **Presidente:** Ing. Marcelo Ariel Hamra (Ingeniero en Sistemas - UTN, DNI 20.665.853)
- **Apoderado:** Hernán Hamra (DNI 23.505.172)

## Reglas de trabajo (OBLIGATORIAS)
1. **NUNCA modificar archivos sin mostrar resultado y pedir confirmación** — Hernán aprueba TODO antes de que se ejecute. Sin excepción.
2. **Solo trabajar sobre lo explícitamente indicado**
3. **No inventar datos** — no fabricar datasheets, no agregar requisitos inexistentes
4. **NUNCA corregir datos (CUIT, DNI, montos) sin preguntar**
5. **Confirmar carpeta de trabajo antes de modificar**
6. **Formato argentino:** montos con $ X.XXX.XXX,XX (puntos miles, coma decimal)
7. **No tocar Excel con hojas helper** de otros proyectos
8. **PPTx en "varios"** son docs intermedios de trabajo - no tocar

## Estructura del proyecto
```
C:\Users\HERNAN\argos\
├── CLAUDE.md                 ← este archivo (reglas del proyecto)
├── tools/                    ← módulos reutilizables
│   ├── config.py            ← CONFIG CENTRALIZADO: paths, DB, tokens, plataforma (Win/Mac/Cloud)
│   ├── tracker.py           ← DB: CRUD proyectos, personas, eventos, seguimiento, agenda, salud, metas
│   ├── orquestador_sesion.py ← MOTOR PRINCIPAL: fuerza apertura/cierre por código
│   ├── parsear_respuesta.py ← "dormí 7hs" → horas_sueno=7 (expresiones argentinas)
│   ├── alertas.py           ← motor alertas rojas/amarillas, seguimientos vencidos
│   ├── aprendizaje.py       ← registrar éxitos/errores, buscar soluciones conocidas
│   ├── session.py           ← ciclo de sesión: abrir/checkpoint/cerrar
│   ├── proactivo.py         ← nudges: áreas descuidadas, reflexiones, metas inactivas
│   ├── coherencia.py        ← medir coherencia intención vs comportamiento
│   ├── patterns.py          ← detección patrones + registro funciones nuevas
│   ├── db_safety.py         ← WAL, papelera, safe_delete/safe_update
│   ├── backup.py            ← backup DB automático
│   ├── doc_generator.py     ← crear docs Word desde template
│   ├── pdf_converter.py     ← docx→PDF via Word COM
│   ├── foliador.py          ← merge PDFs + numeración de folios
│   ├── cotizacion.py        ← análisis de precios, IVA mix, álgebra inversa
│   ├── excel_tools.py       ← lectura/escritura Excel
│   ├── email_reader.py      ← lector IMAP: inbox, búsqueda, clasificación automática
│   ├── resumen_periodico.py ← resumen semanal/mensual con insights automáticos
│   ├── whatsapp_send.py     ← envío masivo WhatsApp via Baileys
│   └── seeds/               ← patrones base para nuevos usuarios
├── agents/                   ← sistema multi-agente (7 agentes + orquestador)
│   ├── orquestador.py       ← enruta consultas al agente apropiado
│   └── *.md                 ← prompts: arquitecto, comercial, data, dba, etico, neuro, ux
├── bot/                      ← Telegram bidireccional
│   ├── bridge.py            ← puente Telegram ↔ Claude Code + grabación en DB
│   ├── loop.py              ← bot principal (polling + transcripción audio)
│   ├── watcher.py           ← notifica cuando llega mensaje
│   ├── send.py / receive.py ← envío/recepción Telegram
│   ├── stt.py / tts.py      ← speech-to-text (Groq) / text-to-speech
│   └── config.py            ← tokens y chat ID
├── projects/                 ← scripts específicos por licitación/proyecto
│   ├── sbase_410_26/        ← LP 410/26 SBASE cableado
│   └── posadas_informe/     ← informes de avance Posadas
├── product/                  ← docs producto ARGOS
│   ├── SRS_ARGOS.md         ← DOCUMENTO MAESTRO ÚNICO (1085 líneas, 12 secciones)
│   ├── MEMORY_TEMPLATE.md   ← template base para nuevos usuarios
│   ├── PROTOCOLO_WHATSAPP_MASIVO.md ← manual operativo WhatsApp
│   └── archivo_historico/   ← backup de 13 archivos absorbidos por el SRS
├── templates/                ← templates .docx reutilizables
├── data/                     ← argos_tracker.db (NO va a git)
└── output/                   ← archivos temporales generados
```

## Fuente de verdad: la DB
- **`data/argos_tracker.db`** (SQLite) es la ÚNICA fuente de datos
- Si necesito datos → consultar DB. Si necesito registrar → escribir en DB
- Tablas principales: proyectos, personas, eventos, seguimiento, agenda, bienestar, metas, mensajes, patrones, metricas_sesion
- **Personas** tienen: empresa, cargo, contacto, perfil_comportamiento, DNI, CUIT
- **Seguimientos** siempre con persona_id asignada (quién debe qué)

## Stack técnico
- **Python 3.12.1** en C:\Python312 (usar `python`, NO `python3`)
- **SQLite** con WAL mode para concurrencia
- **python-docx + lxml**: manipulación .docx a nivel XML
- **win32com.client**: Word COM automation para docx→PDF (SIEMPRE `taskkill /f /im WINWORD.EXE` antes)
- **PyMuPDF (fitz)**: merge PDF, foliación, extracción texto
- **openpyxl**: Excel (data_only=True para valores, False para fórmulas)
- **python-telegram-bot**: Telegram bidireccional
- **Groq API**: speech-to-text para audios Telegram
- **requests**: descarga de datasheets
- **Baileys (Node.js)**: WhatsApp masivo

## Capacidades del sistema
| Capacidad | Herramientas |
|---|---|
| Asesoramiento personal (espejo, patrones, reflexiones) | tracker.py, proactivo.py, coherencia.py |
| Licitaciones públicas (docs, precios, foliación) | doc_generator, foliador, cotizacion, pdf_converter |
| Tracking integral (proyectos, personas, seguimiento) | tracker.py — seguimientos con persona_id asignada |
| Perfiles de comportamiento por persona | personas.perfil_comportamiento — guía tono de comunicación |
| Bienestar diario (humor, energía, estrés, sueño) | tracker.py (tabla bienestar), checkpoints |
| Gestión de metas (personal, profesional, formación) | tracker.py (tabla metas), coherencia.py |
| Facturación recurrente mensual | seguimientos recurrentes con alertas |
| Telegram bidireccional | bot/loop.py, bridge.py, watcher.py |
| Multi-agente (7 agentes invisibles) | agents/orquestador.py |
| Auto-aprendizaje | .claude/hooks/auto_aprendizaje.py, patterns.py |
| Marketing masivo WhatsApp | whatsapp_send.py, wapp_baileys/ |
| Nutrición y salud | tracker.py (tablas salud, nutricion) |

## Catálogo de capacidades
- **Fuente de verdad:** DB (`SELECT * FROM patrones WHERE tipo LIKE 'protocolo_%' AND estado='validado'`)
- **Estado actual:** 107 protocolos validados en 15 tipos de protocolo
- **Documento de referencia:** `product/SRS_ARGOS.md` sección 6
- Si ARGOS aprende capacidad nueva: registrar en patrones → actualizar MEMORY.md → exportar seed → git push

## Patrones técnicos clave

### Paths de OneDrive
- Siempre usar raw strings `r''` en Python
- NUNCA usar heredoc en bash para paths con caracteres españoles (ó, é, í)
- Los .docx originales suelen estar en subcarpeta `varios/`, los .pdf en la carpeta principal

### Documentos Word (licitaciones)
- Template: usar una DDJJ existente como base (preserva header/footer con membrete)
- `tools/doc_generator.py` tiene `load_template()`, `add_para()`, `add_separator()`
- Para modificar .docx existente: buscar en `doc.paragraphs` Y `doc.tables` por separado
- Reemplazar en `run.text` (no en `p.text`) para preservar formato

### Análisis de Precios (Anexo VII)
- Cadena: Costo Directo → Gastos Generales → CF → Beneficio → IVA → Total
- IVA es MIX de 21% (servicios/materiales) y 10.5% (equipamiento informático)
- Trabajar hacia atrás desde el total para despejar Gastos Generales
- `tools/cotizacion.py` tiene `calcular_anexo_vii()` y `calcular_iva_mix()`

### Foliación
- `tools/foliador.py` tiene `merge_and_foliate()`
- Agregar "Folio: X" en bottom-right, fontsize 9, color gris
- Foliación continua entre carpetas (A1→A2→B→C)

## Estructura estándar de licitación
- **Carpeta A1** - Documentación Legal
- **Carpeta A2** - Información Económico-Financiera
- **Carpeta B** - Documentación Técnica
- **Carpeta C** - Oferta Económica

## Marcas con datasheets descargables
- **Furukawa** (lightera.com): Cat6A, FO OM3, ODF, faceplates, patch panels
- **Panduit**: Racks 42U
- **Ubiquiti** (ui.com): Switches, APs, Gateways
- **Grandstream**: Centrales IP, teléfonos, gateways FXO
- **Kaise**: UPS rack

## Problemas conocidos
| Problema | Solución |
|----------|----------|
| Encoding español en paths OneDrive | Python scripts con r'', nunca heredoc |
| OneDrive bloquea archivos | Reintentar con sleep, o pedir cerrar |
| .docx desaparece | Buscar en subcarpeta `varios/` |
| PDFs vacíos (0 bytes) | Skip con getsize() > 0 |
| Excel PermissionError | Cerrar Excel, esperar sync, reintentar |
| Floating point en cadena Excel | Celda de cierre referenciando target |
| DB locked | WAL mode + reintentar. Cerrar procesos Python zombie |
| Telegram no arranca | Verificar .env con BOT_TOKEN y CHAT_ID |
