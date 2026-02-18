# ARGOS — Casos de Uso
*Ejemplos reales de lo que ARGOS puede hacer*

---

## Caso 1: Reclamo laboral con evidencia (real, ejecutado)

**Usuario:** Gerente de proyectos IT
**Situación:** Necesita reclamar pago extra a su jefe, quien le pide un informe de justificación.
**Perfil del jefe:** Controla con dinero, demuestra poder, ya recortó sueldo como castigo.

### Lo que ARGOS hizo:
1. Leyó 567 líneas de perfil personal
2. Parseó chat WhatsApp → extrajo 68 registros documentados
3. Escaneó filesystem del proyecto → timestamps reales de archivos
4. Cruzó ambas fuentes → timeline unificada con evidencia verificable
5. Analizó patrón de comportamiento del jefe
6. Dio opinión honesta ("te maneja con el bolsillo")
7. Desaconsejó agregar evidencia sin timestamp verificable
8. Redactó 6 versiones iterativas del WhatsApp hasta el tono justo
9. Redactó email formal con el informe adjunto
10. Registró todo para seguimiento con deadline de 48hs

**Resultado:** Email + WhatsApp enviados. Seguimiento activo.

---

## Caso 2: Licitación pública completa (real, ejecutado)

**Usuario:** Empresa de IT
**Situación:** Presentar licitación privada de cableado estructurado. 4 carpetas, cientos de documentos.

### Lo que ARGOS hizo:
1. Generó documentos Word con membrete (DDJJs, cartas, memorias técnicas)
2. Creó CVs y organigramas desde datos del perfil
3. Descargó datasheets reales de fabricantes
4. Calculó análisis de precios con IVA mix (21% + 10.5%)
5. Creó carátulas y separadores para cada carpeta
6. Mergeó PDFs y folió 384 páginas con numeración continua
7. Convirtió docx→PDF automatizado

**Resultado:** Licitación presentada con 384 folios en 4 carpetas. 26 scripts generados.

---

## Caso 3: Plan nutricional familiar (demostrado)

**Usuario:** Familia de 5 (2 adultos + 3 adolescentes)
**Situación:** Necesita plan semanal de comidas con lista de compras y presupuesto.

### Lo que ARGOS haría:
1. Lee perfil familiar (edades, cantidad de personas, restricciones)
2. Genera menú semanal balanceado
3. Arma lista de compras categorizada (carnicería, verdulería, almacén, lácteos)
4. Estima presupuesto con precios actualizados
5. Trackea stock ("¿qué tengo / qué falta?")
6. Adapta a preferencias individuales
7. Genera documento lindo para imprimir o pegar en la heladera

**Extensiones posibles:** Recetas paso a paso, control de gastos vs presupuesto, rotación de menús.

---

## Caso 4: Seguimiento de pacientes (potencial — psicólogos)

**Usuario:** Psicóloga con consultorio
**Situación:** Trackear pacientes, sesiones, temas, evolución.

### Lo que ARGOS haría:
1. Perfil de cada paciente (datos básicos, motivo de consulta, historia)
2. Registro de cada sesión (fecha, temas, observaciones, tareas)
3. Alertas de turnos ("Mañana: María 10am, Juan 14pm")
4. Seguimiento de evolución ("María: ansiedad bajó de 8 a 5 en 3 meses")
5. Facturación (honorarios, obras sociales, cobros pendientes)
6. Notas privadas por paciente
7. Recordatorios ("Hace 2 semanas que María no viene, ¿contactar?")

**Advertencia:** Datos de pacientes pasan por Claude API. Evaluar implicaciones éticas.

---

## Caso 5: Gestión de emprendimiento (potencial)

**Usuario:** Emprendedor unipersonal
**Situación:** Maneja cotizaciones, clientes, proveedores, cobros.

### Lo que ARGOS haría:
1. Pipeline de ventas ("3 cotizaciones enviadas, 1 cerrada, 2 esperando")
2. Seguimiento de clientes con historial de interacciones
3. Generación de presupuestos con plantilla profesional
4. Control de cobros pendientes con alertas
5. Métricas mensuales ("Facturé $X, cobré $Y, pendiente $Z")
6. Redacción de comunicaciones comerciales
7. Análisis de rentabilidad por cliente/proyecto

---

## Caso 6: Organización personal (potencial)

**Usuario:** Cualquier persona
**Situación:** Vida desorganizada: archivos mezclados, fechas olvidadas, proyectos abandonados.

### Lo que ARGOS haría:
1. Mapear directorios (OneDrive, PC, nube)
2. Clasificar y reorganizar archivos
3. Trackear fechas importantes (cumpleaños, aniversarios, turnos médicos)
4. Seguimiento de trámites (AFIP, servicios, reclamos)
5. Control de gastos mensual
6. Lista de pendientes con prioridades
7. Devolución semanal: "Esta semana hiciste X, te falta Y, no te olvidés de Z"

---

## Caso 7: Búsqueda laboral (potencial)

**Usuario:** Profesional en transición
**Situación:** Múltiples CVs, relato fragmentado, postulaciones sin seguimiento.

### Lo que ARGOS haría:
1. Unificar CV en un relato potente (usando toda la historia de vida)
2. Adaptar CV por búsqueda (tech, management, data, etc.)
3. Generar cover letters personalizadas por empresa
4. Trackear postulaciones (empresa, fecha, estado, feedback)
5. Preparar para entrevistas (preguntas frecuentes + tus respuestas)
6. Seguimiento ("Mandaste CV a X hace 7 días, ¿respondieron?")
7. Análisis de mercado ("Para este puesto piden X, vos tenés Y")

---

## Patrón común

En todos los casos, ARGOS sigue el mismo método:
1. **Conocer** al usuario (perfil)
2. **Mapear** su contexto (archivos, personas, proyectos)
3. **Trackear** lo que pasa (eventos, pendientes, fechas)
4. **Asesorar** cuando lo pide (opiniones, redacción, análisis)
5. **Construir** lo que necesite (herramientas, documentos, planes)
