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

## Caso 8: Planificación cross-life y cronograma balanceado (real, ejecutado)

**Usuario:** Desarrollador con múltiples proyectos + vida personal compleja
**Situación:** Tiene un proyecto de desarrollo pendiente (Bernasconi) pero también licitaciones con deadline, obra en ejecución, cirugía programada, cumpleaños familiar, plan nutricional, y búsqueda laboral pasiva. Necesita saber cuándo puede entregar Bernasconi de forma realista.

### Lo que ARGOS hizo:
1. Leyó el seguimiento completo de todos los proyectos activos (laborales, personales, desarrollo)
2. Consultó agenda DB: próximos eventos, deadlines, compromisos
3. Consultó pendientes activos con prioridades y fechas límite
4. Incorporó factores personales: cirugía rodilla (~10/03), cumpleaños hijo (26/02), plan nutricional/gym
5. Cruzó todas las áreas para encontrar horas realmente disponibles por semana
6. Estimó horas por fase del proyecto (desglose por tarea)
7. Generó cronograma semana a semana con horas disponibles reales (no teóricas)
8. Identificó ventanas de oportunidad (ej: post-cirugía = reposo pero podés codear)
9. Cargó 12 hitos en la agenda DB con fechas objetivo
10. Proyectó fecha de entrega final: mayo-junio 2026

### Capacidad demostrada:
- **Planificación cross-life:** no planificó "el proyecto" aislado, sino el proyecto DENTRO de la vida completa del usuario
- **Balance entre áreas:** trabajo SBD + desarrollo propio + salud + familia + formación
- **Estimación realista:** no horas ideales, sino horas que sobran después de todas las obligaciones
- **Portfolio multi-proyecto:** vista unificada de todos los frentes abiertos

**Resultado:** Cronograma de 14 semanas cargado en agenda. Fecha probable de entrega: fin mayo (optimista) a fin junio (realista).

---

## Caso 9: Onboarding de proyecto externo (real, ejecutado)

**Usuario:** Desarrollador que trabaja un proyecto Django fuera de ARGOS
**Situación:** Tiene un proyecto (Bernasconi App) que desarrolló con Claude Code en otra carpeta. Quiere traer el seguimiento a ARGOS sin mover el código.

### Lo que ARGOS hizo:
1. Exploró la carpeta del proyecto (CLAUDE.md, README.md, estructura)
2. Leyó documentos de soporte (.docx de reuniones, notas de trabajo)
3. Incorporó el proyecto a la DB del tracker (proyecto ID=8)
4. Creó sección en seguimiento.md con resumen + link al seguimiento detallado
5. Registró pendientes críticos en la tabla de seguimiento
6. Definió protocolo de sincronización: "actualizá Bernasconi" lee el archivo externo y carga novedades

### Capacidad demostrada:
- **ARGOS como capa de seguimiento sobre cualquier proyecto**, sin importar dónde viva el código
- **Separación datos/código:** el código queda en su carpeta, ARGOS solo gestiona el seguimiento
- **Sincronización bajo demanda:** el usuario trabaja donde quiere y sincroniza cuando vuelve

**Resultado:** Proyecto integrado en 5 minutos. Seguimiento unificado sin mover archivos.

---

## Patrón común

En todos los casos, ARGOS sigue el mismo método:
1. **Conocer** al usuario (perfil)
2. **Mapear** su contexto (archivos, personas, proyectos)
3. **Trackear** lo que pasa (eventos, pendientes, fechas)
4. **Asesorar** cuando lo pide (opiniones, redacción, análisis)
5. **Construir** lo que necesite (herramientas, documentos, planes)
