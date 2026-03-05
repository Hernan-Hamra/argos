# ARGOS — Análisis de Bugs, Roadmap y Arquitectura
**Fecha:** 3 de marzo de 2026
**Contexto:** Post-campaña Purim 5786 con Natalia

---

## 1. BUGS DETECTADOS EN CAMPAÑA PURIM

### BUG-001: Base de datos compartida (CRÍTICO)
- **Problema:** Natalia trabajó sobre la misma DB de Hernán. No hay aislamiento de datos por usuario/campaña.
- **Impacto:** Errores de seguimiento, riesgo de corrupción cruzada de datos.
- **Solución:** DB separada por usuario o por campaña. Schema multi-tenant o archivos SQLite independientes.

### BUG-002: WhatsApp bloqueado (ALTO)
- **Problema:** Meta detectó envío masivo y bloqueó el número.
- **Causa raíz:** Contenido idéntico (misma imagen) a muchos contactos en poco tiempo.
- **Mitigación actual:** Variaciones de texto (64 combos), delays aleatorios, tandas de 8.
- **Solución real:** Rate limiting inteligente, detección proactiva de señales de ban, sesiones distribuidas, o migrar a WhatsApp Business API oficial.

### BUG-003: Sin interfaz de usuario (ALTO)
- **Problema:** Todo se opera por CLI/chat. Natalia no puede ver estado, aprobar contactos, ni seguir el progreso visualmente.
- **Impacto:** Dependencia total del operador técnico (Hernán/ARGOS).
- **Solución:** Interfaz web mínima para campañas de mailing/WhatsApp.

### BUG-004: Excel como fuente de verdad incompleta (MEDIO)
- **Problema:** El script mueve archivos pero NO actualiza Excel. Estado desincronizado.
- **Impacto:** Re-envíos accidentales, confusión sobre quién recibió qué.
- **Solución:** El script debe actualizar Excel al enviar (o mejor: migrar a DB como fuente de verdad).

### BUG-005: Matching de contactos frágil (MEDIO)
- **Problema:** Nombres en Excel no coinciden con nombres en WhatsApp. Requiere correcciones manuales extensas.
- **Impacto:** 98 de 126 contactos no matchearon en primer intento.
- **Solución:** Algoritmo de fuzzy matching mejorado + cache de mapeos nombre→JID confirmados.

### BUG-006: Extensiones de archivo case-sensitive (BAJO)
- **Problema:** Script de renombrado usó .upper() en todo el filename, generando .JPG/.DOCX.
- **Impacto:** findCarta no encontraba archivos.
- **Solución ya aplicada:** Filtro case-insensitive en IMAGENES_FS.

### BUG-007: Envío a contactos no aprobados (CRÍTICO)
- **Problema:** Al cambiar nombres en Excel, el script encontró más matches de los esperados y envió sin aprobación.
- **Impacto:** 8 personas recibieron mensajes sin autorización del usuario.
- **Solución:** Whitelist obligatorio (ya implementado). Modo "solo enviar lista explícita".

### BUG-008: Cartas enviadas sin imagen personalizada (ALTO)
- **Problema:** 6 contactos recibieron texto + PDF pero sin carta JPG.
- **Causa:** IMAGENES_FS se carga al inicio y no se actualiza si cambian los archivos.
- **Solución:** Recargar lista de archivos antes de cada envío, o verificar existencia en tiempo real.

### BUG-009: Checkpoints no conectados con herramientas (MEDIO)
- **Problema:** Los checkpoints de apertura/cierre existen en la DB pero no hay herramientas que los fuercen automáticamente en contexto de campaña.
- **Solución:** Hooks específicos por tipo de actividad (campaña, sesión personal, licitación).

### BUG-010: OneDrive bloquea archivos (RECURRENTE)
- **Problema:** PermissionError al guardar Excel porque OneDrive sincroniza.
- **Mitigación:** Guardar en temp + copiar. Cerrar Excel antes.
- **Solución real:** No depender de archivos en OneDrive para operación en tiempo real. Usar DB local → exportar a Excel solo como reporte.

---

## 2. IDEAS A IMPLEMENTAR PARA ARGOS PRODUCTO

### P0 — Sin esto no hay producto
1. **Multi-tenant / bases separadas** — Cada usuario/campaña con su DB
2. **Interfaz web mínima** — Dashboard de campaña: lista contactos, estado, aprobar/rechazar, progreso en vivo
3. **WhatsApp Business API** — Reemplazar whatsapp-web.js por API oficial (requiere cuenta business verificada)
4. **Empaquetado de herramientas** — Cada módulo como servicio independiente con API clara, no scripts sueltos

### P1 — Necesario para que funcione bien
5. **Motor de campañas** — Crear campaña → importar lista → validar contactos → aprobar → programar envío → tracking
6. **Actualización automática de Excel/DB** — El envío actualiza estado en tiempo real
7. **Fuzzy matching robusto** — Levenshtein + phonetic matching + cache de JIDs confirmados
8. **Sistema de templates** — Templates de cartas parametrizados (nombre, fecha, evento) generados automáticamente
9. **Rate limiter inteligente** — Adapta velocidad según señales del servicio (delays, errores, warnings)
10. **Logs y auditoría** — Quién envió qué, cuándo, resultado, con evidencia

### P2 — Mejora la experiencia
11. **Preview antes de enviar** — Mostrar exactamente qué recibiría cada persona
12. **Programación de envíos** — "Enviar mañana a las 10am"
13. **Reportes post-campaña** — Enviados, fallidos, no encontrados, respondieron
14. **Import/export CSV/Excel** — No depender de un formato específico de Excel
15. **Notificaciones** — Telegram/email cuando termina una tanda o hay error

### P3 — Diferenciadores
16. **Multi-canal** — WhatsApp + Email + Telegram desde la misma campaña
17. **A/B testing de mensajes** — Probar variaciones y medir respuesta
18. **CRM básico integrado** — Historial de comunicación por persona
19. **Automatizaciones** — "Cuando responda, mover a grupo X"

---

## 3. QUÉ DEJAR Y QUÉ NO PARA ARGOS PRODUCTO

### MANTENER (core de ARGOS)
| Componente | Por qué |
|---|---|
| Asistente personal (espejo) | Es el diferenciador. Ningún producto hace esto bien. |
| Tracker integral (DB SQLite) | Funciona, es la base de todo. Migrar a PostgreSQL para multi-user. |
| Sistema multi-agente | Arquitectura sólida, escalable. |
| Telegram bridge | Canal de comunicación probado y estable. |
| Auto-aprendizaje | Único en el mercado. Darle más estructura. |
| Gestión de licitaciones | Vertical con valor comercial real para SBD. |

### SEPARAR COMO PRODUCTO/MÓDULO INDEPENDIENTE
| Componente | Por qué |
|---|---|
| Marketing WhatsApp/Mailing | Es un producto en sí mismo. Necesita UI propia, flujos propios, no depender del chat de ARGOS. |
| Generación de documentos | Puede ser servicio API: recibe datos → genera DOCX/PDF. |
| Foliación/merge PDF | Servicio puntual, no necesita estar en el core. |

### ELIMINAR / NO INCLUIR
| Componente | Por qué |
|---|---|
| Scripts ad-hoc (corregir_nombres.py, fix_ext.py, etc.) | Son parches de sesión, no producto. La funcionalidad debe estar en el motor de campañas. |
| Dependencia de OneDrive para operación | Fuente de bugs constante. DB como fuente de verdad, OneDrive solo para backup/compartir. |
| whatsapp-web.js para producción | Frágil, riesgo de ban, no escalable. OK para prototipo, no para producto. |

---

## 4. HOJA DE RUTA

### FASE 1 — Estabilizar en PC local (2-3 semanas)
**Objetivo:** ARGOS funcional y estable en tu máquina.

- [ ] Separar DB por contexto (personal vs campaña vs licitación)
- [ ] Empaquetar herramientas como módulos con CLI estandarizado
- [ ] Crear motor de campañas básico (Python): crear → importar → validar → enviar → reportar
- [ ] Tests automatizados para cada módulo
- [ ] Documentar protocolos en DB (no depender de interpretación del LLM)
- [ ] Fix todos los bugs BUG-001 a BUG-010
- [ ] Evaluar e implementar WSL para estabilidad (ver sección 7)

### FASE 2 — Simular servidor en local (2-3 semanas)
**Objetivo:** Correr ARGOS como si fuera un servidor, en tu PC.

- [ ] Migrar de SQLite a PostgreSQL (local)
- [ ] API REST con FastAPI (Python) para todos los módulos
- [ ] Frontend web mínimo (React o Streamlit) para campañas
- [ ] Docker containers para cada servicio
- [ ] Autenticación básica (JWT)
- [ ] Separar datos de código (volumes Docker)
- [ ] Telegram bot como servicio independiente
- [ ] Pruebas de carga simulada

### FASE 3 — Migrar a nube (2-4 semanas)
**Objetivo:** ARGOS corriendo en un servidor real.

- [ ] Elegir proveedor (Railway, Render, DigitalOcean, o AWS Lightsail)
- [ ] Deploy Docker compose en VPS
- [ ] PostgreSQL managed (o SQLite en volume persistente para empezar)
- [ ] HTTPS + dominio
- [ ] Backup automático (DB + archivos)
- [ ] Monitoreo (uptime, errores, uso)
- [ ] CI/CD básico (push → deploy)

### FASE 4 — Producto (4-8 semanas)
**Objetivo:** ARGOS usable por terceros.

- [ ] Onboarding de usuario nuevo
- [ ] Multi-tenant real
- [ ] Billing / planes
- [ ] WhatsApp Business API (reemplazar whatsapp-web.js)
- [ ] Email transaccional (SendGrid/SES)
- [ ] Dashboard analytics
- [ ] Documentación usuario

---

## 5. INFRAESTRUCTURA Y SEGURIDAD

### Datos sensibles
| Dato | Riesgo | Protección |
|---|---|---|
| DB con contactos, DNI, CUIT | Alto — datos personales (Ley 25.326) | Encriptación at rest, acceso restringido |
| Tokens Telegram/WhatsApp | Alto — acceso a cuentas | Variables de entorno, nunca en código |
| Credenciales SMTP | Medio | .env con permisos restrictivos |
| Conversaciones (caja negra) | Alto — contenido privado | Encriptación, retención limitada, purge policy |
| Backups | Alto — copia de todo | Encriptados, storage separado |

### Checklist de seguridad
- [ ] `.env` fuera del repo (ya cumplido)
- [ ] `data/` en .gitignore (ya cumplido)
- [ ] WAL mode en SQLite (ya cumplido)
- [ ] Backups encriptados (pendiente)
- [ ] Autenticación en API REST (pendiente)
- [ ] HTTPS obligatorio (pendiente)
- [ ] Rate limiting en API (pendiente)
- [ ] Logs de acceso (pendiente)
- [ ] Política de retención de datos (pendiente)
- [ ] Consentimiento de contactos para recibir mensajes (pendiente — regulatorio)

### Arquitectura de seguridad recomendada
```
Internet
    │
    ▼
[Cloudflare / Reverse Proxy] ─── HTTPS, DDoS protection, rate limit
    │
    ▼
[API Gateway] ─── Auth (JWT), logging, permisos por rol
    │
    ├── [ARGOS Core] ─── DB PostgreSQL (encriptada)
    ├── [Campaign Engine] ─── DB campañas (aislada)
    ├── [WhatsApp Service] ─── Tokens en vault
    └── [Telegram Bot] ─── Token en vault
```

---

## 6. PROPUESTAS DEL PLAN TOOLKIT (evaluación)

Del documento PLAN_TOOLKIT_CLAUDE_CODE.md:

| Propuesta | Veredicto | Razón |
|---|---|---|
| Browser automation (Playwright) | **SÍ, Fase 2** | Útil para scraping licitaciones, monitoreo de portales |
| MCP Servers | **SÍ, Fase 2** | Integración nativa de herramientas, elimina friction |
| Email sender | **SÍ, Fase 1** | Básico y necesario para campañas multi-canal |
| Clipboard tools | **NO** | No aporta valor en servidor |
| Google tools | **FASE 4** | Solo si hay demanda de usuarios |
| Sistema propio tipo Claude Code | **FASE 3-4** | Es el futuro de ARGOS, pero requiere todo lo anterior primero |
| Multi-LLM router | **FASE 4** | Optimización de costos, no prioridad ahora |
| Permisos pre-aprobados | **SÍ, Fase 1** | Mejora UX inmediata |

---

## 7. WSL vs WINDOWS — Evaluación

### Ventajas de WSL
| Aspecto | Windows nativo | WSL (Ubuntu) |
|---|---|---|
| Node.js/Python | Funciona pero paths con `\`, encoding issues | Nativo Linux, sin problemas de paths |
| Puppeteer/Chrome | Necesita .exe explícito, crashes frecuentes | Headless nativo, más estable |
| Docker | Docker Desktop (pesado, licencia) | Docker nativo, ligero |
| Cron/systemd | Task Scheduler (limitado) | systemd/cron nativos |
| Git/SSH | Funciona pero lento | Nativo, rápido |
| Encoding UTF-8 | Problemas constantes (ñ, acentos en paths) | Nativo |
| OneDrive | Acceso directo | Acceso via /mnt/c (más lento) |
| Simulación de servidor | Difícil | Idéntico a producción |

### Recomendación
**SÍ, migrar a WSL para desarrollo y simulación de servidor.**

Razones:
1. **Elimina el 80% de los bugs de encoding** que tuvimos en Purim (paths con ñ, extensiones, heredoc)
2. **Idéntico al servidor de producción** — lo que funcione en WSL va a funcionar en el VPS
3. **Docker nativo** — sin Docker Desktop
4. **Node.js y Python más estables** — sin workarounds de Windows
5. **Cron/systemd** — para programar envíos y backups

Plan de migración:
1. Instalar WSL2 + Ubuntu 24.04
2. Clonar repo ARGOS en WSL
3. Instalar Python 3.12, Node.js 20, PostgreSQL
4. Mover DB y tools a WSL
5. Acceder a archivos OneDrive via /mnt/c/ (solo para leer/exportar)
6. Correr ARGOS desde WSL, acceder desde Windows via localhost

**Cuidado:** OneDrive no sincroniza dentro de WSL. Los archivos de trabajo (Excel de campañas, cartas) se importan a la DB/storage de WSL al inicio de la campaña y se exportan al final. OneDrive queda como repositorio de originales, no como storage operativo.

---

## 8. RESUMEN EJECUTIVO

### Estado actual
ARGOS funciona como asistente personal para Hernán. La campaña Purim demostró que el módulo de marketing tiene potencial pero no está listo para terceros.

### Qué falta para producto
1. **Aislamiento de datos** — cada usuario/campaña en su sandbox
2. **Interfaz visual** — no todo puede ser chat
3. **Herramientas empaquetadas** — módulos con API clara, no scripts interpretados por el LLM
4. **Estabilidad** — WSL + Docker + PostgreSQL
5. **Seguridad** — encriptación, auth, permisos

### Orden de prioridades
1. Fix bugs críticos (BUG-001, BUG-007)
2. Migrar a WSL
3. Empaquetar motor de campañas
4. API REST + frontend mínimo
5. Docker + simulación servidor
6. Migrar a nube
7. Multi-tenant + producto

### Inversión estimada
| Fase | Esfuerzo | Costo infra |
|---|---|---|
| Fase 1 (estabilizar) | 2-3 semanas dev | $0 (local) |
| Fase 2 (simular servidor) | 2-3 semanas dev | $0 (local) |
| Fase 3 (nube) | 2-4 semanas dev | ~$20-50 USD/mes (VPS + DB) |
| Fase 4 (producto) | 4-8 semanas dev | ~$50-100 USD/mes |

---

**Fin del análisis. Guardado en: product/ANALISIS_BUGS_ROADMAP.md**
