# Especificacion de Requisitos de Software - ARGOS

**Nombre del proyecto:** ARGOS - Asistente Personal Inteligente
**Fecha:** 2026-03-05
**Version:** 0.8 (Clasificacion seguimientos 2 ejes, auto-clasificacion por codigo, vista agrupada apertura, status proyectos laboral/personal)
**Autor:** Hernan Hamra / ARGOS
**Producto de:** AiControl (proyecto personal de Hernan Hamra)
**Empresa del autor:** SOFTWARE BY DESIGN S.A. (CUIT 30-70894532-0)

---

| Version | Autor                | Descripcion                                                                      | Fecha      |
|---------|----------------------|----------------------------------------------------------------------------------|------------|
| 0.1     | Hernan Hamra + ARGOS | Relevamiento inicial desde DB (1.564 mensajes, 20+ seguimientos, 15 docs producto) | 2026-03-04 |
| 0.2     | Hernan Hamra + ARGOS | Documento maestro unificado. Absorbe 13 archivos de product/ en un solo SRS.     | 2026-03-04 |
| 0.3     | Hernan Hamra + ARGOS | Arquitectura local-first, interfaz web, modelo herramientas comunidad, infraestructura, AiControl como marca. | 2026-03-04 |
| 0.4     | Hernan Hamra + ARGOS | Sandboxing produccion (5 capas), matriz de riesgos, proteccion legal (T&C, seguro E&O, compliance). | 2026-03-04 |
| 0.5     | Hernan Hamra + ARGOS | Roadmap v2 basado en auditoria real. Fase 0 cimientos (orquestador sesion, parseo, nudges, aprendizaje). 6 fases hasta lanzamiento junio 2026. | 2026-03-04 |
| 0.6     | Hernan Hamra + ARGOS | Config centralizado (Win/Mac/Cloud), motor de rutinas (5 seed), email IMAP reader, resumen semanal/mensual, learning loop cerrado (consultar_catalogo), scheduler rutinas en hooks+Telegram. 3 bugs fix. Auditoria: 28/49 req DONE (57%), 0 gaps ROJOS. | 2026-03-04 |
| 0.7     | Hernan Hamra + ARGOS | Sistema de clasificacion de seguimientos: 2 ejes (responsable yo/otro × 9 tipos). Auto-clasificacion por codigo con confianza. Vista agrupada en apertura: Mis Compromisos, Compromisos de Terceros, Vencimientos. Status por proyecto laboral/personal. | 2026-03-05 |
| 0.8     | Hernan Hamra + ARGOS | ARGOS es espejo + coach. Fase 6 coaching. Transparencia 3 fuentes (LLM 40% + DB 35% + contexto 25%). Criterio de decision. 3 capas de confianza del cliente. Metricas de rendimiento por sesion (9 columnas nuevas en metricas_sesion). Perfil psicologico del usuario (8 rasgos con evidencia). | 2026-03-05 |

---

## Indice

1. [Introduccion](#1-introduccion)
2. [Requisitos Funcionales](#2-requisitos-funcionales)
3. [Requisitos de Interfaz](#3-requisitos-de-interfaz)
4. [Requisitos No Funcionales](#4-requisitos-no-funcionales)
5. [Arquitectura y Decisiones Tecnicas](#5-arquitectura-y-decisiones-tecnicas)
6. [Catalogo de Capacidades](#6-catalogo-de-capacidades)
7. [Negocio y Competencia](#7-negocio-y-competencia)
8. [Backlog de Bugs y Deuda Tecnica](#8-backlog-de-bugs-y-deuda-tecnica)
9. [Roadmap por Fases](#9-roadmap-por-fases)
10. [Casos de Uso](#10-casos-de-uso)
11. [Metodo ARGOS](#11-metodo-argos)
12. [Definiciones y Acronimos](#12-definiciones-y-acronimos)

---

## 1. Introduccion

### 1.1 Proposito del documento

Documento maestro unico de ARGOS como producto de software. Consolida:
- 1.564 mensajes en caja negra (feb-mar 2026)
- 20+ seguimientos pendientes sobre el producto
- 13 documentos de producto unificados (BACKLOG, ALCANCE, PLAN_NEGOCIO, COMPETENCIA, DECISIONES, FLUJO, METODO, CASOS_DE_USO, FUNCIONES, MIGRACION_NUBE, ANALISIS_BUGS, PROMPT_SISTEMA, README)
- 107 protocolos validados en DB (tabla `patrones`)
- 12 metas activas del usuario/creador
- Feedback de Natalia (primera clienta piloto)

**Problema central:** ARGOS registra bien (caja negra, eventos, seguimientos) pero **falla en el seguimiento proactivo** de rutinas diarias, proyectos y personas. Los protocolos dependen de la interpretacion del LLM en lugar de estar implementados por codigo.

**Fuente de verdad de capacidades:** La DB (`SELECT * FROM patrones WHERE tipo LIKE 'protocolo_%' AND estado='validado'`). Este documento es referencia, la DB es la verdad.

### 1.2 Alcance del producto

> **ARGOS es un asistente de gestion integral con inteligencia relacional.**
> Sabe quien sos, sabe con quien tratas, sabe como tratar a cada uno,
> y sabe que tenes pendiente con cada persona en cada proyecto.

**El nombre:** En la *Odisea* de Homero, **Argos** es el perro de Ulises. Espero 20 anos el regreso de su amo. Cuando Ulises volvio disfrazado de mendigo, nadie lo reconocio — excepto Argos. Movio la cola, lo miro, y murio en paz. Es la escena mas conmovedora de la literatura antigua. Borges retoma a Argos en *"El Inmortal"* (de *El Aleph*): un perro que aparece cerca de la Ciudad de los Inmortales, testigo silencioso, fiel mas alla del tiempo. *El nombre nacio de una lectura de Borges. Como todo en ARGOS: de la literatura a la tecnologia, de lo humano a lo practico.*

ARGOS hereda esa fidelidad: te reconoce (sabe quien sos), te espera (memoria persistente), es fiel (trackea lo que importa), crece con vos (la relacion se profundiza con el tiempo).

**Que es:**
- Asistente de gestion integral (trabajo + salud + personas + metas + emociones)
- Con inteligencia relacional (perfil de comportamiento por persona, sabe como comunicarte con cada uno)
- Espejo, no coach (muestra patrones, no empuja cambio)
- App local con interfaz web (chat + file browser + paneles de herramientas)
- Local-first: los datos y archivos NUNCA salen de la PC del usuario
- Los usuarios programan herramientas hablando con Claude. AiControl cuida y comparte las mejores.

**Que NO es:**
- No es un CRM (es mas que eso — un CRM registra datos, ARGOS entiende personas)
- No es un coach (no te dice que hacer, te muestra que haces)
- No es un chatbot generico (tiene tu DB, tu historia, tu contexto)
- No es un software que instalas y listo — es una conversacion con alguien que sabe todo de vos
- No es una app cloud — corre en la PC del usuario, la nube solo asiste

| Capacidad                              | CRM tradicional               | ARGOS                                                       |
|----------------------------------------|-------------------------------|-------------------------------------------------------------|
| Registra contactos y actividades       | Si                            | Si + contexto + comportamiento                              |
| Te dice QUE hacer                      | Si                            | Te dice QUE, COMO y CON QUIEN                               |
| Alcance                               | Solo clientes/prospectos       | Clientes + familia + socios + proveedores + vos mismo       |
| Perfiles de comportamiento             | No                            | Si — guia tono y estrategia de comunicacion por persona     |
| Carga de datos                         | Formularios manuales          | Conversacion natural (texto y audio)                        |
| Seguimiento personal (salud, metas)    | No                            | Si — bienestar, nutricion, metas, coherencia                |
| Aprende de la comunidad                | No                            | Si — protocolos y herramientas compartidas entre usuarios    |

**Modos de uso:**

| Modo                     | Descripcion                                                                      | Estado         |
|--------------------------|----------------------------------------------------------------------------------|----------------|
| **Asistente personal**   | Tracking integral de vida: trabajo, salud, personas, metas, emociones, rutinas   | MVP operativo  |
| **Herramientas SBD**     | Licitaciones, documentos, cotizaciones, foliacion, mailing masivo                | Operativo      |
| **Producto comercial**   | Multi-usuario, suscripcion, cloud, onboarding automatizado                       | En definicion  |

**Objetivos del producto:**
- O1: Que el seguimiento de rutinas, proyectos y personas sea por codigo, no por memoria
- O2: Que cada usuario tenga su DB encriptada e independiente
- O3: Que ARGOS corra local en la PC de cada usuario (local-first, cloud-assisted)
- O4: Que el onboarding de un nuevo usuario sea automatizado (< 10 min)
- O5: Que las herramientas (WhatsApp, docs, etc.) sean modulos empaquetados e independientes

**Metas medibles:**
- M1: 0 olvidos de seguimiento por sesion (hoy: ~2-3 por sesion)
- M2: Checkpoint de apertura/cierre ejecutado 100% de las veces (hoy: ~70%)
- M3: 2 usuarios pagos operativos para marzo 2026 (Natalia + 1)
- M4: Deploy en servidor cloud funcional para abril 2026

### 1.3 Valor del producto

| Valor                          | Descripcion                                                                                         |
|--------------------------------|-----------------------------------------------------------------------------------------------------|
| **Continuidad**                | Nunca se pierde contexto. Todo queda en DB. Cada sesion retoma donde termino la anterior.           |
| **Inteligencia relacional**    | Perfil de comportamiento por persona. Te dice como hablarle a cada uno segun su historial.          |
| **Espejo inteligente**         | Detecta patrones de comportamiento y los muestra sin juzgar.                                        |
| **Automatizacion real**        | Genera documentos, envia WhatsApp masivos, calcula precios de licitaciones, folia PDFs.             |
| **Privacidad total**           | DB local/encriptada por usuario. Sin telemetria. Los datos son del usuario.                         |
| **Comunidad de conocimiento**  | Cuando un usuario resuelve un problema, ARGOS lo empaqueta como protocolo. Otros usuarios acceden a esa solucion. El sistema crece con cada usuario. |
| **Efecto acumulativo (moat)**  | Cuanto mas lo usas, mas te conoce, mas valor tiene. Lock-in por valor, no por candado.              |
| **Interfaz web local**         | App local con chat + file browser + paneles. Accesible desde browser o app Tauri. Archivos nunca salen de la PC. |

### 1.4 Publico objetivo

| Perfil                           | Descripcion                                                                                | Ejemplo            |
|----------------------------------|--------------------------------------------------------------------------------------------|---------------------|
| **Profesional independiente**    | Persona con multiples proyectos, clientes y areas de vida que gestionar                    | Hernan              |
| **Pequeno empresario**           | Dueno de empresa chica que necesita tracking de clientes, seguimientos, facturacion         | Natalia (AiControl) |
| **Profesional tecnico**          | Persona que trabaja con licitaciones, documentos tecnicos, presupuestos                    | Equipo SBD          |

**NO es para:** empresas grandes con ERP, personas que necesitan solo un CRM basico.

### 1.5 Uso previsto

El usuario interactua con ARGOS de tres formas:

1. **App web (interfaz principal):** Chat + file browser + paneles. Desde PC via browser o app Tauri. Acceso directo al filesystem local.
2. **Telegram:** Mensajes de texto y audio desde el celular. Canal adicional bidireccional.
3. **WhatsApp:** Canal adicional bidireccional (futuro).

**Flujo tipico de un dia:**
```
08:00  Apertura via app web (PC) o Telegram (celular)
       -> Checkpoint: como dormiste? energia? humor?
       -> Resumen de ayer + pendientes + agenda
       -> "En que trabajamos hoy?"

09:00  Trabajo (app web): licitaciones, documentos, seguimientos
       -> Arrastra PDFs al file browser para foliar
       -> Usa panel de herramientas para cotizacion
12:30  Telegram: "almorce ensalada y pollo"
       -> ARGOS registra en nutricion
15:00  Telegram audio: "me llamo fulano, necesita X"
       -> ARGOS registra seguimiento con persona

20:00  Cierre
       -> Checkpoint: que salio bien? que frustro?
       -> Resumen diario -> caja negra -> backup
```

### 1.6 Descripcion general

ARGOS es un sistema de 4 capas:

```
CAPA 4: INTERFAZ
  App web local (Tauri/browser) + Telegram + WhatsApp (canales adicionales)

CAPA 3: INTELIGENCIA
  LLM (Claude) + 7 agentes invisibles (orquestador.py)
  Auto-aprendizaje (patterns.py + auto_aprendizaje.py)

CAPA 2: HERRAMIENTAS (tools/)
  tracker.py | doc_generator.py | foliador.py | cotizacion.py
  pdf_converter.py | excel_tools.py | whatsapp_send.py | backup.py

CAPA 1: DATOS
  argos_tracker.db (SQLite) — 27 tablas, 1 DB por usuario
  Caja negra (mensajes) + Bitacora (eventos/seguimiento)
```

---

## 2. Requisitos Funcionales

### 2.1 MODULO: Motor de Seguimiento Proactivo [CRITICO - NO EXISTE]

> **Este es el problema #1 identificado por el usuario.** Hoy el seguimiento depende de que el LLM "recuerde" consultar la DB. Debe ser por codigo.

| ID        | Requisito                            | Prioridad | Estado                         |
|-----------|--------------------------------------|-----------|--------------------------------|
| RF-SEG-01 | **Motor de rutinas por codigo**: tabla `rutinas` con: nombre, frecuencia (diaria/semanal/mensual), hora_objetivo, modulo_asociado, preguntas[], acciones_registro[]. Al abrir sesion, el motor ejecuta las rutinas pendientes automaticamente. | CRITICA | NO EXISTE |
| RF-SEG-02 | **Rutina de apertura**: checkpoint obligatorio ejecutado por codigo (no por "recordar"). Lee `checkpoints` tabla, hace las preguntas, registra respuestas en `bienestar`. Si el usuario no quiere contestar, registra NULL. | CRITICA | PARCIAL (depende del LLM) |
| RF-SEG-03 | **Rutina de cierre**: idem apertura. Registra cierre en bienestar, ejecuta caja negra, resumen diario, backup. | CRITICA | PARCIAL |
| RF-SEG-04 | **Rutina de comidas**: 3 checkpoints diarios (almuerzo, merienda, cena) via Telegram. Registra en `nutricion`. Configurable por usuario. | ALTA    | NO EXISTE |
| RF-SEG-05 | **Rutina de ejercicio**: 1 checkpoint diario. Registra tipo, duracion, intensidad. | ALTA    | NO EXISTE |
| RF-SEG-06 | **Alertas de seguimiento vencido**: al inicio de sesion, listar TODOS los seguimientos vencidos con persona asignada. No depender del LLM para que los lea. | CRITICA | DONE (alertas.py + apertura) |
| RF-SEG-07 | **Seguimiento por persona**: query cruzada persona + seguimientos pendientes. "Que le debo a Juan?" ejecutable por codigo. | ALTA    | EXISTE (query manual) |
| RF-SEG-11 | **Clasificacion de seguimientos**: cada seguimiento tiene `responsable` (yo/otro) y `tipo` (tarea/comunicar/cobro/entregar/visita/investigar/vencimiento/espera/decidir). Auto-clasificacion por codigo con nivel de confianza (alta/media/baja). | CRITICA | DONE (v0.7) |
| RF-SEG-12 | **Vista agrupada de pendientes**: apertura muestra 3 bloques: Mis Compromisos (agrupados por tipo), Compromisos de Terceros (agrupados por tipo), Vencimientos. | ALTA | DONE (v0.7) |
| RF-SEG-13 | **Status por proyecto en apertura**: vista rapida de todos los proyectos activos con conteo de pendientes propios/ajenos/vencidos, separados por laboral/personal. | ALTA | DONE (v0.7) |
| RF-SEG-08 | **Modulo de rutinas configurable**: el usuario puede agregar/quitar modulos de seguimiento via comando. | ALTA    | NO EXISTE |
| RF-SEG-09 | **Dashboard de cumplimiento**: por dia/semana, mostrar que rutinas se cumplieron y cuales no. Gap analysis. | MEDIA   | NO EXISTE |
| RF-SEG-10 | **Nudge inteligente por Telegram**: si pasan 2+ horas del horario de una rutina sin registro, enviar recordatorio. | MEDIA   | NO EXISTE |

### 2.2 MODULO: Gestion de Proyectos y Estado

| ID        | Requisito                            | Prioridad | Estado                    |
|-----------|--------------------------------------|-----------|---------------------------|
| RF-PRO-01 | **Estado de proyecto actualizado**: por proyecto, resumen vivo. `get_status_proyectos()` cruza seguimientos con responsable/tipo/vencidos. Vista laboral/personal en apertura. | ALTA  | DONE (v0.7) |
| RF-PRO-02 | **Mapeo completo de proyectos SBD**: todos los proyectos de OneDrive cargados en DB.                                      | ALTA  | PENDIENTE |
| RF-PRO-03 | **Reportes semanales SBD**: generacion automatica de reporte de todos los proyectos activos.                               | MEDIA | PENDIENTE |
| RF-PRO-04 | **Registro automatico de horas**: sin preguntar al usuario, inferir horas por sesion.                                      | ALTA  | PENDIENTE |
| RF-PRO-05 | **Cronologia de conflictos**: reconstruccion de timeline desde WhatsApp/DB para analisis.                                  | BAJA  | EXISTE (manual) |

### 2.3 MODULO: Personas y CRM

| ID        | Requisito                            | Prioridad | Estado           |
|-----------|--------------------------------------|-----------|------------------|
| RF-PER-01 | **Directorio completo**: 42 personas con empresa, cargo, contacto, perfil de comportamiento. | -    | EXISTE           |
| RF-PER-02 | **Perfil de comportamiento**: guia el tono de comunicacion (WhatsApp, mail, llamada).         | -    | EXISTE           |
| RF-PER-03 | **Seguimiento cruzado persona-proyecto**: ver todo lo pendiente con/de una persona.           | ALTA | EXISTE (query)   |
| RF-PER-04 | **Facturacion recurrente por persona/empresa**: alertas primer dia del mes.                   | ALTA | PARCIAL |

### 2.4 MODULO: Bienestar y Salud

| ID        | Requisito                            | Prioridad | Estado                |
|-----------|--------------------------------------|-----------|-----------------------|
| RF-SAL-01 | **Registro diario bienestar**: humor, energia, estres, sueno. Via checkpoint apertura.              | -     | EXISTE  |
| RF-SAL-02 | **Registro nutricion**: comida libre, sin juzgar. Registro rapido por Telegram.                     | ALTA  | EXISTE (tabla vacia) |
| RF-SAL-03 | **Registro salud medica**: turnos, estudios, resultados, planes medicos. Familia incluida.          | MEDIA | EXISTE  |
| RF-SAL-04 | **Plan nutricional cargable**: cargar plan del nutricionista, comparar contra registro real.         | MEDIA | NO EXISTE |
| RF-SAL-05 | **Reporte semanal salud**: comparacion con promedios, tendencias, gaps.                             | MEDIA | NO EXISTE |

### 2.5 MODULO: Comunicacion

| ID        | Requisito                            | Prioridad | Estado                      |
|-----------|--------------------------------------|-----------|-----------------------------|
| RF-COM-01 | **Telegram bidireccional**: texto + audio. Bridge.py graba en DB.                                            | -    | EXISTE                      |
| RF-COM-02 | **WhatsApp masivo**: envio personalizado con anti-ban. Letters JPG + texto.                                   | -    | EXISTE                      |
| RF-COM-03 | **Lectura de emails**: detectar circulares, novedades de COMPR.AR, BAC, proveedores.                         | ALTA | PENDIENTE |
| RF-COM-04 | **Ambos lados ven Q&A**: si pregunto por Telegram, ver respuesta en PC y viceversa.                          | ALTA | PARCIAL                     |
| RF-COM-05 | **Regla de comunicacion**: en pedidos operativos, ir directo al punto.                                       | -    | EXISTE (protocolo)          |
| RF-COM-06 | **Comunicacion always-on en nube**: Telegram y WhatsApp corren en servidor cloud 24/7. El usuario no necesita la PC encendida para recibir/enviar mensajes. Bot Telegram + sesion Baileys persistente en container. | ALTA | NO EXISTE |
| RF-COM-07 | **Acceso remoto a archivos**: si el usuario tiene sus archivos en la nube (OneDrive, Google Drive, o storage propio), ARGOS cloud accede a ellos. Permite trabajar con documentos a distancia sin la PC local. | ALTA | NO EXISTE |

### 2.6 MODULO: Herramientas de Licitaciones

| ID        | Requisito                            | Prioridad | Estado |
|-----------|--------------------------------------|-----------|--------|
| RF-LIC-01 | **Generacion de documentos Word**: desde template con membrete. DDJJ, memorias tecnicas. | - | EXISTE |
| RF-LIC-02 | **Foliacion de PDFs**: merge + numeracion continua entre carpetas A1/A2/B/C.             | - | EXISTE |
| RF-LIC-03 | **Analisis de precios (Anexo VII)**: cadena completa con IVA mix 21%/10.5%.              | - | EXISTE |
| RF-LIC-04 | **Conversion docx a PDF**: via Word COM.                                                  | - | EXISTE |
| RF-LIC-05 | **Descarga de datasheets**: Furukawa, Panduit, Ubiquiti, Grandstream, Kaise.              | - | EXISTE |

### 2.7 MODULO: Auto-aprendizaje

| ID        | Requisito                            | Prioridad | Estado                  |
|-----------|--------------------------------------|-----------|-------------------------|
| RF-APR-01 | **Escaneo automatico**: cada 20 mensajes + al cierre, detectar herramientas/protocolos nuevos.       | -    | EXISTE (hooks)          |
| RF-APR-02 | **Generalizacion**: si un usuario le ensena algo, ARGOS lo empaqueta como seed reutilizable.         | ALTA | PARCIAL                 |
| RF-APR-03 | **Catalogo dinamico**: 107 protocolos validados en DB. Consultar antes de ejecutar tarea.             | -    | EXISTE                  |
| RF-APR-04 | **Seeds exportables**: patrones base para nuevos usuarios en tools/seeds/.                            | -    | EXISTE (85 protocolos)  |

### 2.8 MODULO: Multi-usuario y Producto Comercial

| ID        | Requisito                            | Prioridad | Estado    |
|-----------|--------------------------------------|-----------|-----------|
| RF-MUL-01 | **DB separada por usuario**: cada cliente tiene su argos_tracker.db independiente.        | CRITICA | NO EXISTE |
| RF-MUL-02 | **Encriptacion de DB**: SQLCipher o cifrado a nivel aplicacion.                           | CRITICA | NO EXISTE |
| RF-MUL-03 | **Credenciales aisladas**: .env por usuario, vault de secrets, API keys separadas.        | CRITICA | NO EXISTE |
| RF-MUL-04 | **Aislamiento de archivos**: carpetas privadas por usuario, sin acceso cruzado.           | CRITICA | NO EXISTE |
| RF-MUL-05 | **Onboarding automatizado**: setup < 10 min. MEMORY desde template. Telegram user_id.    | ALTA    | NO EXISTE |
| RF-MUL-06 | **Proceso vs data separados**: herramientas compartidas, datos privados.                  | ALTA    | NO EXISTE |
| RF-MUL-07 | **Soporte Apple**: funcionar en macOS. Eliminar dependencia de Win COM.                   | ALTA    | NO EXISTE |
| RF-MUL-08 | **Panel de administracion**: ver estado de todos los usuarios (solo admin).                | BAJA    | NO EXISTE |

### 2.9 MODULO: Metas y Coherencia

| ID        | Requisito                            | Prioridad | Estado               |
|-----------|--------------------------------------|-----------|----------------------|
| RF-MET-01 | **12 metas registradas**: desarrollo, laboral, salud, personal, formacion.                   | -     | EXISTE               |
| RF-MET-02 | **Medicion de coherencia**: intencion vs comportamiento real.                                | -     | EXISTE (coherencia.py)|
| RF-MET-03 | **Reporte semanal de metas**: progreso, acciones, gaps.                                      | MEDIA | NO ACTIVO            |
| RF-MET-04 | **Deteccion de metas implicitas**: si el usuario habla mucho de algo, sugerir meta.          | BAJA  | EXISTE (protocolo)   |

### 2.10 MODULO: Agenda Inteligente

| ID        | Requisito                            | Prioridad | Estado    |
|-----------|--------------------------------------|-----------|-----------|
| RF-AGE-01 | **Agenda formal en DB**: 88 registros actuales. Carga por comando.                          | -    | EXISTE    |
| RF-AGE-02 | **Agenda inteligente en apertura**: integrar en protocolo obligatorio. Priorizar.            | ALTA | PENDIENTE |
| RF-AGE-03 | **Fechas importantes**: 18 registradas. Alertas anticipadas.                                | -    | EXISTE    |

---

## 3. Requisitos de Interfaz

### 3.1 Interfaz Web (principal)

| Requisito                | Detalle                                                                          |
|--------------------------|----------------------------------------------------------------------------------|
| **Tecnologia**           | Tauri (app nativa liviana) o browser localhost. Frontend React/Svelte.            |
| **Layout PC**            | 3 paneles: chat central + file browser lateral + panel herramientas              |
| **Layout mobile**        | Chat-first. File browser y herramientas via menu hamburguesa.                    |
| **Chat**                 | Texto + audio. Conversacion natural con ARGOS. Centro de la experiencia.         |
| **File browser**         | Acceso directo al filesystem local. El usuario mapea sus carpetas.               |
| **Panel herramientas**   | Configurable por usuario. Solo muestra modulos activos.                          |
| **Drag & drop**          | Arrastrar archivos al chat o a herramientas para procesarlos.                    |
| **Idioma**               | Espanol argentino. Formato montos: $ X.XXX.XXX,XX                                |
| **Tiempo de respuesta**  | < 10 seg para consultas DB. < 30 seg para generacion de docs.                    |
| **Confirmacion**         | NUNCA modificar archivos sin mostrar resultado y pedir confirmacion.             |
| **Archivos**             | NUNCA salen de la PC del usuario. Procesamiento 100% local.                      |

### 3.2 Interfaz Telegram (canal adicional)

| Requisito            | Detalle                                                                              |
|----------------------|--------------------------------------------------------------------------------------|
| **Protocolo**        | python-telegram-bot (polling). Bridge.py conecta con Claude Code.                    |
| **Audio**            | Transcripcion via Groq API (Whisper).                                                |
| **Latencia max**     | NUNCA silencio > 20 seg sin avisar "procesando".                                     |
| **Autenticacion**    | Por Telegram user_id (no PIN). Solo el usuario registrado puede interactuar.         |
| **Registro**         | Todo mensaje entrante/saliente se graba en DB automaticamente (bridge.py).           |

### 3.3 Interfaz WhatsApp (canal adicional + herramienta masiva)

| Requisito          | Detalle                                                       |
|--------------------|---------------------------------------------------------------|
| **Plataforma**     | Baileys (Node.js) via enviar_wwjs.js                          |
| **Uso**            | Envio masivo de campanas. No es canal de conversacion.        |
| **Anti-ban**       | Delays aleatorios, tandas de 10-15, rotacion de mensajes.     |
| **Tracking**       | Tabla de enviados/fallidos/no_encontrados.                    |

### 3.4 Interfaz de Software (integraciones)

| Componente   | Tecnologia                       | Estado                 |
|--------------|----------------------------------|------------------------|
| **DB**       | SQLite + WAL mode                | Operativo              |
| **Word**     | python-docx + lxml               | Operativo              |
| **PDF**      | Win32 COM (Word) + PyMuPDF       | Operativo (solo Windows) |
| **Excel**    | openpyxl                         | Operativo              |
| **STT**      | Groq API (Whisper)               | Operativo              |
| **TTS**      | Por definir                      | NO EXISTE              |
| **Email**    | Por definir (IMAP?)              | NO EXISTE              |
| **OneDrive** | API OAuth (futuro) o agente local | NO EXISTE             |

### 3.4b Visibilidad de datos para el usuario

El usuario debe poder ver y acceder directamente a sus datos almacenados, no solo a traves del chat. ARGOS es transparente: los datos son del usuario, no del sistema.

| Dato                   | Donde se ve                                         | Formato                |
|------------------------|-----------------------------------------------------|------------------------|
| **Contactos/Personas** | Panel web + DB directa (`personas`)                 | Tabla con filtros      |
| **Agenda**             | Panel web + DB directa (`agenda`)                   | Calendario/lista       |
| **Seguimientos**       | Panel web + DB directa (`seguimiento`)              | Kanban o lista con estados |
| **Bienestar**          | Panel web + DB directa (`bienestar`)                | Graficos temporales    |
| **Metas**              | Panel web + DB directa (`metas`)                    | Cards con coherencia   |
| **Proyectos**          | Panel web + DB directa (`proyectos`)                | Dashboard con estado   |
| **Historial eventos**  | Panel web + DB directa (`eventos`)                  | Timeline               |
| **Caja negra**         | Solo DB directa (`mensajes`)                        | Log crudo              |
| **Nutricion/Salud**    | Panel web + DB directa (`nutricion`, `salud`)       | Tablas + graficos      |

**Principio:** El usuario puede abrir la DB con cualquier visor SQLite y ver TODO. No hay datos ocultos. La interfaz web es una capa de presentacion sobre la DB, no un filtro. Si ARGOS desaparece manana, el usuario conserva todos sus datos en formato abierto.

### 3.5 Flujo de sesion

Ciclo de 7 pasos que se repite en cada sesion:

```
APERTURA → AGENDA → CHAT → REGISTRO → DEVOLUCION → AGENDA CIERRE → SEGUIMIENTO
   |                                                                      |
   └──────────────────────── proxima sesion ◄─────────────────────────────┘
```

**Paso 1 — APERTURA:** Saludar por nombre, leer DB (alertas, deadlines, vencidos), ejecutar `reporte_patrones()` + `panel_agentes()`, mostrar agenda del dia, preguntar "En que trabajamos?"

**Paso 2 — AGENDA:** Priorizar urgente → importante → puede esperar. Lista de 3-5 items max.

**Paso 3 — CHAT:** Trabajo libre. Cada interaccion se clasifica automaticamente.

**Paso 4 — REGISTRO:** Cada evento → DB con tipo, subtipo, proyecto, persona. Cada accion completada → marcar en seguimiento. Cada nuevo pendiente → crear con deadline.

**Paso 4b — AGENTES:** El orquestador evalua triggers en segundo plano. Acumula para cierre.

**Paso 5 — DEVOLUCION:** 6 tipos al cerrar:

| Tipo | Que es | Cuando |
|------|--------|--------|
| A. Resumen de sesion | Que hicimos | Siempre (al cerrar) |
| B. Balance vida/trabajo | Distribucion del tiempo | Semanal + a pedido |
| C. Alertas y seguimiento | Deadlines, vencimientos, fechas | Siempre (al abrir) |
| D. Insight personal | Patrones detectados, observaciones | Semanal/mensual |
| E. Metricas de rendimiento | Numeros duros | Mensual + a pedido |
| F. Proximos pasos | Que hacer despues | Siempre (al cerrar) |

**Paso 6 — AGENDA ACTUALIZADA:** Que se completo, que quedo pendiente, que nuevo surgio.

**Paso 7 — SEGUIMIENTO PASIVO:** Entre sesiones, deadlines siguen corriendo. Al abrir la proxima sesion, ARGOS calcula que vencio, que esta por vencer, que patterns se repiten.

**Clasificacion automatica de interacciones:**

| Tipo de entrada | Ejemplo | Tag |
|----------------|---------|-----|
| Pedido de accion | "Dame un mail para X" | accion |
| Actualizacion | "Mande el mail" | estado |
| Consulta estrategica | "Como resuelvo esto?" | estrategia |
| Descarga emocional | "Mi jefe me presiona" | personal |
| Organizacion | "Agrega esto al seguimiento" | organizacion |
| Construccion | "Armemos una herramienta para X" | construccion |

**Estructura del evento en DB:**
```
evento {
    fecha, hora,
    tipo:       laboral | personal | salud | familia | argos
    subtipo:    accion | estado | estrategia | personal | organizacion | construccion
    proyecto:   → FK proyectos
    persona:    → FK personas
    descripcion, fuente, resultado, energia (1-5), impacto (1-5), duracion_min
}
```

---

## 4. Requisitos No Funcionales

### 4.1 Seguridad

| ID          | Requisito                                                                            | Prioridad |
|-------------|--------------------------------------------------------------------------------------|-----------|
| RNF-SEC-01  | DB encriptada por usuario (SQLCipher). Sin acceso cruzado entre usuarios.            | CRITICA   |
| RNF-SEC-02  | Credenciales aisladas (.env por usuario). API keys nunca compartidas.                | CRITICA   |
| RNF-SEC-03  | Repositorio GitHub PRIVADO. Datos personales sensibles.                              | CRITICA   |
| RNF-SEC-04  | Ley 25.326 de Proteccion de Datos Personales. Consentimiento informado.              | ALTA      |
| RNF-SEC-05  | Backup encriptado con verificacion de integridad.                                    | ALTA      |
| RNF-SEC-06  | HTTPS para toda comunicacion si se migra a cloud.                                    | ALTA      |
| RNF-SEC-07  | Papelera (soft delete) obligatoria. Nunca borrar sin papelera.                       | EXISTE    |

### 4.2 Capacidad

| Metrica                  | Valor actual | Proyeccion 1 ano       |
|--------------------------|--------------|------------------------|
| Mensajes en caja negra   | 1.564        | ~50.000 (1 usuario)    |
| Eventos                  | 250          | ~5.000                 |
| Seguimientos             | 149          | ~1.000                 |
| Personas                 | 42           | ~200                   |
| Patrones                 | 227          | ~500                   |
| Tamano DB                | ~5 MB        | ~100 MB por usuario    |
| Usuarios simultaneos     | 1            | 5-10 (meta cloud)      |

### 4.3 Confiabilidad

| Metrica                | Objetivo                                  |
|------------------------|-------------------------------------------|
| Checkpoint ejecutado   | 100% de las sesiones                      |
| Caja negra grabada     | 100% de los mensajes (0 perdida)          |
| Backup al cierre       | 100% de las sesiones                      |
| Uptime (cloud)         | 99% en horario laboral (8-22 hs)          |
| MTTR ante fallo DB     | < 30 min (restaurar desde backup)         |

### 4.4 Escalabilidad

| Escenario                          | Horizonte | Requisito                                    |
|------------------------------------|-----------|----------------------------------------------|
| 1-2 usuarios (Hernan + Natalia)    | Abr 2026  | App local + proxy AiControl basico           |
| 5 usuarios pagos                   | Jun 2026  | Proxy estable + marketplace + auto-update    |
| 30-50 usuarios                     | Dic 2026  | API Anthropic optimizada (Haiku/Sonnet mix)  |
| +50 usuarios                       | 2027      | Escalar proxy, mas plugins, comunidad activa |

### 4.5 Mantenibilidad

| Requisito                        | Detalle                                                             |
|----------------------------------|---------------------------------------------------------------------|
| **Herramientas como modulos**    | Cada tool es un .py independiente, importable, testeable.           |
| **Protocolos en DB**             | Los protocolos estan en tabla `patrones`, no hardcodeados.          |
| **Seeds exportables**            | Patrones base en tools/seeds/ para nuevos usuarios.                 |
| **Auto-aprendizaje**             | ARGOS detecta funcionalidad nueva y la registra automaticamente.    |
| **Git**                          | Control de versiones. Commits con descripcion clara.                |

### 4.6 Portabilidad

| Requisito                                | Detalle                            | Estado    |
|------------------------------------------|------------------------------------|-----------|
| Eliminar paths Windows hardcodeados      | Usar config/env vars               | PENDIENTE |
| Eliminar dependencia Win32 COM           | LibreOffice para PDF en Linux      | PENDIENTE |
| Soporte macOS                            | Para usuarios Apple (Natalia)      | PENDIENTE |
| Docker-ready                             | Contenedorizacion para deploy cloud | NO EXISTE |

### 4.7 Facilidad de uso

| Requisito                            | Detalle                                                                             |
|--------------------------------------|-------------------------------------------------------------------------------------|
| **Chat-first**                       | El chat es el centro. Los paneles son atajos visuales, no formularios.              |
| **Onboarding < 10 min**             | Template MEMORY + Telegram user_id + DB vacia con seeds.                            |
| **Espanol argentino**                | Montos, fechas, modismos.                                                           |
| **Tolerancia a errores de tipeo**    | El LLM interpreta pese a typos.                                                    |
| **Multicanal**                       | Mismo ARGOS responde por app web, Telegram y WhatsApp. El usuario elige canal.      |

---

## 5. Arquitectura y Decisiones Tecnicas

### 5.1 Decision de arquitectura: LOCAL-FIRST, CLOUD-ASSISTED

> **DECISION (2026-03-04)** — ARGOS es una app local. Los datos y archivos NUNCA salen de la PC del usuario. La nube solo asiste (API de IA, auth, marketplace, actualizaciones).

**Por que local-first:**
- Archivos del usuario quedan en su PC (privacidad total, Ley 25.326)
- No hay costo de almacenamiento cloud
- Funciona sin internet (excepto chat con IA)
- El usuario tiene control total de sus datos

**Modelo de IA para produccion:**
- Claude Code Max = herramienta de DESARROLLO (Hernan construyendo ARGOS)
- API Anthropic = infraestructura de PRODUCCION (ARGOS atendiendo clientes)
- Son el mismo cerebro (Claude), distinto cable de conexion

| Concepto | Claude Code (desarrollo) | API Anthropic (produccion) |
|---|---|---|
| Quien lo usa | Hernan programando | ARGOS atendiendo clientes |
| Limite | 1 usuario | Ilimitados |
| Precio | ~$100-200/mes flat | Por consumo (~$3-15/M tokens) |
| Donde corre la IA | Cloud Anthropic | Cloud Anthropic (igual) |

**Capacidades que ARGOS ofrece al usuario (via Claude API):**

| Capacidad                          | Para gente comun                                            | Para especializados                                        |
|------------------------------------|-------------------------------------------------------------|------------------------------------------------------------|
| **Buscar archivos**                | "Donde deje la factura?"                                    | "Buscar los PDF de la licitacion 410"                      |
| **Organizar archivos**             | "Ordename las fotos por fecha"                              | "Mover datasheets a carpeta B"                             |
| **Leer y resumir**                 | "Que dice este contrato?"                                   | "Extraer requisitos tecnicos del pliego"                   |
| **Generar documentos**             | "Escribime una carta"                                       | "Generar DDJJ con membrete"                                |
| **Manipular Excel**                | "Cuanto gaste este mes?"                                    | "Calcular IVA mix 21/10.5"                                 |
| **Mensajes masivos**               | "Feliz cumple a toda la lista"                              | "Campana WhatsApp 300 contactos"                           |
| **Programar herramientas**         | "Avisame cuando vence el seguro"                            | "Foliador de PDFs con numeracion"                          |
| **Gestionar agenda**               | "Que tengo hoy?"                                            | "Vencimientos de la semana por proyecto"                   |
| **Tracking de personas**           | "Que quedo con Maria?"                                      | "Seguimientos con prioridad critica"                       |
| **Salud**                          | "Almorce milanesa con ensalada"                             | "Adherencia semanal al plan nutricional"                   |

### 5.2 Arquitectura local-first

```
PC DEL USUARIO (todo corre aca)
┌─────────────────────────────────────────────┐
│  INTERFAZ: App web (Tauri/browser localhost) │
│  Chat + File Browser + Paneles herramientas  │
├─────────────────────────────────────────────┤
│  ENGINE: Python (FastAPI)                    │
│  tracker.py | tools/*.py | agents/           │
├─────────────────────────────────────────────┤
│  DATOS: SQLite cifrada (SQLCipher)           │
│  argos_tracker.db — UNICA fuente de verdad   │
├─────────────────────────────────────────────┤
│  ARCHIVOS: filesystem local del usuario      │
│  Acceso directo, nunca salen de la PC        │
└──────────────────┬──────────────────────────┘
                   │ internet (solo texto)
                   ▼
┌─────────────────────────────────────────────┐
│  NUBE AICONTROL (kiosco, no fabrica)         │
│                                              │
│  Proxy API Anthropic (controla consumo)      │
│  Auth + Suscripciones (JWT)                  │
│  Marketplace protocolos (descargar tools)    │
│  Actualizaciones de la app                   │
│  Metricas anonimas de uso                    │
└─────────────────────────────────────────────┘
```

### 5.3 Modelo de creacion de herramientas

> **Los usuarios programan hablando con Claude.** AiControl cuida la comunidad.

```
Usuario usa ARGOS → pide algo → Claude lo resuelve → funciona
    ↓
ARGOS detecta patron (3+ usos exitosos) → lo registra como protocolo
    ↓
AiControl revisa → si es bueno, lo perfecciona → lo publica en marketplace
    ↓
Otros usuarios lo descargan y lo usan con SUS datos
```

| Quien | Que hace | Ejemplo |
|---|---|---|
| **El usuario** | Pide, itera, crea herramientas hablando con Claude | "Armame una campaña WhatsApp con esta lista" |
| **ARGOS** | Detecta que funciono, lo generaliza como protocolo | Protocolo: "campaña WhatsApp desde Excel" |
| **AiControl** | Revisa, perfecciona, decide que se comparte | Mejora el protocolo, lo publica en marketplace |
| **La comunidad** | Descarga protocolos validados, los customiza | Usa el protocolo con sus datos y lo adapta |

**Protocolos con variantes:**
- Protocolo base (igual para todos) — publicado por AiControl
- Variante por usuario — cada uno ajusta tono, horarios, filtros
- Protocolo personal (no se comparte) — queda solo en la DB del usuario

### 5.4 Stack tecnico actual

| Componente   | Tecnologia                   | Version       |
|--------------|------------------------------|---------------|
| Runtime      | Python 3.12.1                | C:\Python312  |
| DB           | SQLite + WAL                 | 3.x           |
| LLM          | Claude (via Claude Code Max) | Opus/Sonnet   |
| Telegram     | python-telegram-bot          | 20.x          |
| STT          | Groq API (Whisper)           | -             |
| WhatsApp     | Baileys (Node.js)            | -             |
| Docs         | python-docx + lxml           | -             |
| PDF          | Win32COM + PyMuPDF           | -             |
| Excel        | openpyxl                     | -             |
| OS           | Windows 11 Pro               | 10.0.26200    |

### 5.5 Decisiones estrategicas

#### Decision 1: ARGOS es ESPEJO, no COACH (24/02/2026)

Consenso de 4 agentes (Neuro, Comercial, UX, Etico):

**Dr. Neuro:** ARGOS funciona mejor como espejo que como coach. Mostrar patrones sin empujar cambio. Riesgo Goodhart: si medis algo, la gente optimiza la metrica, no el objetivo real. Herramienta mas impactante: detector de coherencia intencion/comportamiento (IMPLEMENTADO).

**Estratega Comercial:** Enfoque hibrido: arrancar generico, verticalizar despues. Killer feature: "el unico asistente que no te hace repetir tu historia". NO crear agentes visibles para usuarios.

**UX Lead:** Onboarding en 10 preguntas, resultado tangible en 20 minutos. Agentes invisibles para el usuario final. El usuario habla con ARGOS, no con "el Dr. Neuro".

**Etico:** ALERTA: tracking psicologico sin marco legal = riesgo. ALERTA: backup sin encriptacion. Analisis emocional requiere consentimiento explicito. Datos de menores requieren tratamiento especial.

**Resultado:** ARGOS es UNA entidad. Espejo, no coach. Metodo generico + contexto profundo = el producto. Agentes internos invisibles.

#### Decision 2: Sistema Multi-Agente para desarrollo (24/02/2026)

7 agentes especializados que evaluan cada cambio:

| Codigo | Nombre | Rol | Activacion |
|--------|--------|-----|------------|
| neuro | Dr. Neuro | Neurociencia, cognicion, carga mental | Cierre sesion, estres |
| comercial | Estratega | Negocio, pricing, go-to-market | Funcion nueva, estrategia |
| arquitecto | Arquitecto | Diseno tecnico, viabilidad | Cambios tecnicos, schema |
| data | Data Engineer | Metricas, ML, prediccion | Cierre sesion, metricas |
| ux | UX Lead | Experiencia usuario, onboarding | Funcion nueva, interfaz |
| etico | Etico | Privacidad, compliance, limites | Datos sensibles, exportacion |
| dba | DBA | Schema, queries, migraciones | Cambios schema, review |

Son prompts especializados (agents/*.md) invocados como subagentes. El orquestador decide cuando activar cada uno.

#### Decision 3: Detector de Coherencia (24/02/2026)

Cruza metas declaradas con actividad real. Senales: on_track (>=0.7), en_riesgo (0.3-0.7), desalineada (<0.3), abandonada (<0.1). Primer reporte real: coherencia promedio 0.29 — energia concentrada en ARGOS, metas declaradas sin actividad.

**Principio:** El reporte es descriptivo, no prescriptivo. Muestra numeros, no dice que hacer.

#### Decision 4: Proximos pasos por agentes (24/02/2026)

| Tier | Items | Estado |
|------|-------|--------|
| **Tier 1** (impacto alto, esfuerzo bajo) | Detector coherencia, reporte energia al cierre | Coherencia IMPLEMENTADO |
| **Tier 2** (impacto alto, esfuerzo medio) | Onboarding 10 preguntas, marco legal, encriptacion, verticales | Pendiente |
| **Tier 3** (impacto medio, esfuerzo alto) | ML feedback loop, metricas bienestar desde lenguaje, dashboard web, pricing por valor | Pendiente |

**Alertas activas del Agente Etico:**
1. Tracking psicologico requiere consentimiento explicito y marco legal antes de activar para externos
2. Backup con datos sensibles (salud, finanzas, emociones) sin encriptacion
3. Datos de menores (hijos) requieren tratamiento especial

#### Historial completo de decisiones

| Decision | Fecha |
|----------|-------|
| Espejo, no coach — agentes invisibles | 2026-02-24 |
| Sistema multi-agente de 7 para desarrollo | 2026-02-24 |
| Detector de coherencia como primera herramienta espejo | 2026-02-24 |
| DB como unica fuente de verdad | 2026-02-18 |
| 2 capas (caja negra + bitacora) | 2026-02-27 |
| Auto-aprendizaje por hooks | 2026-03-02 |
| Seeds generalizables | 2026-02-22 |
| No API extra (usar suscripcion Claude existente) | 2026-02-27 |
| Arquitectura LOCAL-FIRST, cloud-assisted | 2026-03-04 |
| App web local (Tauri/browser) como interfaz principal | 2026-03-04 |
| API Anthropic para produccion (no Claude Code) | 2026-03-04 |
| Usuarios programan herramientas hablando con Claude | 2026-03-04 |
| AiControl cuida comunidad (revisa, perfecciona, publica) | 2026-03-04 |
| Datos del usuario NUNCA salen de su PC | 2026-03-04 |
| Si no paga, baja a Free pero datos son suyos siempre | 2026-03-04 |
| AiControl es la marca comercial (no SBD) | 2026-03-04 |
| No WSL, mantener Windows nativo | 2026-03-02 |
| Cross-platform: una base de codigo | 2026-03-02 |
| B2C directo. AiControl factura al cliente | 2026-02-20 |
| Telegram como primera interfaz mobile | 2026-02-20 |
| Proceso compartible, data nunca | 2026-02-22 |
| Sandbox cerrado en produccion: tools whitelist, sin bash, sin filesystem libre | 2026-03-04 |
| 5 capas de proteccion tecnica (tools, filesystem, destructivas, rate limit, audit) | 2026-03-04 |
| T&C + seguro E&O obligatorios antes de dia 1 | 2026-03-04 |

### 5.6 Alertas de migracion a la nube

ARGOS hoy corre en Windows nativo (PC de Hernan). Para funcionar en nube y servir a multiples usuarios, resolver estas alertas ANTES del deploy. **Principio:** una sola base de codigo, no se duplican herramientas por ecosistema.

#### ALERTA 1 — Encriptacion de DB por usuario [CRITICA]
Hoy `argos_tracker.db` es SQLite plano. Cualquiera con acceso al servidor lee datos personales.
**Recomendacion:** SQLCipher. Encriptacion transparente AES-256, una key por DB. Ni AiControl puede leer datos sin la key del usuario.
**Impacto:** Modificar tracker.py: `sqlite3.connect()` → `sqlcipher.connect()` + `PRAGMA key`. Script de migracion DB plana → encriptada.

#### ALERTA 2 — Credenciales por usuario [CRITICA]
Hoy hay un solo `.env` con las API keys de Hernan. En multi-usuario, cada uno tiene sus propias credenciales.
**Necesita cada usuario:** TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, DB_ENCRYPTION_KEY (propios). GROQ_API_KEY puede ser compartida (AiControl paga). ANTHROPIC_API_KEY depende del modelo de negocio.

#### ALERTA 3 — Archivos privados por usuario [CRITICA]
Arquitectura propuesta: `/srv/argos/users/{uid}/` con data/, config/, output/, files/, memory/ por usuario. `shared/` con tools, templates, seeds (read-only para usuarios).

#### ALERTA 4 — pdf_converter.py: win32com → LibreOffice headless [MEDIA]
Reemplazar `win32com.client` por `soffice --headless --convert-to pdf`. Solo 1 archivo a modificar. Calidad 95% identica a Word.

#### ALERTA 5 — Paths hardcodeados Windows [MEDIA]
Rutas `C:\Users\HERNAN\...` hardcodeadas. Solucion: `pathlib.Path` + env vars (`ARGOS_USER_ROOT`).

#### ALERTA 6 — Separacion proceso vs data [ALTA]
Principio definido: **se comparte el PROCESO, nunca la DATA.** 3 niveles: (1) usuario mejora su ARGOS, (2) ARGOS generaliza automaticamente, (3) distribucion a otros. Falta: mecanismo de export, catalogo central, filtro por perfil, sugerencia al abrir sesion.

#### ALERTA 7 — Marco legal y consentimiento [ALTA]
Normativa: Ley 25.326 (Habeas Data Argentina), GDPR (UE), CCPA (California). Falta: texto legal T&C, flujo consentimiento onboarding, mecanismo borrado total (derecho al olvido), log auditoria, politica retencion, tratamiento datos menores.

#### ALERTA 8 — Comunicacion always-on (Telegram + WhatsApp en nube) [ALTA]
Hoy Telegram y WhatsApp dependen de la PC encendida. En nube, corren 24/7 en container.
**Componentes:** (1) Bot Telegram en container con reconnect automatico, (2) Sesion Baileys persistente (WhatsApp Web) con auth guardada en volumen, (3) Cola de mensajes para cuando ARGOS procesa.
**Riesgo WhatsApp:** Meta puede banear sesiones cloud. Mitigar con: delays humanos, rotacion IP, limite diario, no envio masivo desde cloud.
**Impacto:** RF-COM-06. Requiere A2 (credenciales por usuario) y A3 (archivos privados).

#### ALERTA 9 — Acceso remoto a archivos del usuario [ALTA]
Si el usuario tiene archivos en OneDrive/Google Drive/storage propio, ARGOS cloud necesita acceso.
**Opciones:** (1) Sync bidireccional con rclone (OneDrive, GDrive, S3), (2) Mount FUSE en el container, (3) API directa de cada proveedor.
**Recomendacion:** rclone con config por usuario. Sync selectivo (solo carpetas autorizadas).
**Impacto:** RF-COM-07. Requiere A3 (archivos privados por usuario).

#### Checklist pre-deploy

| # | Alerta | Prioridad | Bloqueante | Dependencias |
|---|--------|-----------|------------|-------------|
| A1 | Encriptacion DB | CRITICA | SI | — |
| A2 | Credenciales | CRITICA | SI | A1 |
| A3 | Archivos privados | CRITICA | SI | A2 |
| A4 | PDF cross-platform | MEDIA | NO | — |
| A5 | Paths hardcodeados | MEDIA | NO | — |
| A6 | Proceso vs data | ALTA | SI para comunidad | A1, A2, A3 |
| A7 | Marco legal | ALTA | SI para produccion | Asesoria legal |
| A8 | Comunicacion always-on | ALTA | SI para cloud | A2, A3 |
| A9 | Acceso remoto archivos | ALTA | NO (mejora) | A3 |

**Orden recomendado:** A5 (simple, desbloquea testing) → A1 → A2 → A3 → A8 → A4 → A6 → A9 → A7

---

## 6. Catalogo de Capacidades

### 6.1 Fuente de verdad

El catalogo de capacidades vive en la DB, no en este documento. Consultar:
```sql
SELECT tipo, COUNT(*) as cantidad
FROM patrones
WHERE tipo LIKE 'protocolo_%' AND estado='validado'
GROUP BY tipo ORDER BY cantidad DESC
```

**Estado actual:** 107 protocolos validados en 15 tipos de protocolo.

### 6.2 Resumen por tipo de protocolo

| Tipo en DB | Capacidad | Cant | Herramientas principales |
|---|---|---|---|
| `protocolo_licitacion` | Licitaciones publicas | 30 | foliador, doc_generator, cotizacion, pdf_converter |
| `protocolo_asesor` | Asesoramiento personal | 16 | bridge.py, tracker.py |
| `protocolo_salud` | Seguimiento de salud | 7 | tracker.py (tabla salud), proactivo.py |
| `protocolo_nutricion` | Nutricion / dieta | 5 | tracker.py (tabla nutricion) |
| `protocolo_reflexion` | Reflexiones / emocional | 5 | proactivo.py, tracker.py |
| `protocolo_metas` | Gestion de metas | 5 | coherencia.py, tracker.py |
| `protocolo_telegram` | Telegram bridge | 5 | bot/loop.py, bridge.py, send.py |
| `protocolo_bienestar` | Bienestar diario | 4 | tracker.py (tabla bienestar) |
| `protocolo_backup` | Backup y seguridad | 4 | backup.py, db_safety.py |
| `protocolo_agentes` | Multi-agente | 4 | agents/orquestador.py |
| `protocolo_sistema` | Auto-aprendizaje + metricas | 4 | auto_aprendizaje.py, detector_cierre.py |
| `protocolo_datos` | Data science / analisis | 4 | LLM + openpyxl + matplotlib |
| `protocolo_marketing` | Marketing masivo WhatsApp | 2 | enviar_wwjs.js, wapp_baileys/ |
| `protocolo_gestion` | Tracking por persona, perfiles | - | seguimiento.persona_id, consultas cruzadas |
| `protocolo_admin` | Facturacion recurrente | - | seguimientos mensuales, alertas |

### 6.3 Herramientas por tipo

**Con tool Python dedicado (20+ funciones):**
tracker.py (tracking, agenda, onboarding, nutricion), doc_generator.py (docs Word, notas membrete), excel_tools.py (Excel, materiales, informes), cotizacion.py (analisis precios), foliador.py (foliacion PDFs), pdf_converter.py (extraccion datos), backup.py (backup DB), bot/loop.py (Telegram), patterns.py (auto-aprendizaje), coherencia.py (detector coherencia), agents/orquestador.py (multi-agente).

**Sin tool — LLM directo (12 funciones):**
Redaccion calibrada, emails formales, WhatsApp, cotizacion a proveedores, analisis cadenas WhatsApp, investigacion tecnica, estrategias, planificacion cross-life, dinamicas interpersonales, toma de decisiones, documentacion producto, estructura carpetas.

### 6.4 Auto-aprendizaje

El catalogo NO es fijo. Crece con cada interaccion exitosa:

```
USUARIO PIDE ALGO → ARGOS detecta si es NUEVA / CONOCIDA / MEJORA
  → NUEVA: registra en catalogo con herramienta + protocolo
  → CONOCIDA: incrementa contador de uso
  → MEJORA: crea nueva version, conserva historial
```

**Motor de deteccion automatica de patrones:**

1. **Que mide (automaticamente):** tiempo por tipo de tarea, secuencia de acciones, frecuencia por modulo, iteraciones hasta resultado, horarios de trabajo, tasa de aceptacion de sugerencias.

2. **Triggers de deteccion:**
   - Por repeticion: misma secuencia 3+ veces → patron
   - Por contraste: sesion significativamente distinta al promedio → analizar
   - Por abandono: empieza algo y lo deja → registrar punto de abandono
   - Por exito: pocas iteraciones + aceptacion rapida → patron exitoso

3. **Clasificacion:**
   - **General** — aplica a cualquier usuario → se comparte anonimo
   - **Por perfil** — aplica a usuarios similares → se comparte agrupado
   - **Personal** — especifico del usuario → queda solo en su instancia

4. **Principio fundamental: SE COMPARTE EL PROCESO, NUNCA LA DATA**

| Concepto | Ejemplo | Se comparte? |
|----------|---------|-------------|
| **PROCESO** | "Para seguimiento de peso: tabla fecha+peso, registro diario, grafico semanal" | Si (anonimo) |
| **DATA** | "Juan pesa 85kg el 22/02" | NUNCA |
| **HERRAMIENTA** | Script/funcion que implementa el proceso | Si (codigo generico) |
| **ARCHIVOS** | Excel, Word, PDF generados | NUNCA |

3 niveles de generalizacion:
- **Nivel 1:** Usuario mejora su ARGOS → ARGOS implementa para ese usuario
- **Nivel 2:** ARGOS generaliza automaticamente → extrae proceso sin data → registra en catalogo
- **Nivel 3:** Distribucion → proximo usuario del mismo perfil recibe sugerencia

**Transparencia:** Al registrarse, se informa del modelo. Opt-out por proceso o total disponible.

### 6.5 Cumplimiento normativo (compliance)

| Normativa | Jurisdiccion | Que exige |
|-----------|-------------|-----------|
| Ley 25.326 (Habeas Data) | Argentina | Consentimiento, acceso, rectificacion, supresion |
| GDPR | Union Europea | Consentimiento explicito, portabilidad, derecho al olvido, DPO |
| CCPA | California, EEUU | Derecho a saber, derecho a borrado, opt-out de venta |

**Garantias:**
- DATA nunca sale de la instancia del usuario (DB encriptada + archivos privados)
- Solo se comparte el PROCESO (pasos, metodo, herramienta generica sin datos)
- Opt-out por proceso o total. Derecho al olvido (borrado completo).
- Moderacion etica: el LLM rechaza interacciones ilegales. Bloqueadas = nunca se generalizan.
- AiControl no modera contenido — el filtro es del motor IA. Solo metricas anonimas de bloqueos.

---

## 7. Negocio y Competencia

### 7.0 Propiedad del producto

| Concepto | Detalle |
|---|---|
| **Producto** | ARGOS |
| **Marca comercial** | AiControl |
| **Creador** | Hernan Hamra |
| **Empresa del creador** | Software By Design S.A. (SBD es donde trabaja, no es duena de ARGOS) |
| **Facturacion** | AiControl factura directo al cliente |

### 7.1 Propuesta de valor

> "Un asistente con IA que te conoce, te organiza, te asesora y construye lo que necesitas — sin que sepas programar."

**Diferenciador clave:** No existe ningun producto que combine perfil profundo + memoria persistente + ejecucion de codigo + asesoramiento + tracking multi-dominio + datos 100% locales + herramientas creadas por los propios usuarios.

### 7.2 Analisis de competencia

**No existe ningun producto que haga lo que ARGOS hace.** Los competidores cubren partes del problema pero ninguno integra todo.

| Capacidad | ARGOS | ChatGPT | Claude.ai | Notion AI | Copilot MS | Rewind |
|-----------|:-----:|:-------:|:---------:|:---------:|:----------:|:------:|
| Perfil profundo del usuario | **SI** | parcial | no | no | no | no |
| Memoria persistente estructurada | **SI** | parcial | no | no | no | si |
| Ejecuta codigo local | **SI** | no | no | no | no | no |
| Construye herramientas a pedido | **SI** | no | no | no | no | no |
| Trackea proyectos + vida personal | **SI** | no | no | parcial | no | pasivo |
| Asesora con contexto profundo | **SI** | parcial | no | no | no | no |
| Redacta calibrado al interlocutor | **SI** | generico | generico | generico | generico | no |
| Datos 100% locales | **SI** | no | no | no | no | si |
| Multi-dominio (trabajo+personal+salud) | **SI** | no | no | parcial | no | pasivo |

### 7.3 Ventaja competitiva

1. **Categoria nueva** — "Asesor personal con IA que construye herramientas". No hay incumbents.
2. **Efecto red personal** — Cuanto mas lo usas, mas te conoce. Lock-in natural sin manipulacion.
3. **Local-first como feature** — Datos y archivos NUNCA salen de la PC. Diferenciador para datos sensibles.
4. **Usuarios crean herramientas** — Los usuarios programan hablando. AiControl cuida y comparte las mejores.
5. **Costo bajo** — USD 30-50/mes total. Un asistente humano: USD 500+/mes.

### 7.4 Amenazas

| Amenaza | Probabilidad | Impacto | Respuesta |
|---------|:----------:|:------:|-----------|
| Anthropic lanza producto similar | Media | Alto | First mover + personalización profunda |
| OpenAI mejora memoria ChatGPT | Alta | Medio | ChatGPT no ejecuta codigo local — brecha estructural |
| Precio de Claude sube | Baja | Medio | Metodo migrable a otro LLM |
| Usuarios no tecnicos no adoptan | Media | Alto | Setup guiado + video + soporte |

### 7.5 Modelo de negocio

**Arquitectura de costos:**

| Item | Costo/mes | Detalle |
|---|---|---|
| API Anthropic | ~$5 por usuario | Tokens consumidos (variable) |
| Servidor proxy (auth, marketplace) | ~$20 fijo | VPS basico (Hetzner/DigitalOcean) |
| Dominio | ~$1 | aicontrol.com.ar o similar |

| Escenario | Ingreso | Costo | Margen |
|---|---|---|---|
| 1 usuario | $40 | $25 | $15 (38%) |
| 10 usuarios | $400 | $75 | $325 (81%) |
| 50 usuarios | $2.000 | $295 | $1.705 (85%) |

**Planes propuestos:**
- **ARGOS Free:** Chat basico + 3 herramientas + datos locales. Sin costo.
- **ARGOS Pro (USD 30-40/mes):** Todas las herramientas + canales (Telegram, WhatsApp) + seeds comunidad + soporte.
- **ARGOS Enterprise (a definir):** + plugins custom + SLA + soporte dedicado.

**Si deja de pagar:** baja a Free. Los datos son suyos SIEMPRE. No se borran, no se bloquean. Puede exportar todo (CSV, JSON, SQLite). Los datos NUNCA son rehenes.

**Canales de venta:** Red personal (mes 1-2) → Contenido LinkedIn + video demo (mes 2-4) → Landing page con cobro automatico LemonSqueezy/Gumroad (mes 4+) → Comunidad WhatsApp/Telegram.

### 7.6 Riesgos de negocio

| Riesgo | Mitigacion |
|--------|-----------|
| Anthropic cambia pricing | Modelo flexible, ARGOS vale por el metodo |
| Anthropic lanza similar | First mover + personalizacion profunda |
| No-tecnicos no pueden instalar | Setup guiado + video + soporte |
| Pocos pagan | Empezar con red personal, crecer organico |
| Soporte escala linealmente | Documentacion + FAQ + comunidad |
| Dependencia de Opus | Router futuro: Opus para crear, Sonnet/Haiku para operar |

---

## 8. Backlog de Bugs y Deuda Tecnica

### 8.1 Bugs reportados

| ID      | Bug                                                                             | Severidad | Origen              | Estado                  |
|---------|---------------------------------------------------------------------------------|-----------|----------------------|-------------------------|
| BUG-01  | Seguimiento vencido no alertado (Alejandro baterias 27/02)                      | CRITICA   | errores_argos #1     | Pendiente               |
| BUG-02  | Checkpoint de cierre no ejecutado automaticamente                               | ALTA      | errores_argos #2     | Resuelto (hook)         |
| BUG-03  | Natalia: DB compartida causa errores de seguimiento entre usuarios              | CRITICA   | Purim 2026-03-03     | Requiere RF-MUL-01      |
| BUG-04  | WhatsApp baneado durante campana Purim (contenido identico a muchos contactos)  | ALTA      | Purim                | Protocolo anti-ban creado |
| BUG-05  | Checkpoints no integrados con herramientas por codigo                           | ALTA      | Purim                | Requiere RF-SEG-01      |
| BUG-06  | Protocolos dependen de interpretacion del LLM, no de codigo                     | CRITICA   | Purim 2026-03-03     | Requiere RF-SEG-01/08   |
| BUG-07  | Envio a contactos no aprobados (8 personas sin autorizacion)                    | CRITICO   | Purim                | Whitelist implementada  |
| BUG-08  | Cartas enviadas sin imagen personalizada (6 contactos)                          | ALTO      | Purim                | Recargar lista pre-envio |
| BUG-09  | Excel como fuente de verdad incompleta (script no actualiza estado)             | MEDIO     | Purim                | Migrar a DB             |
| BUG-10  | Matching contactos fragil (98 de 126 no matchearon primer intento)             | MEDIO     | Purim                | Fuzzy matching + cache  |
| BUG-11  | Telegram loop.py no responde inteligentemente (solo "procesando...")            | ALTO      | 2026-03-04           | Pendiente               |

### 8.2 Deuda tecnica

| Item   | Descripcion                                       | Impacto                                   |
|--------|---------------------------------------------------|--------------------------------------------|
| DT-01  | Paths hardcodeados (C:\Users\HERNAN\...)          | Bloquea deploy cloud y multiusuario        |
| DT-02  | Win32 COM para PDF                                | Bloquea soporte macOS/Linux                |
| DT-03  | Sin tests automatizados                           | Regresiones silenciosas                    |
| DT-04  | Sin CI/CD                                         | Deploy manual                              |
| DT-05  | Sin containerizacion                              | No reproducible en otro entorno            |
| DT-06  | Telegram bot sin reconnect automatico             | Se cae y nadie se entera                   |
| DT-07  | Sin health check del sistema                      | No sabe si los componentes estan vivos     |
| DT-08  | Sin logging estructurado                          | Dificil debuggear en produccion            |

### 8.3 Arquitectura de seguridad

```
PC del usuario (todo local)              Nube AiControl (solo proxy)
┌────────────────────────┐          ┌──────────────────────────┐
│ App Tauri/browser       │          │ Cloudflare (HTTPS, DDoS) │
│ Engine Python           │◄────────►│ Proxy API Anthropic       │
│ SQLite cifrada          │  tokens  │ Auth JWT                  │
│ Archivos locales        │  solo    │ Marketplace protocolos    │
│ Credenciales en keyring │          │ Metricas anonimas         │
└────────────────────────┘          └──────────────────────────┘
```

**Principio:** los datos viajan solo como texto de chat hacia la API de IA. Archivos, DB y credenciales NUNCA salen de la PC.

### 8.4 Componentes a separar como modulos independientes

| Componente | Razon |
|---|---|
| Marketing WhatsApp/Mailing | Producto en si mismo. Necesita UI propia. |
| Generacion de documentos | Servicio API: datos → DOCX/PDF. |
| Foliacion/merge PDF | Servicio puntual, no necesita estar en core. |

### 8.5 Sandboxing y proteccion del cliente (CRITICO)

> **DECISION (2026-03-04)** — ARGOS produccion usa API Anthropic con tools pre-definidas. Claude SOLO puede llamar funciones que AiControl define. No tiene bash, no tiene acceso libre al filesystem, no puede hacer nada fuera de la whitelist.

#### Diferencia fundamental: Claude Code vs ARGOS produccion

| Aspecto | Claude Code (desarrollo) | ARGOS produccion (clientes) |
|---------|--------------------------|----------------------------|
| Acceso al sistema | Total (bash, archivos, todo) | Sandbox cerrado |
| Permisos | Pregunta cada vez | Pre-aprobados y limitados |
| Herramientas | Infinitas (bash = hace cualquier cosa) | Solo las que AiControl define |
| Se cuelga pidiendo permisos | Si | No — no hay permisos dinamicos |
| Riesgo de dano | Alto (desarrollo) | Minimo (produccion) |

#### 5 capas de proteccion tecnica

**CAPA 1 — API TOOLS (que puede hacer)**
- Whitelist cerrada: solo tracker.py, session.py, proactivo.py, etc.
- Cada tool tiene validacion de inputs (tipos, rangos, longitud)
- NINGUNA tool tiene acceso a bash/shell/exec/eval
- Claude no puede inventar tools nuevas en runtime

**CAPA 2 — FILESYSTEM (que puede ver)**
- Solo lee/escribe dentro de `argos/data/`
- Archivos del usuario: SOLO si el usuario arrastra/selecciona explicitamente
- NUNCA navega el disco libremente
- Paths controlados por la app, no por el modelo

**CAPA 3 — OPERACIONES DESTRUCTIVAS (que puede borrar)**
- `safe_delete()` → papelera con retencion 30 dias (ya implementado en db_safety.py)
- `safe_update()` → backup automatico antes de modificar
- NADA se borra definitivamente sin retencion
- Undo disponible para TODA operacion de datos

**CAPA 4 — RATE LIMITING (cuanto puede hacer)**
- Max 50 operaciones DB por minuto por usuario
- Max 10 archivos procesados por sesion
- Si algo falla 3 veces consecutivas → para y avisa al usuario
- Timeout de 30 seg por operacion individual

**CAPA 5 — AUDIT LOG (que hizo)**
- TODA operacion queda en caja negra (tabla `mensajes`)
- Timestamp + tool + parametros + resultado
- Inmutable (append-only, nunca se borra)
- El usuario puede exportar su log completo en cualquier momento

#### Matriz de riesgos y mitigaciones

| Riesgo | Mitigacion tecnica | Mitigacion legal |
|--------|-------------------|------------------|
| ARGOS borra archivo del usuario | No tiene acceso al filesystem fuera de data/ | T&C: limitacion de responsabilidad |
| ARGOS envia datos a la nube sin permiso | Solo envia texto de chat (controlado por proxy) | T&C: scope de datos explicito |
| ARGOS da mal consejo (financiero, legal, medico) | Disclaimer visible en UI: "no es asesoramiento profesional" | T&C: herramienta de asistencia, no asesor |
| ARGOS se cuelga y no responde | Timeout 30 seg + fallback a mensaje de error | SLA: sin garantia de resultado |
| Usuario pierde datos | Backup automatico diario + papelera 30 dias | T&C: usuario responsable de backups adicionales |
| Claude alucina datos incorrectos | Disclaimer en UI: "verificar informacion importante" | T&C: no garantiza precision |
| Accion no autorizada en PC del cliente | Imposible: sandbox cerrado, tools whitelist | T&C + seguro E&O |

#### Proteccion legal (requerido antes de dia 1)

**a) Terminos de Servicio:**
- "AiControl provee una herramienta de asistencia. Las decisiones y acciones son responsabilidad del usuario."
- "Responsabilidad maxima limitada al monto pagado en los ultimos 12 meses."
- Estandar en SaaS (Google, Microsoft, Notion usan clausulas similares).

**b) Consentimiento explicito por scope (pantalla de instalacion):**
```
Al instalar ARGOS, el usuario autoriza:
✅ Leer/escribir en la carpeta argos/data/
✅ Enviar texto de chat a API Claude (encriptado en transito)
✅ Enviar metricas anonimas de uso
✅ Descargar actualizaciones de AiControl

El usuario NO autoriza (y ARGOS no puede):
❌ Acceder a archivos fuera de argos/
❌ Instalar software adicional
❌ Modificar configuracion del sistema operativo
❌ Enviar archivos a la nube
❌ Acceder a otras aplicaciones
```

**c) Permisos granulares (modelo celular):**
- Si el usuario quiere procesar un archivo → lo arrastra al chat
- ARGOS lo procesa en memoria → devuelve resultado → borra temporal
- Nunca tiene acceso permanente a carpetas fuera de su sandbox

**d) Seguro E&O (Errors & Omissions):**
- Contratar seguro de responsabilidad profesional
- En Argentina: ~$200-500 USD/anio para SaaS chica
- Cubre reclamos por errores del software

**e) Compliance legal:**
- Ley 25.326 (Proteccion de datos personales, Argentina): datos nunca salen de la PC = posicion mas fuerte posible
- GDPR (si hay usuarios en UE): derecho al olvido, portabilidad, consentimiento explicito
- Registro en AAIP (Agencia de Acceso a la Informacion Publica)
- Politica de privacidad + aviso legal publicados en sitio web

---

### 8.6 Estado actual vs alcance (auditoria 5/3/2026)

> 52 requisitos funcionales totales (+3 en v0.7). Descartando cloud phase (RF-MUL).

| Area | DONE | PARTIAL | MISSING | Total | Score |
|------|------|---------|---------|-------|-------|
| Motor seguimiento (RF-SEG) | 11 | 1 | 1 | 13 | 85% |
| Proyectos (RF-PRO) | 2 | 0 | 3 | 5 | 40% |
| Personas/CRM (RF-PER) | 3 | 1 | 0 | 4 | 75% |
| Bienestar/Salud (RF-SAL) | 3 | 1 | 1 | 5 | 60% |
| Comunicacion (RF-COM) | 3 | 2 | 0 | 5 | 60% |
| Licitaciones (RF-LIC) | 5 | 0 | 0 | 5 | 100% |
| Auto-aprendizaje (RF-APR) | 3 | 1 | 0 | 4 | 75% |
| Multi-usuario (RF-MUL) | 0 | 0 | 8 | 8 | CLOUD |
| Metas (RF-MET) | 2 | 1 | 1 | 4 | 50% |
| Agenda (RF-AGE) | 2 | 1 | 0 | 3 | 67% |
| **TOTAL (sin cloud)** | **33** | **8** | **7** | **48** | **69%** |

**Gaps pendientes LOCAL (no cloud):**

| # | Gap | Prioridad | Esfuerzo |
|---|-----|-----------|----------|
| 1 | Mapeo proyectos SBD en DB (RF-PRO-02) | Alta | 2 hs |
| 2 | Reportes semanales SBD auto (RF-PRO-03) | Media | 3 hs |
| 3 | Registro auto de horas (RF-PRO-04) | Media | 4 hs |
| 4 | Dashboard cumplimiento rutinas (RF-SEG-09) | Baja | 4 hs |
| 5 | Plan nutricional con comparacion (RF-SAL-04) | Baja | 3 hs |
| 6 | Reporte semanal metas auto (RF-MET-03) | Media | 2 hs |
| 7 | Email wired a alertas (RF-COM-03 completar) | Alta | 2 hs |
| 8 | PDF cross-platform Mac (RF-MUL-07) | Alta | 3 hs |
| 9 | Nudge Telegram horario (RF-SEG-10 completar) | Media | 1 hr |
| 10 | Multi-agente activo en apertura (RF-5.4) | Baja | 2 hs |

**Estimado para 100% local: ~26 hs de trabajo**

---

## 9. Roadmap por Fases

> **Criterio:** cada fase se valida antes de pasar a la siguiente. No se avanza con cimientos flojos.
> **Pistas paralelas:** Fase 0 es prerequisito. A partir de Fase 1, infra cloud corre en paralelo.

### Fase 0: Cimientos — COMPLETADA (4/3/2026)
> Objetivo: eliminar dependencia del LLM para el flujo core. Todo por codigo.
> Resultado: 80/80 tests pasan. 13/13 modulos funcionando. 0 gaps rojos.

**0.1 Orquestador de sesion — DONE**
- [x] `tools/orquestador_sesion.py` — motor que fuerza apertura/cierre por codigo
- [x] Apertura: carga nudges + coherencia + agenda + alertas + rutinas pendientes
- [x] Checkpoint apertura: parsea respuesta natural → registra en bienestar
- [x] Cierre: checkpoint + resumen diario + aprendizaje + backup automatico
- [x] Integrado con hooks (caja_negra.py inyecta rutinas pendientes al LLM)

**0.2 Parseo de respuestas naturales — DONE**
- [x] `tools/parsear_respuesta.py` — 100+ expresiones argentinas mapeadas
- [x] "dormi 7 horas" → horas_sueno=7, "como el orto" → humor=2, "barbaro" → humor=9
- [x] Extrae: humor, energia, estres, horas_sueno, ejercicio_min, atencion_familia
- [x] `campos_faltantes()` para saber que re-preguntar

**0.3 Nudges + coherencia conectados — DONE**
- [x] `generar_nudges()` llamado en apertura() automaticamente
- [x] `reporte_coherencia()` ejecutado cada apertura (12 metas analizadas)
- [x] Ambos integrados en orquestador_sesion.py

**0.4 Aprendizaje real activado — DONE**
- [x] `tools/aprendizaje.py` — registrar_exito(), registrar_error(), buscar_solucion()
- [x] `consultar_catalogo()` — cierra el learning loop: consulta ANTES de ejecutar
- [x] Error patterns con frecuencia + confianza + solucion sugerida
- [x] Auto-aprendizaje via hook: escanea tools/ cada 20 mensajes

**0.5 Alertas de seguimiento vencido — DONE**
- [x] `tools/alertas.py` — motor rojas/amarillas/info
- [x] Alertas integradas en apertura() automaticamente
- [x] BUG-01 resuelto: seguimientos vencidos SIEMPRE visibles

**0.6 Tests basicos — DONE (80/80)**
- [x] `tests/test_fase0.py` — 7 suites, 80 tests, todos pasan
- [x] Parser, nudges, coherencia, alertas, aprendizaje, orquestador, flujo completo

**0.7 Config centralizado — DONE (agregado en iteracion)**
- [x] `tools/config.py` — un solo archivo para paths, DB, tokens, plataforma
- [x] Detecta Win/Mac/Linux/Cloud automaticamente
- [x] DB_PATH unificado (antes estaba en 5 archivos)
- [x] Lee .env sin dependencias externas

**0.8 Motor de rutinas — DONE (agregado en iteracion)**
- [x] Tabla `rutinas` con 5 seeds: apertura, cierre, almuerzo, cena, ejercicio
- [x] `get_rutinas_pendientes()` — detecta overdue automaticamente
- [x] Hook `caja_negra.py` inyecta rutinas pendientes al LLM cada mensaje
- [x] `bot/loop.py` envia recordatorio por Telegram 1x/hora si hay overdue
- [x] Racha de dias consecutivos + stats de omision

**0.9 Email reader — DONE (agregado en iteracion)**
- [x] `tools/email_reader.py` — IMAP reader con clasificacion automatica
- [x] Detecta: circulares, COMPR.AR, BAC, proveedores, financiero, agenda
- [x] `resumen_inbox()` para apertura de sesion
- [ ] Pendiente: configurar credenciales en .env y wire a alertas

**0.10 Resumen periodico — DONE (agregado en iteracion)**
- [x] `tools/resumen_periodico.py` — semanal y mensual
- [x] Promedios bienestar, actividad, insights automaticos
- [x] Tendencias vs mes anterior
- [x] Cobertura de registros

**0.11 Bugs corregidos**
- [x] MIN() en SQLite UPDATE (aprendizaje.py) — reemplazado por calculo Python
- [x] cerrar_seguimiento() sin completed_at (tracker.py) — ahora graba timestamp
- [x] Dead code _ya_registrado() en auto_aprendizaje.py — eliminado

### Fase 1: App local para Natalia (semanas del 10-24/3)
> Objetivo: ARGOS corriendo en la PC de Natalia con interfaz web local
> Criterio de exito: Natalia abre browser, chatea con ARGOS, ARGOS le trackea cosas

**1.1 Backend local — FastAPI (3-4 dias)**
- [ ] API REST local (FastAPI localhost:8000) sobre tracker.py y tools/
- [ ] Endpoint /chat: recibe mensaje → manda a Claude API → devuelve respuesta
- [ ] Endpoint /session: abrir/cerrar sesion via API
- [ ] Endpoint /tools: Claude puede llamar tools via function calling
- [ ] System prompt ARGOS: personalidad espejo, reglas, tono
- [ ] Memoria entre sesiones: historial en DB local

**1.2 Chat web basico (2-3 dias)**
- [ ] Frontend HTML/JS/CSS — un input, mensajes, nada mas
- [ ] Streaming de respuestas (no esperar todo el mensaje)
- [ ] Indicador "ARGOS esta pensando..."
- [ ] Historial de conversacion visible
- [ ] Responsive basico (PC + celular)

**1.3 Conexion con Claude API (1-2 dias)**
- [ ] Proxy basico: app local → Hetzner proxy → API Anthropic
- [ ] Control de tokens por usuario (limite diario)
- [ ] Fallback si proxy cae: mensaje de error amigable
- [ ] Function calling: Claude puede invocar tools del backend local

**1.4 Instalador (1 dia)**
- [ ] Script que instala Python + dependencias + ARGOS en PC nueva
- [ ] Crear DB vacia con seeds (checkpoints, patrones base)
- [ ] Configurar auto-arranque (abrir browser al iniciar ARGOS)
- [ ] Probarlo en PC limpia (VM o PC de test)

**1.5 Onboarding primera vez (1 dia)**
- [ ] Primera apertura: "Hola, soy ARGOS. ¿Como te llamas?"
- [ ] Preguntas basicas: nombre, a que te dedicas, que necesitas
- [ ] Registrar en DB: perfil_datos, empresa_datos
- [ ] Cargar seeds de patrones base

### Fase 2: Infraestructura cloud — en paralelo con Fase 1 (semanas del 10-24/3)
> Objetivo: proxy AiControl en Hetzner funcionando
> Se desarrolla en WSL2, se deploya con Docker

**2.1 Server Hetzner (1 dia)**
- [ ] Contratar CX22 (€3,79/mes) — ANTES del 1/4 (sube precio)
- [ ] Instalar Docker + Docker Compose
- [ ] Configurar firewall (solo 443, 22)
- [ ] Dominio aicontrol.com.ar (o .app) + HTTPS (Let's Encrypt)

**2.2 Proxy API Anthropic (2-3 dias)**
- [ ] FastAPI proxy: recibe request con JWT → valida → forward a Anthropic → responde
- [ ] Auth JWT: registro, login, validacion de token
- [ ] Control de consumo: tokens usados por usuario, limite por plan
- [ ] Rate limiting: max requests por minuto por usuario
- [ ] Logs sin datos personales (solo metricas: tokens, latencia, modelo)

**2.3 Deploy automatizado (1 dia)**
- [ ] docker-compose.yml: proxy + PostgreSQL (solo auth/metricas)
- [ ] CI/CD basico: push a main → deploy automatico
- [ ] Monitoreo: uptime check + alertas si cae
- [ ] Backup automatico DB auth (diario)

### Fase 3: Natalia — prueba de fuego (semanas del 24/3 - 7/4)
> Objetivo: Natalia usa ARGOS real en su PC, feedback directo
> Criterio de exito: Natalia lo usa 5 dias seguidos sin que se rompa

**3.1 Instalacion en PC de Natalia (1 dia)**
- [ ] Correr instalador en su PC
- [ ] Verificar que arranca, que chatea, que registra
- [ ] Configurar su cuenta en el proxy (JWT + limite tokens)
- [ ] Onboarding: que ARGOS la conozca

**3.2 Acompanamiento primera semana (5 dias)**
- [ ] Dia 1-2: estar disponible para bugs en vivo
- [ ] Dia 3-5: que use sola, registrar que pide y que falla
- [ ] Recopilar: que pidio, que funciono, que no entendio, que falta
- [ ] Iterar rapido: fix bugs en el dia

**3.3 Registro de aprendizajes (continuo)**
- [ ] Que herramientas pidio Natalia que no existen
- [ ] Que flujos no fueron naturales
- [ ] Que preguntas de checkpoint le parecieron inutiles
- [ ] Que le gustaria que ARGOS haga distinto

### Fase 4: Producto completo (semanas del 7-28/4)
> Objetivo: ARGOS con interfaz completa + herramientas + marketplace basico
> Incorporar aprendizajes de Natalia

**4.1 Interfaz mejorada (1-2 semanas)**
- [ ] File browser: arrastrar archivos al chat, procesarlos local
- [ ] Panel lateral: agenda, pendientes, metas (solo modulos activos)
- [ ] Dashboard: metricas, bienestar, coherencia
- [ ] Configuracion de modulos (activar/desactivar herramientas)
- [ ] Drag & drop para archivos

**4.2 Herramientas expandidas (1 semana)**
- [ ] Tools via function calling: Excel, Word, PDF segun lo que Natalia pidio
- [ ] Creacion de herramientas por chat: usuario pide → Claude construye → ARGOS registra
- [ ] Validacion de herramientas nuevas antes de activarlas

**4.3 Multi-usuario real (1 semana)**
- [ ] DB separada por usuario (SQLCipher)
- [ ] Cada usuario tiene su system prompt + configuracion
- [ ] Marketplace basico: AiControl publica protocolos, usuarios descargan
- [ ] 3-5 usuarios beta adicionales

### Fase 5: Lanzamiento (mayo-junio 2026)
> Objetivo: ARGOS vendible con suscripcion
> Criterio de exito: 10 usuarios pagos operativos

- [ ] Pricing final validado con beta
- [ ] Sistema de suscripciones (LemonSqueezy)
- [ ] Landing page + video demo
- [ ] Canales de venta (LinkedIn, landing, red personal)
- [ ] Soporte / FAQ / documentacion
- [ ] Marketing: Natalia como caso de exito
- [ ] T&C + politica de privacidad publicados
- [ ] Seguro E&O contratado
- [ ] 10 usuarios pagos operativos

---

## 10. Casos de Uso

### Caso 1: Reclamo laboral con evidencia (REAL, ejecutado)
**Usuario:** Gerente de proyectos IT. Necesita reclamar pago extra a su jefe.
**Lo que ARGOS hizo:** Leyo perfil (567 lineas), parseo WhatsApp (68 registros), escaneo filesystem (timestamps reales), cruzo fuentes, analizo patron del jefe, dio opinion honesta, redacto 6 versiones iterativas, armo email formal + WhatsApp, registro seguimiento con deadline.

### Caso 2: Licitacion publica completa (REAL, ejecutado)
**Usuario:** Empresa IT, licitacion privada de cableado.
**Lo que ARGOS hizo:** Genero docs Word con membrete (DDJJs, memorias tecnicas), creo CVs, descargo datasheets reales, calculo IVA mix 21%+10.5%, creo caratulas, mergeó y folio 384 paginas, convirtio docx→PDF. 26 scripts generados.

### Caso 3: Planificacion cross-life (REAL, ejecutado)
**Usuario:** Desarrollador con multiples proyectos + vida personal compleja.
**Lo que ARGOS hizo:** Releyo todos los proyectos activos, consulto agenda y pendientes, incorporo factores personales (cirugia, cumpleanos hijo, plan nutricional), cruzo areas para horas reales disponibles, genero cronograma semana a semana, cargo 12 hitos en agenda. Resultado: cronograma 14 semanas.

### Caso 4: Onboarding de proyecto externo (REAL, ejecutado)
**Usuario:** Proyecto Django desarrollado fuera de ARGOS (Bernasconi App).
**Lo que ARGOS hizo:** Exploro carpeta, leyo docs, incorporo a DB, creo seguimiento, definio protocolo de sincronizacion. Resultado: proyecto integrado en 5 minutos sin mover archivos.

### Caso 5: Plan nutricional familiar (demostrado)
Menu semanal balanceado, lista de compras categorizada, presupuesto, tracking de stock, documento para imprimir.

### Caso 6: Seguimiento de pacientes (potencial — psicologos)
Perfil por paciente, registro de sesiones, alertas de turnos, seguimiento de evolucion, facturacion, notas privadas.

### Caso 7: Gestion de emprendimiento (potencial)
Pipeline de ventas, seguimiento clientes, presupuestos profesionales, control cobros, metricas mensuales, analisis rentabilidad.

### Caso 8: Organizacion personal (potencial)
Mapear directorios, clasificar archivos, trackear fechas importantes, control de gastos, devolucion semanal.

### Caso 9: Busqueda laboral (potencial)
Unificar CV, adaptar por busqueda, cover letters personalizadas, trackear postulaciones, preparar entrevistas.

**Patron comun:** Conocer al usuario → Mapear contexto → Trackear → Asesorar → Construir lo que necesite.

---

## 11. Metodo ARGOS

### Filosofia

ARGOS no es un software que usas. Es un asistente que te conoce. La diferencia es fundamental:
- Un software tiene funciones fijas → vos te adaptas a el
- ARGOS se adapta a vos → le decis que necesitas y lo construye

El metodo tiene 5 fases. Las primeras 2 son onboarding. Las otras 3 son uso diario.

### Fase 1: Conocerte (onboarding, sesion 1)
ARGOS te hace preguntas: quien sos, a que te dedicas, que proyectos tenes, que queres lograr, que te preocupa. Se genera: perfil completo (crece con cada sesion), CLAUDE.md personalizado, MEMORY.md.

### Fase 2: Mapear tu mundo (onboarding, sesion 1-2)
ARGOS escanea tu entorno digital: carpetas, herramientas, estructura de trabajo. Se genera: mapa de archivos, base de datos con proyectos/personas/fechas. Sin mapeo, ARGOS no puede ayudarte.

### Fase 3: Trackear (uso diario)
Cada evento relevante queda registrado: mails enviados, reuniones, pendientes con deadline, eventos importantes. Eventos en DB con fecha/tipo/proyecto/persona/resultado. Metricas por periodo.

### Fase 4: Asesorar (bajo demanda)
Lee perfil completo + contexto del proyecto + historial con la persona → respuesta calibrada. Redaccion de mensajes (calibra tono), analisis de situaciones, opiniones honestas, construccion de casos con evidencia. Nunca fabrica datos. Itera rapido. Respeta decision final del usuario.

### Fase 5: Construir (cuando lo necesitas)
Le pedis una herramienta y ARGOS la construye. "Quiero trackear pacientes" → tabla + consultas. "Armame una cotizacion con IVA" → planilla con calculos. "Organizame esta carpeta" → clasifica y mueve. El usuario dice QUE. ARGOS decide COMO.

### Perfiles de usuario

| Perfil | Modulos principales | Ejemplo |
|--------|--------------------|----|
| **Project Manager** | Obra, materiales, avance, subcontratistas, cobranzas | Posadas |
| **Psicologo** | Pacientes, sesiones, evolucion, turnos, facturacion | 20 pacientes |
| **Secretaria/Admin** | Agenda, comunicaciones, tramites, archivo | Gestion turnos |
| **Emprendedor** | Pipeline ventas, cotizaciones, clientes, cobros | AiControl |
| **Personal** | Organizacion, fechas, salud, familia, busqueda laboral | Balance vida/trabajo |

Los perfiles no son excluyentes. Un usuario puede ser Project Manager en lo laboral y Personal en lo privado.

### Fase 6: Coaching (cuando el usuario lo necesita)

ARGOS no solo muestra datos (espejo) — tambien interpreta, sugiere y confronta (coach).

**Espejo:** "Dormiste 4.5hs y tu estres esta en 6/10 hace 10 dias."
**Coach:** "La inseguridad que sentis es racional, no emocional. Se resuelve con datos, no con validacion."

El coaching se activa cuando:
- El usuario pide opinion o reflexion
- ARGOS detecta patron recurrente que amerita intervencion (estres cronico, conflicto repetido)
- El usuario esta redactando comunicacion sensible (tono, estrategia, atenuantes)

El coaching NO se activa sin pedir. Regla: espejo por default, coach cuando el usuario lo pide o cuando el patron es riesgoso.

### Como funciona la inteligencia de ARGOS

La capacidad de ARGOS viene de 3 fuentes que se cruzan en tiempo real:

| Fuente | Peso aprox. | Que aporta | Sin esta fuente |
|---|---|---|---|
| **LLM (modelo base)** | ~40% | Conocimiento general, psicologia, comunicacion, logica, redaccion | Coach generico sin contexto personal |
| **DB (datos del usuario)** | ~35% | Historial, patrones, metricas, bienestar, reflexiones, seguimientos | Planilla con numeros sin interpretar |
| **Contexto de sesion** | ~25% | Lo que el usuario dice ahora, correcciones, tono, emociones | Respuestas desconectadas del momento |

**La magia esta en el cruce.** Sin DB, ARGOS dice cosas que suenan bien pero no tienen sustento.
Sin LLM, la DB es una tabla que nadie interpreta. Sin contexto, las respuestas no se ajustan al momento.

### Criterio de decision de ARGOS

1. Lee lo que el usuario dice (contexto)
2. Busca en la DB si hay patron previo (datos)
3. Cruza con conocimiento del tema (entrenamiento LLM)
4. Si hay conflicto entre las 3 fuentes → pregunta al usuario
5. Si las 3 coinciden → da la respuesta con confianza
6. Siempre etiqueta que es DATO (de la DB) y que es INTERPRETACION (del LLM)

### Confianza del cliente en el metodo

3 capas de confianza:

**Capa 1 — Transparencia radical:**
El cliente siempre puede ver de donde sale cada conclusion. "Tu estres esta en 6" → dato de la DB. "Eso es sindrome del impostor" → interpretacion del LLM. Se etiqueta.

**Capa 2 — El usuario corrige:**
Cada correccion mejora el modelo. Un coach que no acepta correcciones no es coach — es dogma. Ejemplo real: en una sesion el usuario corrigio 6 veces a ARGOS (datos familiares, materiales de obra, tono de mensaje). Cada correccion quedo registrada y mejoró futuras respuestas.

**Capa 3 — Evolucion medible:**
Si en 30 dias el usuario tiene: mas temas cerrados, menos estres, mejor sueno, mas decisiones tomadas → el metodo funciona. Si no → hay que ajustar. Los datos lo dicen, no el coach.

### Lo que hace unico al metodo

1. No es una app con botones — es una conversacion con un asistente que te conoce.
2. No tiene funciones fijas — construye lo que necesitas cuando lo necesitas.
3. No pierde contexto — memoria persistente entre sesiones.
4. No juzga — pero tampoco miente si le pedis honestidad.
5. Crece con vos — cada sesion lo hace mas util.
6. Se adapta a tu perfil — no es lo mismo un psicologo que un director de obra.
7. Es espejo Y coach — muestra patrones y tambien interpreta, sugiere y confronta cuando se lo piden.
8. Transparencia total — el usuario siempre sabe que es dato y que es interpretacion.
9. El usuario corrige a ARGOS — no es un sistema cerrado, es un dialogo que mejora con el uso.

---

## 12. Definiciones y Acronimos

| Termino              | Definicion                                                                        |
|----------------------|-----------------------------------------------------------------------------------|
| **ARGOS**            | Asistente personal inteligente. Nombre del producto (Odisea/Borges).              |
| **Caja negra**       | Tabla `mensajes`. Registro crudo de TODO, sin filtro. Analogia con avion.         |
| **Bitacora**         | Tablas `eventos` + `seguimiento`. Lo que interpreta ARGOS como relevante.         |
| **Checkpoint**       | Conjunto de preguntas obligatorias en apertura/cierre de sesion.                  |
| **Seed**             | Patron generalizable empaquetado para nuevos usuarios.                            |
| **Nudge**            | Recordatorio suave. No invasivo.                                                  |
| **Motor de rutinas** | Componente por codigo que ejecuta seguimientos sin depender del LLM.              |
| **Espejo**           | Modo de ARGOS: mostrar patrones sin juzgar. Se complementa con modo Coach.        |
| **Coach**            | Modo de ARGOS: interpretar, sugerir, confrontar. Se activa cuando el usuario lo pide o ante patron riesgoso. |
| **Bridge**           | Puente entre Telegram y Claude Code (bridge.py).                                  |
| **WAL**              | Write-Ahead Logging. Modo SQLite para concurrencia segura.                        |
| **SQLCipher**        | Extension de SQLite con encriptacion AES-256.                                     |
| **LLM**              | Large Language Model. El "cerebro" de ARGOS (Claude).                             |
| **CLI**              | Command Line Interface. Terminal donde corre Claude Code.                         |
| **SBD**              | Software By Design S.A. Empresa de Hernan.                                       |
| **AiControl**        | Marca comercial del producto ARGOS. Propiedad de Hernan Hamra.                    |
| **VPS**              | Virtual Private Server. Servidor cloud.                                           |
| **Goodhart**         | Ley de Goodhart: "cuando una medida se convierte en meta, deja de ser buena medida". Riesgo identificado por Dr. Neuro. |
| **Compliance**       | Cumplimiento normativo / regulatorio en proteccion de datos.                      |

---

## Apendice A: Fuentes de este documento

| Fuente                               | Registros analizados                            |
|--------------------------------------|--------------------------------------------------|
| `mensajes` (caja negra)             | 1.564 mensajes (feb-mar 2026)                    |
| `seguimiento` (pendientes)          | 149 total, 20+ sobre ARGOS producto              |
| `eventos`                            | 250 eventos                                      |
| `patrones`                           | 227 patrones (107 protocolos validados)          |
| `metas`                              | 12 metas activas                                 |
| `errores_argos`                      | 2 errores registrados                            |
| `reflexiones`                        | 22 reflexiones                                   |
| product/BACKLOG.md                   | 254 lineas, P0-P3                                |
| product/ALCANCE.md                   | 354 lineas, 44 capacidades listadas              |
| product/ANALISIS_BUGS_ROADMAP.md     | 295 lineas, 10 bugs + 19 features               |
| product/MIGRACION_NUBE.md            | 282 lineas, 7 alertas criticas                   |
| product/PLAN_NEGOCIO.md              | 197 lineas, modelo de negocio                    |
| product/COMPETENCIA.md               | 98 lineas, analisis competitivo                  |
| product/DECISIONES.md                | 165 lineas, 4 decisiones + consenso agentes      |
| product/FLUJO.md                     | 174 lineas, ciclo 7 pasos + 6 formatos           |
| product/METODO.md                    | 162 lineas, 5 fases + perfiles                   |
| product/CASOS_DE_USO.md              | 187 lineas, 9 casos (4 reales + 5 potenciales)   |
| product/FUNCIONES.md                 | 463 lineas, 35 capacidades detalladas            |
| product/PROMPT_SISTEMA.md            | 303 lineas, identidad + flujo + capacidades       |
| product/README.md                    | 63 lineas, historia del nombre + resumen          |
| Feedback Natalia (2026-03-03)        | 5 problemas reportados                           |

---

*Documento maestro generado por ARGOS. Absorbe 13 archivos de product/ en un unico SRS.*
*Fuente de verdad de capacidades: DB (`patrones` tabla). Este documento es referencia.*
*Ultima actualizacion: 2026-03-04 v0.3*
