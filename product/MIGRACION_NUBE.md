# ARGOS - Alertas de Migración a la Nube
*Creado: 2 de marzo de 2026*
*Última actualización: 2 de marzo de 2026*

---

## Contexto

ARGOS hoy corre en Windows nativo (PC de Hernán). Para funcionar en la nube y servir a múltiples usuarios (empezando por Natalia en Mac), hay que resolver estas alertas ANTES del deploy.

**Principio:** una sola base de código. No se duplican herramientas por ecosistema. El 95% ya es cross-platform.

---

## ALERTA 1 — Encriptación de DB por usuario
**Prioridad: CRÍTICA** | **Estado: pendiente** | **Seguimiento DB: #100**

### Problema
Hoy `argos_tracker.db` es SQLite plano. Cualquiera con acceso al servidor puede leer datos personales de cualquier usuario (bienestar, reflexiones, salud, nutrición, mensajes, personas, metas).

### Opciones
| Opción | Ventaja | Desventaja |
|--------|---------|------------|
| **SQLCipher** | Encriptación transparente AES-256, una key por DB | Requiere compilar extensión C, no es pip install puro |
| **Cifrado app-level** | Python puro (cryptography lib), portable | Más lento, hay que cifrar/descifrar cada campo sensible |
| **DB separada + filesystem permissions** | Simple, sin cambios de código | No protege si alguien tiene acceso root al servidor |

### Recomendación
SQLCipher. Es el estándar de la industria para SQLite encriptado. Cada usuario tiene su DB con su key. Ni AiControl (el operador) puede leer datos sin la key del usuario.

### Dependencias
- Definir modelo de gestión de keys (¿el usuario la tiene? ¿se genera automáticamente?)
- Definir política de recuperación (si pierde la key, ¿se pierden los datos?)
- Evaluar impacto en performance (SQLCipher agrega ~5-15% overhead)

### Implementación estimada
- Instalar pysqlcipher3 en el entorno de deploy
- Modificar tracker.py: `sqlite3.connect()` → `sqlcipher.connect()` + `PRAGMA key`
- Script de migración: DB plana → DB encriptada (una vez por usuario)
- Test: verificar que todas las queries funcionan igual

---

## ALERTA 2 — Credenciales por usuario
**Prioridad: CRÍTICA** | **Estado: pendiente** | **Seguimiento DB: nuevo**

### Problema
Hoy hay un solo `.env` con las API keys de Hernán (Anthropic, Telegram, Groq, GitHub). En multi-usuario, cada uno tiene sus propias credenciales. Si se mezclan, un usuario podría consumir el crédito de otro o acceder a su Telegram.

### Qué necesita cada usuario
| Credencial | Por usuario | Compartida |
|-----------|-------------|-----------|
| ANTHROPIC_API_KEY | ✓ (o pool de AiControl) | Depende del modelo de negocio |
| TELEGRAM_BOT_TOKEN | ✓ (cada uno su bot) | — |
| TELEGRAM_USER_ID | ✓ | — |
| GROQ_API_KEY | — | ✓ (AiControl paga, es barato) |
| GitHub PAT | ✓ (si usa git) | — |
| DB_ENCRYPTION_KEY | ✓ | NUNCA compartida |

### Recomendación
- Un `.env` por usuario (o directorio de config por usuario)
- Variables sensibles en vault (HashiCorp Vault, AWS Secrets Manager, o archivo encriptado)
- En desarrollo local: `.env.{usuario}` con naming convention
- En nube: variables de entorno del container/VM de cada usuario

### Modelo de API Anthropic
Dos opciones:
1. **AiControl subcontrata:** AiControl tiene UNA key de Anthropic, paga el consumo, cobra al usuario en la suscripción. Más simple para el usuario.
2. **Usuario paga directo:** cada usuario crea su cuenta Anthropic y pone su key. Más barato para AiControl, más complejo para el usuario.

**Decisión pendiente** — depende del pricing final.

---

## ALERTA 3 — Archivos privados por usuario
**Prioridad: CRÍTICA** | **Estado: pendiente** | **Seguimiento DB: nuevo**

### Problema
Hoy los archivos de trabajo (Word, PDF, Excel, licitaciones) están en `C:\Users\HERNAN\OneDrive\...`. En multi-usuario:
- Cada usuario tiene sus archivos en su nube (OneDrive, Google Drive, o local)
- Un usuario NO puede ver archivos de otro
- ARGOS genera documentos (output/) que son privados de cada usuario

### Arquitectura propuesta
```
/srv/argos/
├── users/
│   ├── hernan/
│   │   ├── data/           ← DB encriptada
│   │   ├── config/         ← .env, preferences
│   │   ├── output/         ← docs generados
│   │   ├── files/          ← archivos subidos o sincronizados
│   │   └── memory/         ← MEMORY.md personal
│   ├── natalia/
│   │   ├── data/
│   │   ├── config/
│   │   ├── output/
│   │   ├── files/
│   │   └── memory/
│   └── ...
├── shared/
│   ├── tools/              ← herramientas compartidas (foliador, doc_generator, etc.)
│   ├── templates/          ← templates genéricos
│   ├── seeds/              ← patrones base para nuevos usuarios
│   └── catalogo/           ← funciones generalizadas de la comunidad
└── system/
    ├── CLAUDE.md            ← instrucciones del sistema
    └── product/             ← docs de producto
```

### Permisos
- Cada proceso de usuario corre con UID propio (Linux) o en container aislado
- `users/hernan/` solo accesible por el proceso de Hernán
- `shared/` es read-only para usuarios, write solo por el sistema
- Logs de acceso para auditoría

### Integración con nubes del usuario
- **Fase 1:** el usuario sube archivos manualmente (por Telegram o web)
- **Fase 2:** OAuth2 con Google Drive / OneDrive API — sincronización bidireccional
- **Fase 3:** cliente local que sincroniza carpetas (como Dropbox)

---

## ALERTA 4 — pdf_converter.py: win32com → LibreOffice headless
**Prioridad: MEDIA** | **Estado: pendiente** | **Seguimiento DB: #114**

### Problema
`tools/pdf_converter.py` usa `win32com.client` para abrir Word y convertir a PDF. Esto SOLO funciona en Windows con Microsoft Word instalado. En Linux/Mac/nube no existe COM.

### Solución
Reemplazar con LibreOffice headless:
```python
# Actual (solo Windows)
import win32com.client
word = win32com.client.Dispatch("Word.Application")
doc = word.Documents.Open(docx_path)
doc.SaveAs(pdf_path, FileFormatType=17)

# Nuevo (cross-platform)
import subprocess
subprocess.run([
    'soffice', '--headless', '--convert-to', 'pdf',
    '--outdir', output_dir, docx_path
])
```

### Consideraciones
- Instalar LibreOffice en el servidor (apt install libreoffice-writer)
- En Mac: `brew install libreoffice`
- Calidad de conversión: 95% idéntica a Word. Diferencias menores en fonts/kerning
- Para licitaciones (donde el formato exacto importa): mantener opción Word COM en Windows como fallback
- Implementar detección de OS automática

### Impacto
Solo 1 archivo a modificar. El resto del pipeline (doc_generator, foliador, cotización) no se toca.

---

## ALERTA 5 — Paths hardcodeados Windows
**Prioridad: MEDIA** | **Estado: pendiente** | **Seguimiento DB: #115**

### Problema
Hay rutas Windows hardcodeadas en scripts y configs:
- `C:\Users\HERNAN\OneDrive\...` en scripts de licitaciones
- `C:\Python312\python` en algunos lugares
- `r''` raw strings para paths OneDrive con caracteres especiales

### Solución
```python
# config.py (nuevo)
import os
from pathlib import Path

# Raíz del usuario (configurable por env var o archivo)
USER_ROOT = Path(os.environ.get('ARGOS_USER_ROOT', Path.home()))
DATA_DIR = USER_ROOT / 'data'
OUTPUT_DIR = USER_ROOT / 'output'
FILES_DIR = USER_ROOT / 'files'

# Python
PYTHON_CMD = 'python'  # siempre, en todos los OS
```

### Archivos a revisar
- `tools/*.py` — imports de paths
- `projects/` — scripts de licitaciones (estos son específicos de Hernán, no migran)
- `.claude/hooks/` — hooks con paths locales
- `bot/*.py` — paths de audio/temp

---

## ALERTA 6 — Separación proceso vs data
**Prioridad: ALTA** | **Estado: diseñado, no implementado**

### Qué ya está definido
En `product/ALCANCE.md` se definió el principio: **se comparte el PROCESO, nunca la DATA.** Hay 3 niveles:
1. Usuario mejora su ARGOS
2. ARGOS generaliza automáticamente
3. Distribución a otros usuarios

### Qué falta implementar
- Mecanismo de export de procesos (extraer pasos sin data)
- Catálogo central de funciones generalizadas
- Filtro por perfil de usuario
- Sistema de sugerencia al abrir sesión
- Opt-out por proceso

### Dependencia
Requiere que A1 (encriptación), A2 (credenciales) y A3 (archivos) estén resueltas primero. Sin aislamiento no hay separación real.

---

## ALERTA 7 — Marco legal y consentimiento
**Prioridad: ALTA** | **Estado: diseñado, no implementado**

### Qué ya está definido
En `product/ALCANCE.md` y `product/DECISIONES.md` (alertas del agente Ético):
- Ley 25.326 (Habeas Data Argentina)
- GDPR (UE)
- CCPA (California)
- Consentimiento explícito al registrarse
- Opt-out de generalización
- Derecho al olvido

### Qué falta implementar
- Texto legal de términos y condiciones
- Flujo de consentimiento en onboarding
- Mecanismo de borrado total (derecho al olvido)
- Log de auditoría de acceso a datos
- Política de retención de datos (¿cuánto tiempo se guardan?)
- Tratamiento especial de datos de menores (si el usuario trackea hijos)

### Dependencia
Requiere asesoría legal antes de implementar. El agente Ético marcó esto como riesgo.

---

## DECISIONES YA TOMADAS (referencia cruzada)

| Decisión | Fuente | Fecha |
|----------|--------|-------|
| DB separada por usuario | seguimiento #99 + BACKLOG.md | 27/02/2026 |
| VM/container por cliente | BACKLOG.md (arquitectura cloud) | 20/02/2026 |
| Suscripción gestionada (AiControl factura todo) | BACKLOG.md | 20/02/2026 |
| Proceso compartible, data nunca | ALCANCE.md | 22/02/2026 |
| Encriptación por usuario con key propia | ALCANCE.md #33 | 22/02/2026 |
| ARGOS es espejo, no coach | DECISIONES.md #1 | 24/02/2026 |
| Agentes invisibles para el usuario | DECISIONES.md #1 | 24/02/2026 |
| Multi-agente para desarrollo interno | DECISIONES.md #2 | 24/02/2026 |
| No WSL, mantener Windows nativo | evento #219-220 | 02/03/2026 |
| Cross-platform: una base de código | evento #220 | 02/03/2026 |
| Modelo multi-usuario cloud aprobado | evento #165 | 27/02/2026 |

---

## CHECKLIST PRE-DEPLOY

| # | Alerta | Prioridad | Estado | Bloqueante | Dependencias |
|---|--------|-----------|--------|------------|-------------|
| A1 | Encriptación DB por usuario | CRÍTICA | Pendiente | SÍ | — |
| A2 | Credenciales por usuario | CRÍTICA | Pendiente | SÍ | A1 |
| A3 | Archivos privados por usuario | CRÍTICA | Pendiente | SÍ | A2 |
| A4 | pdf_converter cross-platform | MEDIA | Pendiente | NO (workaround posible) | — |
| A5 | Paths hardcodeados | MEDIA | Pendiente | NO (solo afecta licitaciones) | — |
| A6 | Separación proceso vs data | ALTA | Diseñado | SÍ para comunidad, NO para 1 usuario | A1, A2, A3 |
| A7 | Marco legal | ALTA | Diseñado | SÍ para producción | Asesoría legal |

### Orden recomendado de implementación
```
Fase 0 (pre-requisito): A5 (paths) — es lo más simple y desbloquea testing en Linux
Fase 1 (seguridad): A1 (encriptación) → A2 (credenciales) → A3 (archivos)
Fase 2 (funcionalidad): A4 (PDF converter)
Fase 3 (producto): A6 (proceso vs data) → A7 (legal)
```

---

## Historial de cambios
| Fecha | Cambio |
|---|---|
| 02/03/2026 | Creación inicial — 7 alertas consolidadas de eventos DB + ALCANCE.md + BACKLOG.md + DECISIONES.md |
