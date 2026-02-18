# ARGOS — Plan de Negocio
*Versión 1.0 — Febrero 2026*

---

## El producto

**ARGOS** es un kit descargable que convierte a Claude Code en un asesor personal con IA. El usuario descarga, instala, hace el onboarding, y tiene un asistente que lo conoce y construye herramientas a medida.

### Propuesta de valor
> "Un asistente con IA que te conoce, te organiza, te asesora y construye lo que necesitás — sin que sepas programar."

### Diferenciador clave
No existe ningún producto en el mercado que combine:
- Perfil profundo del usuario (historia, personalidad, relaciones)
- Memoria persistente estructurada entre sesiones
- Ejecución de código (crea herramientas hablando)
- Asesoramiento calibrado al contexto
- Tracking multi-dominio (trabajo + personal + salud + familia)
- Todo 100% local

---

## Modelo de negocio

### Opción principal: Setup + Suscripción

| Concepto | Precio | Frecuencia |
|----------|--------|-----------|
| Setup + onboarding personalizado | USD 50-100 | Una vez |
| Suscripción ARGOS | USD 10-15/mes | Mensual |
| **Total primer mes** | **USD 60-115** | |
| **Meses siguientes** | **USD 10-15** | |

### Costos del usuario (aparte)
- Suscripción Claude Pro (Anthropic): USD 20/mes
- **Costo total usuario: USD 30-35/mes**

### Costos del creador (Hernán)
- Suscripción Claude Max propia: USD 100/mes (herramienta de trabajo)
- Hosting landing page: USD 0-10/mes (Carrd, GitHub Pages)
- Plataforma de cobro (LemonSqueezy/Gumroad): 5-8% por transacción
- Tiempo: ~30 min/semana por usuario (setup + soporte)

### Proyección de ingresos

| Usuarios | Ingreso mensual | Ingreso anual | Tu ganancia neta/mes |
|----------|----------------|---------------|---------------------|
| 5 | USD 50-75 | USD 600-900 | USD 40-65 |
| 10 | USD 100-150 | USD 1.200-1.800 | USD 90-140 |
| 20 | USD 200-300 | USD 2.400-3.600 | USD 190-290 |
| 50 | USD 500-750 | USD 6.000-9.000 | USD 490-740 |

*Nota: los setups iniciales generan picos de ingreso (50-100 por usuario nuevo).*

---

## Planes

### ARGOS Prueba (7 días gratis)
- Onboarding guiado (perfil básico)
- Tracking de proyectos (hasta 3)
- Seguimiento básico
- Sin herramientas avanzadas ni asesoramiento

### ARGOS Personal (USD 10/mes)
- Perfil completo
- Tracking ilimitado (proyectos, salud, familia, fechas)
- Asesoramiento (redacción, análisis, opiniones)
- Organización de archivos
- Construcción de herramientas a medida
- Actualizaciones mensuales

### ARGOS Business (USD 25/mes)
- Todo lo Personal +
- Módulo de licitaciones (carpetas, foliación, análisis de precios)
- Módulo de cotizaciones (IVA mix, álgebra inversa)
- Generación de documentos con membrete
- Conversión docx→PDF automatizada
- Templates empresariales

---

## Seguridad y privacidad

### Lo que comunicamos
1. **Datos 100% locales** — la DB SQLite y los archivos markdown viven en tu máquina
2. **Sin servidor central** — ARGOS no almacena nada fuera de tu computadora
3. **Sin login en nuestro sistema** — solo descarga + tu cuenta de Claude
4. **Hernán (creador) no tiene acceso a tus datos**

### Lo que advertimos
1. Los datos son procesados por Anthropic (Claude) según su política de privacidad
2. Para profesionales con datos sensibles (psicólogos, médicos): evaluar implicaciones éticas
3. Para empresas: información confidencial pasa por Claude — verificar política interna
4. Nunca guardar contraseñas, datos bancarios o datos médicos identificables

### Opción para empresas
- API key propia de Anthropic con data retention = 0
- Datos procesados pero no almacenados por Anthropic
- Costo adicional del usuario

---

## Canales de venta

### Fase 1: Red personal (mes 1-2)
- Amigos y familiares que pidieron ARGOS
- LinkedIn (publicaciones con casos anonimizados)
- Comunidad (sinagoga, conocidos, ex-colegas)
- Clientes SBD que ven el sistema funcionando

### Fase 2: Contenido (mes 2-4)
- Video demo de 3 minutos (caso real anonimizado)
- Posts LinkedIn semanales (before/after, tips, casos)
- Landing page con pricing y CTA

### Fase 3: Producto digital (mes 4+)
- Landing page con cobro automático (LemonSqueezy/Gumroad)
- ZIP descargable post-pago
- Comunidad WhatsApp/Telegram de usuarios
- Referidos (usuario trae usuario, descuento)

---

## Kit descargable (lo que recibe el usuario)

```
argos/
├── setup.py              ← Wizard de instalación + onboarding
├── CLAUDE.md             ← Se genera automáticamente en el onboarding
├── tools/
│   ├── tracker.py        ← DB SQLite + seguimiento
│   ├── doc_generator.py  ← Generación de documentos (plan Business)
│   ├── pdf_converter.py  ← Conversión docx→PDF (plan Business)
│   ├── foliador.py       ← Merge + foliación (plan Business)
│   ├── cotizacion.py     ← Análisis de precios (plan Business)
│   └── excel_tools.py    ← Excel (plan Business)
├── templates/
│   ├── CLAUDE_base.md    ← Template que se personaliza
│   └── MEMORY_base.md    ← Template de memoria
├── docs/
│   ├── METODO.md         ← El método ARGOS paso a paso
│   ├── GUIA_RAPIDA.md    ← Empezar en 10 minutos
│   └── FAQ.md            ← Preguntas frecuentes
└── data/                 ← Se crea en el setup (DB SQLite vacía)
```

---

## Roadmap

### MVP (febrero-marzo 2026)
- [ ] Setup.py con onboarding guiado
- [ ] Templates genéricos (CLAUDE.md, MEMORY.md)
- [ ] Tracker.py generalizado (sin datos hardcodeados)
- [ ] Documentación (METODO, GUIA_RAPIDA, FAQ)
- [ ] 3 usuarios piloto (amigos/familia)

### V1 (abril 2026)
- [ ] Landing page
- [ ] Cobro automatizado
- [ ] Video demo
- [ ] 10 usuarios pagos

### V2 (junio 2026)
- [ ] Dashboard visual (gráficos de actividad, balance vida/trabajo)
- [ ] WhatsApp parser generalizado
- [ ] Dir scanner
- [ ] Comunidad de usuarios
- [ ] 20+ usuarios

### V3 (septiembre 2026)
- [ ] Bot Telegram — canal de consultas rápidas + alertas automáticas
- [ ] n8n como bridge (Telegram → Claude API → DB → respuesta)
- [ ] Alertas push ("Mañana vence deadline de X")
- [ ] Envío de mensajes desde ARGOS ("Mandale esto a Richard" → envía por WhatsApp/email)
- [ ] Servidor propio o VPS para bot 24/7

### V4 (2027)
- [ ] WhatsApp Business API — acceso desde WhatsApp directo
- [ ] ARGOS como SaaS — usuario no instala nada, todo vía chat
- [ ] Multi-usuario con datos aislados por cuenta
- [ ] Panel web para dashboard y métricas

---

## Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Anthropic cambia pricing de Claude | Modelo flexible, ARGOS vale por el método no por la plataforma |
| Anthropic lanza producto similar | First mover advantage + personalización profunda |
| Usuarios no técnicos no pueden instalar | Setup guiado + soporte + video tutorial |
| Pocos usuarios pagan | Empezar con red personal, crecer orgánico |
| Tiempo de soporte escala linealmente | Documentación + FAQ + comunidad de usuarios |
