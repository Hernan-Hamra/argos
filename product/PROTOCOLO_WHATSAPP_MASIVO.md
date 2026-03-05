# Protocolo de Envío Masivo WhatsApp — ARGOS

## 1. Métricas del Caso PURIM 5786 (2 marzo 2026)

### Qué pasó
- **Cuenta personal** de WhatsApp (no Business) usada para envío masivo
- **Herramienta:** whatsapp-web.js (Puppeteer controlando WhatsApp Web)
- **Contenido por contacto:** 3 mensajes (texto saludo + carta JPG personalizada + PDF 37MB)

### Timeline del bloqueo
| Hora | Acción | Resultado |
|------|--------|-----------|
| 16:00 | Tanda 1 — 28 contactos | OK |
| 18:30 | Tanda 2 — 28 contactos | OK |
| 19:30 | Tanda 3 — 31 contactos | OK |
| 21:30 | Tanda 4 — 30 contactos | OK |
| 22:00 | Tanda 5 — contacto 17/28 | SESIÓN CAÍDA |
| 22:05 | Intento reconexión | **CUENTA RESTRINGIDA 24hs** |

### Números exactos al momento del bloqueo
- **134 contactos únicos** alcanzados
- **402 mensajes** enviados (134 × 3: texto + JPG + PDF)
- **~4.9 GB de PDFs** enviados (134 × 37MB)
- **6 horas** de operación continua
- **Delays usados:** 3s entre mensajes, 15s post-PDF, 8s entre contactos, 1min entre tandas de 30

### Análisis de la detección
WhatsApp detectó la cuenta por combinación de factores:
1. **Volumen:** 134 contactos nuevos en 6 horas (nunca se había chateado con ellos)
2. **Patrón repetitivo:** mismo texto base + archivo + PDF para todos
3. **Ratio envío/respuesta:** 0% de respuestas (todos eran envíos unidireccionales)
4. **Media pesada:** 37MB de PDF × 134 = enorme volumen de datos
5. **Velocidad:** aunque espaciado, el ritmo era consistente (patrón bot)
6. **Horario continuo:** 6 horas sin pausa natural

### Umbrales conocidos (investigación)
| Fuente | Límite reportado | Contexto |
|--------|------------------|----------|
| WhatsApp Business App | 256 contactos por broadcast | Límite oficial broadcast |
| Cuentas personales | ~20-30 mensajes nuevos/día | Umbral de alerta para cuentas sin historial |
| Cuentas Business API | 250 → 1000 → 10K → 100K/día | Tiers oficiales con verificación |
| Experiencia PURIM | 134 contactos = bloqueo | 3 mensajes c/u, media pesada, sin respuestas |

### Restricción aplicada
- **Tipo:** Temporal, 24 horas
- **Efecto:** No puede iniciar chats nuevos, sí puede responder existentes
- **Apelación:** Botón "Contáctanos" en Ajustes > Cuenta, no acortó el plazo
- **Resolución:** Esperar las 24 horas

## 2. Protocolo Anti-Ban (OBLIGATORIO para futuros envíos)

### Regla de oro: parecer humano, no bot

### Límites seguros por día
| Tipo de cuenta | Contactos nuevos/día | Mensajes totales/día |
|----------------|----------------------|----------------------|
| Personal (sin historial) | **máx 30-40** | máx 120 |
| Personal (con historial) | **máx 50-60** | máx 200 |
| Business App | **máx 100** | máx 300 |
| Business API (Tier 1) | **máx 250** | según tier |

### Tiempos mínimos entre mensajes
```
DELAY_ENTRE_MENSAJES = 5000    // 5s entre texto/carta/pdf
DELAY_POST_PDF       = 25000   // 25s después de media pesada (>5MB)
DELAY_ENTRE_CONTACTOS = 25000  // 25s entre contactos
DELAY_ENTRE_TANDAS   = 300000  // 5 min entre tandas
TANDA_SIZE           = 10      // máx 10 contactos por tanda
```

### Distribución horaria recomendada
- **Mañana (9-12):** máx 15-20 contactos
- **Pausa almuerzo:** mínimo 2 horas sin enviar
- **Tarde (15-18):** máx 15-20 contactos
- **Nunca enviar:** después de las 21hs ni antes de las 8hs
- **Máximo por sesión continua:** 2 horas, luego pausa de 1 hora

### Variación de contenido (anti-patrón)
- Rotar entre 3-4 variantes del texto de saludo
- Agregar nombre completo en el texto (ya lo hacemos)
- Variar el orden: a veces texto-carta-pdf, a veces carta-texto-pdf
- Agregar delay aleatorio (±30% del base) para romper patrón
- Si hay 200+ contactos: **distribuir en 5+ días**

### Campaña de 300 contactos — plan de distribución
| Día | Contactos | Horario | Nota |
|-----|-----------|---------|------|
| Día 1 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 2 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 3 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 4 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 5 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 6 | 40 | 10:00-12:00 + 15:00-17:00 | 4 tandas de 10 |
| Día 7 | 60 | Reenvíos fallidos + no encontrados | Limpieza |
| **Total** | **300** | **7 días** | Seguro |

### Checklist pre-envío (OBLIGATORIO)
- [ ] ¿La cuenta tiene historial de chat con al menos algunos destinatarios?
- [ ] ¿El volumen diario es ≤40 contactos nuevos?
- [ ] ¿Los delays están configurados en modo conservador?
- [ ] ¿El contenido tiene variaciones?
- [ ] ¿Se distribuye en múltiples días?
- [ ] ¿Se evita horario nocturno (21-8)?
- [ ] ¿Se hizo backup de la sesión WhatsApp?
- [ ] ¿Hay cuenta de respaldo lista?

### Si se bloquea la cuenta
1. **NO reintentar** — empeora la situación
2. Solicitar revisión desde Ajustes > Cuenta
3. Esperar 24-72 horas (primera vez generalmente 24h)
4. Restricciones posteriores pueden ser más largas o permanentes
5. Si es urgente: usar cuenta alternativa con ritmo aún más lento

## 3. Herramientas del Sistema

### Stack actual
```
tools/wapp_baileys/
├── enviar_wwjs.js          ← Motor principal de envío
│   ├── buscarContacto()    ← Match 3 niveles (exacto, partes, inverso)
│   ├── findCarta()         ← Busca JPG personalizada por apellido+nombre
│   ├── prepararImagen()    ← Copia carta a temp con nombre ASCII
│   ├── textoIntro()        ← Genera texto saludo con nombre
│   └── Modos: test/dry/full
├── enviar_tablas.cjs       ← Envía mensajes formateados a uno mismo (review)
├── wwjs_auth/              ← Sesión WhatsApp activa
├── wwjs_auth_hernan/       ← Sesión backup (Hernán)
├── temp/
│   ├── contactos.json      ← Todos los contactos del Excel
│   ├── restantes.json      ← Contactos pendientes
│   ├── pruebas_tanda[N].js ← Arrays pre-armados por tanda
│   ├── msg_tanda_[N].txt   ← Tablas de revisión por tanda
│   └── msg_no_encontrados.txt
├── no_encontrados.txt      ← Contactos sin match WhatsApp
└── package.json            ← whatsapp-web.js + qrcode-terminal
```

### Creación de cartas personalizadas (Pillow)
```python
from PIL import Image, ImageDraw, ImageFont
# 1. Abrir carta base (cualquier carta existente)
# 2. Blanquear rectángulo del nombre: [180, 458, 700, 498]
# 3. Escribir nuevo nombre: Times New Roman 28pt, color (50,50,50)
# 4. Guardar como "APELLIDO NOMBRE salutacion purim 5786.jpg"
```

### Campos clave por contacto
| Campo | Uso | Ejemplo |
|-------|-----|---------|
| `contacto` | Búsqueda en WhatsApp | 'Alberto Laham Berro' |
| `nombre` | Carta JPG + saludo | 'Alberto' |
| `apellido` | Carta JPG (APELLIDO NOMBRE...) | 'Laham' |
| `saludo` | Override para el texto (opcional) | 'Dr. Adrian' |

### Flujo operativo
```
1. Excel con lista de destinatarios
2. ARGOS genera PRUEBAS array con contactos
3. Modo DRY → busca matches en WhatsApp, genera tabla
4. Natalia/usuario revisa tabla → correcciones
5. ARGOS aplica correcciones (excluir, cambiar contacto, agregar)
6. Si falta carta → ARGOS la crea con Pillow
7. Modo TEST → envía usando PRUEBAS array
8. ARGOS actualiza log_envios.csv
9. Repetir por tanda
```

## 4. Módulo de Seguimiento Campañas (NUEVO — a implementar)

### Tabla propuesta: `campanas_whatsapp`
```sql
CREATE TABLE campanas_whatsapp (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,           -- 'PURIM 5786', 'Rosh Hashana 5787'
    descripcion TEXT,
    tipo TEXT,                      -- 'festivo', 'institucional', 'comercial'
    fecha_inicio DATE,
    fecha_fin DATE,
    total_destinatarios INTEGER,
    total_enviados INTEGER DEFAULT 0,
    total_fallidos INTEGER DEFAULT 0,
    total_excluidos INTEGER DEFAULT 0,
    total_no_encontrados INTEGER DEFAULT 0,
    estado TEXT DEFAULT 'preparacion', -- preparacion/en_curso/pausada/completada/bloqueada
    cuenta_whatsapp TEXT,           -- número usado
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla propuesta: `envios_whatsapp`
```sql
CREATE TABLE envios_whatsapp (
    id INTEGER PRIMARY KEY,
    campana_id INTEGER REFERENCES campanas_whatsapp(id),
    tanda INTEGER,
    nro INTEGER,
    nombre_excel TEXT,
    nombre_whatsapp TEXT,
    telefono TEXT,
    texto TEXT,                     -- 'OK' o contenido
    carta_jpg TEXT,                 -- 'OK', 'SKIP', 'CREADA'
    adjunto_pdf TEXT,               -- 'OK', 'SKIP'
    estado TEXT,                    -- COMPLETADO/ERROR/PENDIENTE/EXCLUIDO/DUDAS
    hora TIMESTAMP,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla propuesta: `listas_contactos`
```sql
CREATE TABLE listas_contactos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,           -- 'Comunidad Sefardí', 'Socios Club'
    descripcion TEXT,
    origen TEXT,                    -- 'excel', 'manual', 'whatsapp_export'
    total_contactos INTEGER,
    archivo_origen TEXT,            -- path al Excel original
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Queries útiles del módulo
```sql
-- Estado de campaña en curso
SELECT estado, COUNT(*) FROM envios_whatsapp
WHERE campana_id=? GROUP BY estado;

-- Contactos que nunca recibieron nada (cruzar campañas)
SELECT DISTINCT nombre_excel FROM envios_whatsapp
WHERE campana_id=? AND estado NOT IN ('COMPLETADO');

-- Historial de envíos a una persona
SELECT c.nombre, e.* FROM envios_whatsapp e
JOIN campanas_whatsapp c ON e.campana_id = c.id
WHERE e.nombre_excel LIKE '%Safdie%';

-- Tasa de éxito por campaña
SELECT nombre, total_enviados, total_fallidos,
  ROUND(100.0 * total_enviados / total_destinatarios, 1) as pct
FROM campanas_whatsapp;
```

## 5. Funcionalidades para el Usuario

### Lo que ARGOS ofrece hoy para campañas WhatsApp:
1. **Importar lista** desde Excel → matching automático con contactos WhatsApp
2. **Crear cartas personalizadas** (JPG) automáticamente con Pillow
3. **Revisión pre-envío** — tablas de matcheo para aprobación humana
4. **Envío masivo controlado** con anti-ban y logging completo
5. **Tracking en tiempo real** — log CSV + consola con estado por contacto
6. **Gestión de excepciones** — excluidos, dudas, no encontrados, reenvíos
7. **Reenvío selectivo** — solo los fallidos, sin duplicar
8. **Multi-sesión** — backup de cuenta WhatsApp para contingencia

### Lo que ARGOS va a ofrecer (próxima iteración):
1. **Dashboard de campaña** — estado en tiempo real desde DB
2. **Programación de envíos** — distribuir automáticamente en N días
3. **Rotación de textos** — variantes automáticas del mensaje
4. **Delays aleatorios** — randomización ±30% para parecer humano
5. **Detección proactiva** — pausar automáticamente si detecta señales de riesgo
6. **Historial cruzado** — saber qué se le envió a cada persona en todas las campañas
7. **Listas reutilizables** — guardar y actualizar grupos de contactos
8. **Reportes** — informe final para quien encargó la campaña
9. **WhatsApp Business API** — migración a canal oficial (sin riesgo de ban)

## 6. Fuentes

- [WhatsApp Messaging Limits 2026 - Chatarmin](https://chatarmin.com/en/blog/whats-app-messaging-limits)
- [WhatsApp Message Limits - SendWo](https://sendwo.com/blog/whatsapp-message-limits/)
- [WhatsApp Business Account Restricted Fix - ChakraHQ](https://chakrahq.com/article/whatsapp-business-account-restricted-fix/)
- [WhatsApp New Limits 2025 - Privyr](https://www.privyr.com/blog/whatsapp-messaging-limits/)
- [WhatsApp Messaging Limits Changes Oct 2025 - Convrs](https://convrs.io/blog/whatsapp-messaging-limits-updates/)
