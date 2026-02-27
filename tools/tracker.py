"""
ARGOS Tracker - Sistema de seguimiento personal y laboral
Una sola DB (argos_tracker.db) con todo junto.
En cloud se separa en sistema + usuario.
"""

import sqlite3
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'argos_tracker.db')


def get_connection():
    """Conectar a la DB. Crea directorio data/ si no existe."""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Alias para que el código de capacidades no se rompa
get_connection_sistema = get_connection


def init_db():
    """Crear todas las tablas si no existen."""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, tipo TEXT NOT NULL, categoria TEXT,
        estado TEXT DEFAULT 'activo', fecha_inicio TEXT, fecha_fin TEXT,
        descripcion TEXT, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, relacion TEXT, empresa TEXT, contacto TEXT,
        notas TEXT, perfil_comportamiento TEXT,
        dni TEXT, cuit TEXT, fecha_nacimiento TEXT, lugar_nacimiento TEXT,
        domicilio TEXT, cargo TEXT, estado_civil TEXT, nacionalidad TEXT, sexo TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL, hora TEXT, tipo TEXT NOT NULL, subtipo TEXT,
        proyecto_id INTEGER, persona_id INTEGER,
        descripcion TEXT NOT NULL, fuente TEXT, resultado TEXT,
        duracion_min INTEGER, energia INTEGER, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS seguimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER, proyecto_id INTEGER, persona_id INTEGER,
        accion TEXT NOT NULL, fecha_limite TEXT,
        estado TEXT DEFAULT 'pendiente', prioridad TEXT DEFAULT 'media',
        recordatorio TEXT, resultado TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        completed_at TEXT,
        FOREIGN KEY (evento_id) REFERENCES eventos(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS fechas_importantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER, tipo TEXT NOT NULL, fecha TEXT NOT NULL,
        fecha_hebreo TEXT, descripcion TEXT, recurrente INTEGER DEFAULT 1, notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS salud (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER, tipo TEXT NOT NULL, fecha TEXT, hora TEXT,
        profesional TEXT, lugar TEXT, especialidad TEXT, descripcion TEXT,
        estado TEXT DEFAULT 'pendiente', resultado TEXT, proxima_cita TEXT, notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL, tipo TEXT NOT NULL,
        proyectos_activos INTEGER, eventos_dia INTEGER, eventos_semana INTEGER,
        horas_laboral REAL, horas_personal REAL, horas_salud REAL, horas_formacion REAL,
        balance_vida_trabajo REAL, energia_promedio REAL,
        pendientes_abiertos INTEGER, pendientes_vencidos INTEGER, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER, tag TEXT NOT NULL,
        FOREIGN KEY (evento_id) REFERENCES eventos(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS agenda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL, hora TEXT, hora_fin TEXT, titulo TEXT NOT NULL,
        tipo TEXT NOT NULL, proyecto_id INTEGER, persona_id INTEGER,
        lugar TEXT, descripcion TEXT, recurrente TEXT,
        recordatorio_dias INTEGER DEFAULT 1, estado TEXT DEFAULT 'pendiente', notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS nutricion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL, comida TEXT NOT NULL, descripcion TEXT NOT NULL,
        del_plan INTEGER DEFAULT 1, proteina INTEGER DEFAULT 0, vegetales INTEGER DEFAULT 0,
        agua_litros REAL, suplementos TEXT, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS capacidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE, nombre_display TEXT NOT NULL,
        descripcion TEXT, herramienta TEXT, protocolo TEXT, categoria TEXT,
        version INTEGER DEFAULT 1, origen TEXT DEFAULT 'sistema',
        es_generalizable INTEGER DEFAULT 1, perfiles TEXT, keywords TEXT,
        veces_usada INTEGER DEFAULT 1, ultima_vez TEXT,
        estado TEXT DEFAULT 'activa', mejora_de INTEGER, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (mejora_de) REFERENCES capacidades(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS patrones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_deteccion TEXT NOT NULL, tipo TEXT NOT NULL, categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL, evidencia TEXT,
        frecuencia INTEGER DEFAULT 1, confianza REAL DEFAULT 0.5,
        estado TEXT DEFAULT 'detectado', sugerencia TEXT,
        compartido INTEGER DEFAULT 0, anonimizado_en TEXT, ultimo_visto TEXT, notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # === DATOS EMPRESA (info corporativa para formularios) ===

    c.execute('''CREATE TABLE IF NOT EXISTS empresa_datos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campo TEXT NOT NULL,
        valor TEXT NOT NULL,
        categoria TEXT DEFAULT 'general',
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # === METAS (intenciones declaradas) ===

    c.execute('''CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        area TEXT NOT NULL,
        proyecto_id INTEGER,
        prioridad TEXT DEFAULT 'media',
        fecha_objetivo TEXT,
        horas_semana_meta REAL,
        indicador TEXT DEFAULT 'horas',
        estado TEXT DEFAULT 'activa',
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
    )''')

    # === SISTEMA MULTI-AGENTE ===

    c.execute('''CREATE TABLE IF NOT EXISTS agentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        estado TEXT DEFAULT 'activo',
        prompt_file TEXT,
        capacidades TEXT,
        triggers TEXT,
        fecha_creacion TEXT DEFAULT (date('now','localtime')),
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS consultas_agente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agente_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT,
        tipo TEXT,
        contexto TEXT,
        resultado TEXT,
        confianza REAL DEFAULT 0.8,
        aceptado INTEGER DEFAULT NULL,
        evento_id INTEGER,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (agente_id) REFERENCES agentes(id),
        FOREIGN KEY (evento_id) REFERENCES eventos(id)
    )''')

    # Agregar agente_id a eventos si no existe
    try:
        c.execute("ALTER TABLE eventos ADD COLUMN agente_id INTEGER REFERENCES agentes(id)")
    except sqlite3.OperationalError:
        pass  # Columna ya existe

    c.execute('''CREATE TABLE IF NOT EXISTS bienestar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        persona_id INTEGER DEFAULT 12,
        humor INTEGER,                   -- 1-10 (1=pésimo, 10=excelente)
        energia INTEGER,                 -- 1-10
        estres INTEGER,                  -- 1-10 (10=máximo estrés)
        horas_sueno REAL,                -- horas dormidas
        calidad_sueno INTEGER,           -- 1-5 (1=pésima, 5=excelente)
        atencion_familia INTEGER,        -- 1-5 (1=nula, 5=plena)
        ejercicio_min INTEGER DEFAULT 0, -- minutos de ejercicio
        intensidad_laboral INTEGER,      -- 1-10 (calculado: tareas + interlocutores + presión)
        intensidad_personal INTEGER,     -- 1-10 (carga emocional, temas personales)
        interlocutores INTEGER,          -- cantidad de personas con las que habló
        tareas_contadas INTEGER,         -- tareas registradas en el día
        conflictos TEXT,                 -- descripción breve de conflictos del día
        logros TEXT,                     -- qué salió bien
        frustraciones TEXT,              -- qué generó frustración
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # === SESIONES (A1: protocolo de sesión en código) ===

    c.execute('''CREATE TABLE IF NOT EXISTS sesiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT,
        duracion_min INTEGER,
        estado TEXT DEFAULT 'abierta',
        proyecto_id INTEGER,
        resumen TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
    )''')

    # === MENSAJES (A2: registro de Q&A) ===

    c.execute('''CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sesion_id INTEGER,
        timestamp TEXT NOT NULL,
        rol TEXT NOT NULL,
        contenido TEXT NOT NULL,
        tipo TEXT DEFAULT 'mensaje',
        tokens_estimados INTEGER,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (sesion_id) REFERENCES sesiones(id)
    )''')

    # === REFLEXIONES (sensaciones, opiniones, pensamientos para retomar) ===

    c.execute('''CREATE TABLE IF NOT EXISTS reflexiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT,
        tema TEXT NOT NULL,
        contenido TEXT NOT NULL,
        sentimiento TEXT DEFAULT 'neutro',
        intensidad INTEGER DEFAULT 3,
        area TEXT DEFAULT 'personal',
        tags TEXT,
        sesion_id INTEGER,
        revisado INTEGER DEFAULT 0,
        fecha_revision TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (sesion_id) REFERENCES sesiones(id)
    )''')

    conn.commit()
    conn.close()
    print(f"DB inicializada en: {os.path.abspath(DB_PATH)}")


# === FUNCIONES DE INSERCIÓN ===

def add_proyecto(nombre, tipo, categoria=None, estado='activo', descripcion=None, fecha_inicio=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO proyectos (nombre, tipo, categoria, estado, descripcion, fecha_inicio)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (nombre, tipo, categoria, estado, descripcion, fecha_inicio))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid


def add_persona(nombre, relacion=None, empresa=None, contacto=None, notas=None, perfil=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO personas (nombre, relacion, empresa, contacto, notas, perfil_comportamiento)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (nombre, relacion, empresa, contacto, notas, perfil))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid


def add_evento(fecha, tipo, descripcion, subtipo=None, hora=None, proyecto_id=None,
               persona_id=None, fuente=None, resultado=None, duracion_min=None,
               energia=None, notas=None):
    # A3: auto-fill hora si no viene
    if hora is None:
        hora = datetime.now().strftime('%H:%M')
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO eventos (fecha, hora, tipo, subtipo, proyecto_id, persona_id,
                 descripcion, fuente, resultado, duracion_min, energia, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (fecha, hora, tipo, subtipo, proyecto_id, persona_id,
               descripcion, fuente, resultado, duracion_min, energia, notas))
    eid = c.lastrowid
    conn.commit()
    conn.close()
    return eid


def add_mensaje(sesion_id, rol, contenido, tipo='mensaje', tokens_estimados=None):
    """Registrar un mensaje de la conversación.
    rol: 'user' o 'assistant'
    tipo: 'pregunta', 'respuesta', 'accion', 'decision', 'checkpoint', 'mensaje'
    """
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Estimar tokens si no viene: ~1 token por 4 caracteres
    if tokens_estimados is None:
        tokens_estimados = len(contenido) // 4
    c.execute('''INSERT INTO mensajes (sesion_id, timestamp, rol, contenido, tipo, tokens_estimados)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (sesion_id, ahora, rol, contenido, tipo, tokens_estimados))
    mid = c.lastrowid
    conn.commit()
    conn.close()
    return mid


def add_reflexion(tema, contenido, sentimiento='neutro', intensidad=3, area='personal',
                  tags=None, sesion_id=None, notas=None):
    """Registrar una reflexión/sensación/opinión sobre un tema.
    sentimiento: positivo/negativo/neutro/mixto
    intensidad: 1-5 (qué tan fuerte)
    area: laboral/personal/salud/familia/proyecto/otro
    tags: string separado por comas para búsqueda posterior
    """
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now()
    c.execute('''INSERT INTO reflexiones (fecha, hora, tema, contenido, sentimiento, intensidad,
                 area, tags, sesion_id, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (ahora.strftime('%Y-%m-%d'), ahora.strftime('%H:%M'),
               tema, contenido, sentimiento, intensidad, area, tags, sesion_id, notas))
    rid = c.lastrowid
    conn.commit()
    conn.close()
    return rid


def get_reflexiones(tema=None, area=None, sin_revisar=False, limit=20):
    """Buscar reflexiones por tema, área, o sin revisar."""
    conn = get_connection()
    c = conn.cursor()
    query = 'SELECT * FROM reflexiones WHERE 1=1'
    params = []
    if tema:
        query += ' AND tema LIKE ?'
        params.append(f'%{tema}%')
    if area:
        query += ' AND area = ?'
        params.append(area)
    if sin_revisar:
        query += ' AND revisado = 0'
    query += ' ORDER BY fecha DESC, hora DESC LIMIT ?'
    params.append(limit)
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def marcar_reflexion_revisada(reflexion_id):
    """Marcar una reflexión como revisada (retomada en sesión)."""
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now().strftime('%Y-%m-%d')
    c.execute('UPDATE reflexiones SET revisado = 1, fecha_revision = ? WHERE id = ?',
              (ahora, reflexion_id))
    conn.commit()
    conn.close()
    return True


def add_seguimiento(accion, fecha_limite=None, proyecto_id=None, persona_id=None,
                    evento_id=None, prioridad='media'):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO seguimiento (evento_id, proyecto_id, persona_id, accion,
                 fecha_limite, prioridad)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (evento_id, proyecto_id, persona_id, accion, fecha_limite, prioridad))
    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid


def add_fecha_importante(persona_id, tipo, fecha, descripcion=None, fecha_hebreo=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO fechas_importantes (persona_id, tipo, fecha, fecha_hebreo, descripcion)
                 VALUES (?, ?, ?, ?, ?)''',
              (persona_id, tipo, fecha, fecha_hebreo, descripcion))
    fid = c.lastrowid
    conn.commit()
    conn.close()
    return fid


def add_salud(persona_id, tipo, fecha=None, hora=None, profesional=None,
              lugar=None, especialidad=None, descripcion=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO salud (persona_id, tipo, fecha, hora, profesional,
                 lugar, especialidad, descripcion)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (persona_id, tipo, fecha, hora, profesional, lugar, especialidad, descripcion))
    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid


def add_agenda(fecha, titulo, tipo, hora=None, hora_fin=None, proyecto_id=None,
               persona_id=None, lugar=None, descripcion=None, recurrente=None,
               recordatorio_dias=1, estado='pendiente'):
    """Agregar evento a la agenda."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO agenda (fecha, hora, hora_fin, titulo, tipo, proyecto_id,
                 persona_id, lugar, descripcion, recurrente, recordatorio_dias, estado)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (fecha, hora, hora_fin, titulo, tipo, proyecto_id, persona_id,
               lugar, descripcion, recurrente, recordatorio_dias, estado))
    aid = c.lastrowid
    conn.commit()
    conn.close()
    return aid


def update_agenda(agenda_id, **kwargs):
    """Actualizar un evento de agenda. Pasar campos como keyword args."""
    conn = get_connection()
    c = conn.cursor()
    campos_validos = ['fecha', 'hora', 'hora_fin', 'titulo', 'tipo', 'proyecto_id',
                      'persona_id', 'lugar', 'descripcion', 'recurrente',
                      'recordatorio_dias', 'estado', 'notas']
    sets = []
    vals = []
    for k, v in kwargs.items():
        if k in campos_validos:
            sets.append(f"{k} = ?")
            vals.append(v)
    if sets:
        vals.append(agenda_id)
        c.execute(f"UPDATE agenda SET {', '.join(sets)} WHERE id = ?", vals)
        conn.commit()
    conn.close()


# === FUNCIONES DE CONSULTA ===

def get_pendientes(incluir_vencidos=True):
    """Obtener todos los seguimientos pendientes."""
    conn = get_connection()
    c = conn.cursor()
    if incluir_vencidos:
        c.execute('''SELECT s.*, p.nombre as proyecto, pe.nombre as persona
                     FROM seguimiento s
                     LEFT JOIN proyectos p ON s.proyecto_id = p.id
                     LEFT JOIN personas pe ON s.persona_id = pe.id
                     WHERE s.estado IN ('pendiente', 'en_curso', 'vencido')
                     ORDER BY s.prioridad DESC, s.fecha_limite ASC''')
    else:
        c.execute('''SELECT s.*, p.nombre as proyecto, pe.nombre as persona
                     FROM seguimiento s
                     LEFT JOIN proyectos p ON s.proyecto_id = p.id
                     LEFT JOIN personas pe ON s.persona_id = pe.id
                     WHERE s.estado IN ('pendiente', 'en_curso')
                     ORDER BY s.prioridad DESC, s.fecha_limite ASC''')
    rows = c.fetchall()
    conn.close()
    return rows


def get_agenda_dia(fecha=None):
    """Obtener agenda de un día específico."""
    conn = get_connection()
    c = conn.cursor()
    if fecha is None:
        fecha = date.today().isoformat()
    c.execute('''SELECT a.*, p.nombre as proyecto, pe.nombre as persona
                 FROM agenda a
                 LEFT JOIN proyectos p ON a.proyecto_id = p.id
                 LEFT JOIN personas pe ON a.persona_id = pe.id
                 WHERE a.fecha = ? AND a.estado != 'cancelado'
                 ORDER BY a.hora ASC''', (fecha,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_agenda_semana(fecha_desde=None):
    """Obtener agenda de los próximos 7 días."""
    conn = get_connection()
    c = conn.cursor()
    if fecha_desde is None:
        fecha_desde = date.today().isoformat()
    from datetime import timedelta
    fecha_hasta = (date.fromisoformat(fecha_desde) + timedelta(days=7)).isoformat()
    c.execute('''SELECT a.*, p.nombre as proyecto, pe.nombre as persona
                 FROM agenda a
                 LEFT JOIN proyectos p ON a.proyecto_id = p.id
                 LEFT JOIN personas pe ON a.persona_id = pe.id
                 WHERE a.fecha BETWEEN ? AND ? AND a.estado != 'cancelado'
                 ORDER BY a.fecha ASC, a.hora ASC''',
              (fecha_desde, fecha_hasta))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_alertas_agenda(fecha=None):
    """Obtener recordatorios: eventos cuyo recordatorio cae hoy."""
    conn = get_connection()
    c = conn.cursor()
    if fecha is None:
        fecha = date.today().isoformat()
    c.execute('''SELECT a.*, p.nombre as proyecto, pe.nombre as persona
                 FROM agenda a
                 LEFT JOIN proyectos p ON a.proyecto_id = p.id
                 LEFT JOIN personas pe ON a.persona_id = pe.id
                 WHERE a.estado IN ('pendiente', 'confirmado')
                 AND date(a.fecha, '-' || a.recordatorio_dias || ' days') <= ?
                 AND a.fecha >= ?
                 ORDER BY a.fecha ASC, a.hora ASC''',
              (fecha, fecha))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_eventos_periodo(fecha_desde, fecha_hasta=None):
    """Obtener eventos en un período."""
    conn = get_connection()
    c = conn.cursor()
    if fecha_hasta is None:
        fecha_hasta = datetime.now().strftime('%Y-%m-%d')
    c.execute('''SELECT e.*, p.nombre as proyecto, pe.nombre as persona
                 FROM eventos e
                 LEFT JOIN proyectos p ON e.proyecto_id = p.id
                 LEFT JOIN personas pe ON e.persona_id = pe.id
                 WHERE e.fecha BETWEEN ? AND ?
                 ORDER BY e.fecha ASC, e.hora ASC''',
              (fecha_desde, fecha_hasta))
    rows = c.fetchall()
    conn.close()
    return rows


def get_proximas_fechas(dias=30):
    """Obtener fechas importantes en los próximos N días."""
    conn = get_connection()
    c = conn.cursor()
    hoy = date.today()
    c.execute('''SELECT f.*, pe.nombre as persona
                 FROM fechas_importantes f
                 LEFT JOIN personas pe ON f.persona_id = pe.id
                 WHERE f.recurrente = 1
                 ORDER BY f.fecha ASC''')
    rows = c.fetchall()
    conn.close()

    # Filtrar por proximidad (comparar MM-DD)
    proximas = []
    for row in rows:
        fecha_str = dict(row)['fecha']
        try:
            if len(fecha_str) == 5:  # MM-DD
                mes, dia = int(fecha_str[:2]), int(fecha_str[3:])
            else:  # YYYY-MM-DD
                mes, dia = int(fecha_str[5:7]), int(fecha_str[8:10])
            fecha_este_ano = date(hoy.year, mes, dia)
            if fecha_este_ano < hoy:
                fecha_este_ano = date(hoy.year + 1, mes, dia)
            diff = (fecha_este_ano - hoy).days
            if diff <= dias:
                proximas.append((dict(row), diff))
        except (ValueError, IndexError):
            continue

    proximas.sort(key=lambda x: x[1])
    return proximas


def get_metricas_resumen(fecha_desde=None):
    """Resumen de métricas: eventos por tipo, proyectos activos, balance."""
    conn = get_connection()
    c = conn.cursor()

    if fecha_desde is None:
        fecha_desde = '2025-01-01'

    # Eventos por tipo
    c.execute('''SELECT tipo, COUNT(*) as total FROM eventos
                 WHERE fecha >= ? GROUP BY tipo ORDER BY total DESC''', (fecha_desde,))
    por_tipo = c.fetchall()

    # Eventos por proyecto
    c.execute('''SELECT p.nombre, COUNT(*) as total FROM eventos e
                 JOIN proyectos p ON e.proyecto_id = p.id
                 WHERE e.fecha >= ? GROUP BY p.nombre ORDER BY total DESC''', (fecha_desde,))
    por_proyecto = c.fetchall()

    # Eventos por mes
    c.execute('''SELECT substr(fecha, 1, 7) as mes, COUNT(*) as total FROM eventos
                 WHERE fecha >= ? GROUP BY mes ORDER BY mes ASC''', (fecha_desde,))
    por_mes = c.fetchall()

    # Proyectos activos
    c.execute("SELECT COUNT(*) FROM proyectos WHERE estado = 'activo'")
    activos = c.fetchone()[0]

    # Pendientes
    c.execute("SELECT COUNT(*) FROM seguimiento WHERE estado IN ('pendiente', 'en_curso')")
    pendientes = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM seguimiento WHERE estado = 'vencido'")
    vencidos = c.fetchone()[0]

    conn.close()
    return {
        'por_tipo': [dict(r) for r in por_tipo],
        'por_proyecto': [dict(r) for r in por_proyecto],
        'por_mes': [dict(r) for r in por_mes],
        'proyectos_activos': activos,
        'pendientes': pendientes,
        'vencidos': vencidos
    }


# === CAPACIDADES (catálogo dinámico herramienta + protocolo) ===

def add_capacidad(nombre, nombre_display, descripcion=None, herramienta=None,
                  protocolo=None, categoria=None, origen='sistema',
                  es_generalizable=1, perfiles=None, keywords=None, notas=None):
    """Registrar una capacidad nueva en el catálogo dinámico.
    Va a DB SISTEMA (compartible).
    """
    import json as _json
    conn = get_connection_sistema()
    c = conn.cursor()
    hoy = date.today().isoformat()

    # Serializar protocolo si es dict/list
    if isinstance(protocolo, (dict, list)):
        protocolo = _json.dumps(protocolo, ensure_ascii=False)
    if isinstance(perfiles, list):
        perfiles = _json.dumps(perfiles, ensure_ascii=False)
    if isinstance(keywords, list):
        keywords = ', '.join(keywords)

    c.execute('''INSERT INTO capacidades (nombre, nombre_display, descripcion, herramienta,
                 protocolo, categoria, origen, es_generalizable, perfiles, keywords,
                 ultima_vez, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (nombre, nombre_display, descripcion, herramienta, protocolo,
               categoria, origen, es_generalizable, perfiles, keywords, hoy, notas))
    cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid


def mejorar_capacidad(capacidad_id, nueva_herramienta=None, nuevo_protocolo=None,
                      nueva_descripcion=None, notas_mejora=None):
    """Registrar una mejora a una capacidad existente. DB SISTEMA."""
    import json as _json
    conn = get_connection_sistema()
    c = conn.cursor()

    # Leer la capacidad actual
    c.execute('SELECT * FROM capacidades WHERE id = ?', (capacidad_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None

    original = dict(row)

    # Marcar la anterior como mejorada
    c.execute('''UPDATE capacidades SET estado = 'mejorada',
                 updated_at = datetime('now','localtime') WHERE id = ?''', (capacidad_id,))

    # Serializar si es necesario
    protocolo = nuevo_protocolo or original['protocolo']
    if isinstance(protocolo, (dict, list)):
        protocolo = _json.dumps(protocolo, ensure_ascii=False)

    # Crear nueva versión
    nueva_version = (original['version'] or 1) + 1
    nombre_v = original['nombre']  # mismo nombre, nueva versión

    c.execute('''INSERT INTO capacidades (nombre, nombre_display, descripcion, herramienta,
                 protocolo, categoria, version, origen, es_generalizable, perfiles,
                 keywords, veces_usada, ultima_vez, estado, mejora_de, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'activa', ?, ?)''',
              (nombre_v + f'_v{nueva_version}',
               original['nombre_display'],
               nueva_descripcion or original['descripcion'],
               nueva_herramienta or original['herramienta'],
               protocolo,
               original['categoria'],
               nueva_version,
               original['origen'],
               original['es_generalizable'],
               original['perfiles'],
               original['keywords'],
               original['veces_usada'],
               date.today().isoformat(),
               capacidad_id,
               notas_mejora or f'Mejora de v{original["version"]}'))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id


def usar_capacidad(nombre):
    """Incrementar contador de uso de una capacidad por nombre. DB SISTEMA."""
    conn = get_connection_sistema()
    c = conn.cursor()
    hoy = date.today().isoformat()
    c.execute('''UPDATE capacidades SET veces_usada = veces_usada + 1,
                 ultima_vez = ?, updated_at = datetime('now','localtime')
                 WHERE nombre = ? AND estado = 'activa' ''', (hoy, nombre))
    conn.commit()
    conn.close()


def get_catalogo(solo_activas=True):
    """Obtener catálogo completo de capacidades. DB SISTEMA."""
    conn = get_connection_sistema()
    c = conn.cursor()
    if solo_activas:
        c.execute('''SELECT * FROM capacidades WHERE estado = 'activa'
                     ORDER BY categoria, veces_usada DESC''')
    else:
        c.execute('SELECT * FROM capacidades ORDER BY categoria, nombre, version DESC')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def buscar_capacidad(texto):
    """Buscar capacidades por texto. DB SISTEMA."""
    conn = get_connection_sistema()
    c = conn.cursor()
    patron = f'%{texto.lower()}%'
    c.execute('''SELECT * FROM capacidades
                 WHERE estado = 'activa'
                 AND (LOWER(nombre) LIKE ? OR LOWER(nombre_display) LIKE ?
                      OR LOWER(descripcion) LIKE ? OR LOWER(keywords) LIKE ?
                      OR LOWER(herramienta) LIKE ? OR LOWER(protocolo) LIKE ?)
                 ORDER BY veces_usada DESC''',
              (patron, patron, patron, patron, patron, patron))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_capacidad_por_nombre(nombre):
    """Obtener una capacidad activa por su nombre exacto. DB SISTEMA."""
    conn = get_connection_sistema()
    c = conn.cursor()
    c.execute('''SELECT * FROM capacidades WHERE nombre = ? AND estado = 'activa' ''', (nombre,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_historial_capacidad(nombre_base):
    """Ver todas las versiones de una capacidad. DB SISTEMA."""
    conn = get_connection_sistema()
    c = conn.cursor()
    patron = f'{nombre_base}%'
    c.execute('''SELECT * FROM capacidades WHERE nombre LIKE ?
                 ORDER BY version ASC''', (patron,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# === FUNCIONES DE HORAS Y SESIONES ===

def registrar_sesion(fecha, tipo, descripcion, duracion_min, hora_inicio=None,
                     proyecto_id=None, persona_id=None, subtipo='sesion', notas=None):
    """Shortcut para registrar una sesión de trabajo con duración.
    tipo: 'laboral' o 'personal'
    duracion_min: minutos trabajados
    hora_inicio: HH:MM (opcional, si no se pone usa la hora actual)
    """
    if hora_inicio is None:
        hora_inicio = datetime.now().strftime('%H:%M')
    return add_evento(fecha, tipo, descripcion, subtipo=subtipo, hora=hora_inicio,
                      proyecto_id=proyecto_id, persona_id=persona_id,
                      fuente='sistema', duracion_min=duracion_min, notas=notas)


def registrar_entrenamiento(fecha, actividad, duracion_min, hora=None,
                            intensidad=None, notas=None):
    """Registrar sesión de entrenamiento.
    actividad: gym, correr, padel, caminar, etc.
    intensidad: 1-5 (opcional)
    """
    desc = f'Entrenamiento: {actividad}'
    if intensidad:
        desc += f' (intensidad {intensidad}/5)'
    return add_evento(fecha, 'salud', desc, subtipo='entrenamiento', hora=hora,
                      persona_id=12, fuente='sistema', duracion_min=duracion_min,
                      energia=intensidad, notas=notas)


def get_entrenamientos(fecha_desde=None, fecha_hasta=None):
    """Listar entrenamientos en un período."""
    conn = get_connection()
    c = conn.cursor()
    if fecha_desde is None:
        from datetime import timedelta
        fecha_desde = (date.today() - timedelta(days=30)).isoformat()
    if fecha_hasta is None:
        fecha_hasta = date.today().isoformat()
    c.execute('''SELECT fecha, hora, descripcion, duracion_min, energia, notas
                 FROM eventos
                 WHERE tipo = 'salud' AND subtipo = 'entrenamiento'
                 AND fecha BETWEEN ? AND ?
                 ORDER BY fecha ASC''',
              (fecha_desde, fecha_hasta))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    total_min = sum(r['duracion_min'] or 0 for r in rows)
    print(f"ENTRENAMIENTOS | {fecha_desde} a {fecha_hasta}")
    print(f"{'='*50}")
    print(f"Total: {len(rows)} sesiones, {round(total_min/60,1)}hs")
    for r in rows:
        dur = r['duracion_min'] or 0
        energia = f" [{r['energia']}/5]" if r['energia'] else ""
        print(f"  {r['fecha']} {r['hora'] or '':5s}  {dur:3d}min{energia}  {r['descripcion']}")
    print(f"{'='*50}")
    return rows


def get_horas_por_dia(fecha_desde=None, fecha_hasta=None):
    """Horas trabajadas por día, desglosadas por tipo (laboral/personal/etc).
    Retorna dict: {fecha: {tipo: minutos_total, ...}, ...}
    """
    conn = get_connection()
    c = conn.cursor()
    if fecha_desde is None:
        fecha_desde = date.today().isoformat()
    if fecha_hasta is None:
        fecha_hasta = date.today().isoformat()
    c.execute('''SELECT fecha, tipo, SUM(duracion_min) as total_min, COUNT(*) as sesiones
                 FROM eventos
                 WHERE fecha BETWEEN ? AND ?
                 AND duracion_min IS NOT NULL AND duracion_min > 0
                 GROUP BY fecha, tipo
                 ORDER BY fecha ASC, tipo ASC''',
              (fecha_desde, fecha_hasta))
    rows = c.fetchall()
    conn.close()

    resultado = {}
    for r in rows:
        r = dict(r)
        fecha = r['fecha']
        if fecha not in resultado:
            resultado[fecha] = {}
        resultado[fecha][r['tipo']] = {
            'minutos': r['total_min'],
            'horas': round(r['total_min'] / 60, 1),
            'sesiones': r['sesiones']
        }
    return resultado


def get_horas_resumen(fecha_desde=None, fecha_hasta=None):
    """Resumen de horas: total por tipo + por proyecto + por día.
    Ideal para saber cuánto trabajó Hernán en SBD vs personal.
    """
    conn = get_connection()
    c = conn.cursor()
    if fecha_desde is None:
        from datetime import timedelta
        fecha_desde = (date.today() - timedelta(days=7)).isoformat()
    if fecha_hasta is None:
        fecha_hasta = date.today().isoformat()

    # Total por tipo
    c.execute('''SELECT tipo, SUM(duracion_min) as total_min, COUNT(*) as sesiones
                 FROM eventos
                 WHERE fecha BETWEEN ? AND ?
                 AND duracion_min IS NOT NULL AND duracion_min > 0
                 GROUP BY tipo ORDER BY total_min DESC''',
              (fecha_desde, fecha_hasta))
    por_tipo = [dict(r) for r in c.fetchall()]

    # Total por proyecto
    c.execute('''SELECT p.nombre as proyecto, e.tipo, SUM(e.duracion_min) as total_min,
                 COUNT(*) as sesiones
                 FROM eventos e
                 LEFT JOIN proyectos p ON e.proyecto_id = p.id
                 WHERE e.fecha BETWEEN ? AND ?
                 AND e.duracion_min IS NOT NULL AND e.duracion_min > 0
                 GROUP BY p.nombre, e.tipo ORDER BY total_min DESC''',
              (fecha_desde, fecha_hasta))
    por_proyecto = [dict(r) for r in c.fetchall()]

    # Por día
    c.execute('''SELECT fecha, SUM(duracion_min) as total_min,
                 SUM(CASE WHEN tipo = 'laboral' THEN duracion_min ELSE 0 END) as laboral_min,
                 SUM(CASE WHEN tipo = 'personal' THEN duracion_min ELSE 0 END) as personal_min,
                 COUNT(*) as sesiones
                 FROM eventos
                 WHERE fecha BETWEEN ? AND ?
                 AND duracion_min IS NOT NULL AND duracion_min > 0
                 GROUP BY fecha ORDER BY fecha ASC''',
              (fecha_desde, fecha_hasta))
    por_dia = [dict(r) for r in c.fetchall()]

    conn.close()

    total_min = sum(t['total_min'] for t in por_tipo)
    return {
        'periodo': f'{fecha_desde} a {fecha_hasta}',
        'total_horas': round(total_min / 60, 1),
        'total_minutos': total_min,
        'por_tipo': por_tipo,
        'por_proyecto': por_proyecto,
        'por_dia': por_dia
    }


def imprimir_horas(fecha_desde=None, fecha_hasta=None):
    """Print bonito del resumen de horas. Para usar desde Claude Code."""
    res = get_horas_resumen(fecha_desde, fecha_hasta)
    print(f"{'='*50}")
    print(f"HORAS TRABAJADAS | {res['periodo']}")
    print(f"{'='*50}")
    print(f"Total: {res['total_horas']}hs ({res['total_minutos']} min)")
    print()

    if res['por_tipo']:
        print("POR TIPO:")
        for t in res['por_tipo']:
            hs = round(t['total_min'] / 60, 1)
            print(f"  {t['tipo']:12s} {hs:5.1f}hs  ({t['sesiones']} sesiones)")

    if res['por_proyecto']:
        print("\nPOR PROYECTO:")
        for p in res['por_proyecto']:
            hs = round(p['total_min'] / 60, 1)
            nombre = p['proyecto'] or '(sin proyecto)'
            print(f"  {nombre:35s} {hs:5.1f}hs  [{p['tipo']}]")

    if res['por_dia']:
        print("\nPOR DÍA:")
        for d in res['por_dia']:
            total = round(d['total_min'] / 60, 1)
            lab = round(d['laboral_min'] / 60, 1)
            per = round(d['personal_min'] / 60, 1)
            print(f"  {d['fecha']}  Total:{total:4.1f}hs  SBD:{lab:4.1f}hs  Personal:{per:4.1f}hs  ({d['sesiones']} sesiones)")

    print(f"{'='*50}")


# === NUTRICIÓN ===

PLAN_OPCIONES = {
    'desayuno': [
        'Omelette proteico (4 huevos + espinaca/tomate + galletas arroz + queso)',
        'Pancake proteico (avena + huevo + whey + banana)',
        'Tostada con palta y huevo (3 huevos + palta + tomate)',
        'Yogur con granola (yogur desc + granola Integra + fruta)',
        'Wrap salado (rapiditas + pollo + palta + vegetales)',
        'Chia y avena pudding (chia + avena + whey + fruta)',
    ],
    'almuerzo': [
        'Plato plan: proteina 270g + vegetales 2 colores + legumbres + grasa buena',
    ],
    'merienda': [
        'Omelette proteico', 'Pancake proteico', 'Tostada con palta y huevo',
        'Yogur con granola', 'Wrap salado', 'Chia y avena pudding',
    ],
    'cena': [
        'Plato plan: proteina 270g + vegetales 2 colores + legumbres + grasa buena',
    ],
    'snack': [
        'Banana + whey con agua/leche',
        'Barrita proteica + banana',
        'Sandwich jamon y queso',
        'Yogur proteico + 40g frutos secos',
    ],
}

SUPLEMENTOS_PLAN = ['whey', 'creatina', 'magnesio']


def registrar_comida(fecha, comida, descripcion, del_plan=1, proteina=0, vegetales=0,
                     agua_litros=None, suplementos=None, notas=None):
    """Registrar una comida. comida: desayuno, almuerzo, merienda, cena, snack."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO nutricion (fecha, comida, descripcion, del_plan, proteina, vegetales,
                 agua_litros, suplementos, notas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (fecha, comida.lower(), descripcion, del_plan, proteina, vegetales,
               agua_litros, suplementos, notas))
    nid = c.lastrowid
    conn.commit()
    conn.close()
    return nid


def get_nutricion_dia(fecha=None):
    """Ver todas las comidas de un día."""
    if fecha is None:
        fecha = date.today().isoformat()
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM nutricion WHERE fecha = ? ORDER BY id', (fecha,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print(f"Sin registros de comida para {fecha}")
        return []

    comidas_orden = ['desayuno', 'almuerzo', 'merienda', 'cena', 'snack']
    print(f"\n{'='*55}")
    print(f"  NUTRICION {fecha}")
    print(f"{'='*55}")

    suplementos_dia = set()
    proteina_ok = 0
    vegetales_ok = 0
    fuera_plan = 0

    for r in rows:
        plan_tag = 'OK' if r['del_plan'] else 'FUERA'
        prot_tag = 'P' if r['proteina'] else '-'
        veg_tag = 'V' if r['vegetales'] else '-'
        print(f"  {r['comida'].upper():10s} | [{plan_tag:5s}] [{prot_tag}][{veg_tag}] {r['descripcion']}")
        if r['suplementos']:
            for s in r['suplementos'].split(','):
                suplementos_dia.add(s.strip().lower())
        if r['proteina']:
            proteina_ok += 1
        if r['vegetales']:
            vegetales_ok += 1
        if not r['del_plan']:
            fuera_plan += 1
        if r['notas']:
            print(f"{'':13s}   Nota: {r['notas']}")

    # Resumen del día
    total = len(rows)
    agua = None
    for r in rows:
        if r['agua_litros']:
            agua = r['agua_litros']

    print(f"\n  --- Resumen ---")
    print(f"  Comidas: {total} | Del plan: {total - fuera_plan}/{total} | Fuera: {fuera_plan}")
    print(f"  Proteina OK: {proteina_ok}/{total} | Vegetales OK: {vegetales_ok}/{total}")

    # Suplementos check
    faltantes = [s for s in SUPLEMENTOS_PLAN if s not in suplementos_dia]
    tomados = [s for s in SUPLEMENTOS_PLAN if s in suplementos_dia]
    if tomados:
        print(f"  Suplementos: {', '.join(tomados)}")
    if faltantes:
        print(f"  Faltan: {', '.join(faltantes)}")

    if agua:
        ok = 'OK' if agua >= 2.0 else 'BAJO'
        print(f"  Agua: {agua:.1f}L [{ok}] (meta: 2-3L)")

    print(f"{'='*55}\n")
    return [dict(r) for r in rows]


def get_nutricion_semana(fecha_desde=None):
    """Resumen nutricional semanal."""
    if fecha_desde is None:
        from datetime import timedelta
        fecha_desde = (date.today() - timedelta(days=6)).isoformat()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT fecha, COUNT(*) as comidas,
                 SUM(del_plan) as del_plan, SUM(proteina) as con_proteina,
                 SUM(vegetales) as con_vegetales, MAX(agua_litros) as agua,
                 GROUP_CONCAT(DISTINCT suplementos) as supls
                 FROM nutricion WHERE fecha >= ?
                 GROUP BY fecha ORDER BY fecha''', (fecha_desde,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print(f"Sin registros desde {fecha_desde}")
        return []

    print(f"\n{'='*65}")
    print(f"  NUTRICION SEMANAL desde {fecha_desde}")
    print(f"{'='*65}")
    print(f"  {'FECHA':12s} {'COMIDAS':8s} {'PLAN':6s} {'PROT':6s} {'VEG':6s} {'AGUA':6s} {'SUPLS'}")
    print(f"  {'-'*60}")

    total_dias = len(rows)
    total_plan = 0
    total_comidas = 0

    for r in rows:
        plan_pct = f"{r['del_plan'] or 0}/{r['comidas']}"
        prot_pct = f"{r['con_proteina'] or 0}/{r['comidas']}"
        veg_pct = f"{r['con_vegetales'] or 0}/{r['comidas']}"
        agua_str = f"{r['agua']:.1f}L" if r['agua'] else '-'
        supls = r['supls'] or '-'
        # Limpiar duplicados en suplementos
        if supls != '-':
            all_s = set()
            for part in supls.split(','):
                all_s.add(part.strip().lower())
            supls = ', '.join(sorted(all_s))
        print(f"  {r['fecha']:12s} {r['comidas']:8d} {plan_pct:6s} {prot_pct:6s} {veg_pct:6s} {agua_str:6s} {supls}")
        total_plan += (r['del_plan'] or 0)
        total_comidas += r['comidas']

    adherencia = (total_plan / total_comidas * 100) if total_comidas > 0 else 0
    print(f"\n  Adherencia al plan: {adherencia:.0f}% ({total_plan}/{total_comidas} comidas)")
    print(f"  Dias registrados: {total_dias}")
    print(f"{'='*65}\n")

    return [dict(r) for r in rows]


def imprimir_plan():
    """Mostrar el plan nutricional de referencia."""
    print("\n" + "="*55)
    print("  PLAN NUTRICIONAL - Lic. Julieta B. Iglesias")
    print("  artro nutricion - Feb 2026")
    print("="*55)

    for comida, opciones in PLAN_OPCIONES.items():
        print(f"\n  {comida.upper()}:")
        for i, op in enumerate(opciones, 1):
            print(f"    {i}. {op}")

    print(f"\n  SUPLEMENTOS: whey (en comidas), creatina 5g post-comida, magnesio antes de dormir")
    print(f"  EJERCICIO: gym 2-3x/sem, cardio 3-4x/sem, 10k pasos/dia")
    print(f"  AGUA: 2-3 litros/dia")
    print(f"  ORDEN: vegetales -> proteina -> hidratos. Fruta de postre, nunca antes.")
    print(f"  POST-COMIDA: 10 min caminata (baja glucemia)")
    print(f"{'='*55}\n")


# === METAS ===

def add_meta(descripcion, area, proyecto_id=None, prioridad='media',
             fecha_objetivo=None, horas_semana_meta=None, indicador='horas',
             notas=None):
    """Registrar una meta/intención declarada."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO metas (descripcion, area, proyecto_id, prioridad,
                 fecha_objetivo, horas_semana_meta, indicador, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (descripcion, area, proyecto_id, prioridad,
               fecha_objetivo, horas_semana_meta, indicador, notas))
    mid = c.lastrowid
    conn.commit()
    conn.close()
    return mid


def get_metas(solo_activas=True):
    """Listar metas. Incluye nombre del proyecto si tiene proyecto_id."""
    conn = get_connection()
    c = conn.cursor()
    query = '''SELECT m.*, p.nombre as proyecto_nombre
               FROM metas m
               LEFT JOIN proyectos p ON m.proyecto_id = p.id'''
    if solo_activas:
        query += " WHERE m.estado = 'activa'"
    query += " ORDER BY CASE m.prioridad WHEN 'alta' THEN 1 WHEN 'media' THEN 2 ELSE 3 END"
    c.execute(query)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def update_meta(meta_id, **kwargs):
    """Actualizar campos de una meta. Acepta cualquier campo válido."""
    campos_validos = {'descripcion', 'area', 'proyecto_id', 'prioridad',
                      'fecha_objetivo', 'horas_semana_meta', 'indicador',
                      'estado', 'notas'}
    updates = {k: v for k, v in kwargs.items() if k in campos_validos}
    if not updates:
        return False
    conn = get_connection()
    c = conn.cursor()
    set_clause = ', '.join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [meta_id]
    c.execute(f"UPDATE metas SET {set_clause} WHERE id = ?", values)
    conn.commit()
    affected = c.rowcount
    conn.close()
    return affected > 0


# === SISTEMA MULTI-AGENTE ===

def add_agente(codigo, nombre, descripcion=None, prompt_file=None,
               capacidades=None, triggers=None):
    """Registrar un agente en el sistema."""
    import json as _json
    conn = get_connection()
    c = conn.cursor()
    if isinstance(capacidades, list):
        capacidades = _json.dumps(capacidades, ensure_ascii=False)
    if isinstance(triggers, list):
        triggers = _json.dumps(triggers, ensure_ascii=False)
    c.execute('''INSERT OR IGNORE INTO agentes (codigo, nombre, descripcion,
                 prompt_file, capacidades, triggers)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (codigo, nombre, descripcion, prompt_file, capacidades, triggers))
    aid = c.lastrowid
    conn.commit()
    conn.close()
    return aid


def get_agentes(solo_activos=True):
    """Listar agentes registrados."""
    conn = get_connection()
    c = conn.cursor()
    if solo_activos:
        c.execute("SELECT * FROM agentes WHERE estado = 'activo' ORDER BY id")
    else:
        c.execute("SELECT * FROM agentes ORDER BY id")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_agente(codigo):
    """Obtener un agente por su código."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM agentes WHERE codigo = ?", (codigo,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def registrar_consulta_agente(agente_codigo, tipo, contexto, resultado,
                               confianza=0.8, evento_id=None):
    """Registrar una intervención/consulta de un agente."""
    conn = get_connection()
    c = conn.cursor()
    # Buscar agente_id por código
    c.execute("SELECT id FROM agentes WHERE codigo = ?", (agente_codigo,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    agente_id = row['id']
    hora = datetime.now().strftime('%H:%M')
    fecha = date.today().isoformat()
    c.execute('''INSERT INTO consultas_agente (agente_id, fecha, hora, tipo,
                 contexto, resultado, confianza, evento_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (agente_id, fecha, hora, tipo, contexto, resultado, confianza, evento_id))
    cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid


def get_consultas_agente(agente_codigo, fecha_desde=None, limit=20):
    """Obtener últimas consultas de un agente."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM agentes WHERE codigo = ?", (agente_codigo,))
    row = c.fetchone()
    if not row:
        conn.close()
        return []
    agente_id = row['id']
    if fecha_desde:
        c.execute('''SELECT * FROM consultas_agente
                     WHERE agente_id = ? AND fecha >= ?
                     ORDER BY fecha DESC, hora DESC LIMIT ?''',
                  (agente_id, fecha_desde, limit))
    else:
        c.execute('''SELECT * FROM consultas_agente
                     WHERE agente_id = ?
                     ORDER BY fecha DESC, hora DESC LIMIT ?''',
                  (agente_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_resumen_agentes():
    """Resumen de actividad de todos los agentes: consultas, aceptación, última actividad."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT a.codigo, a.nombre, a.estado,
                 COUNT(ca.id) as total_consultas,
                 SUM(CASE WHEN ca.aceptado = 1 THEN 1 ELSE 0 END) as aceptadas,
                 SUM(CASE WHEN ca.aceptado = 0 THEN 1 ELSE 0 END) as rechazadas,
                 MAX(ca.fecha || ' ' || COALESCE(ca.hora, '')) as ultima_actividad
                 FROM agentes a
                 LEFT JOIN consultas_agente ca ON a.id = ca.agente_id
                 WHERE a.estado = 'activo'
                 GROUP BY a.id
                 ORDER BY a.id''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# === BIENESTAR DIARIO ===

def add_bienestar(fecha, humor=None, energia=None, estres=None,
                  horas_sueno=None, calidad_sueno=None, atencion_familia=None,
                  ejercicio_min=0, intensidad_laboral=None, intensidad_personal=None,
                  interlocutores=None, tareas_contadas=None,
                  conflictos=None, logros=None, frustraciones=None, notas=None):
    """Registrar bienestar diario. Escalas: humor/energia/estres/intensidad 1-10, sueño/familia 1-5."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO bienestar (fecha, humor, energia, estres, horas_sueno,
                 calidad_sueno, atencion_familia, ejercicio_min,
                 intensidad_laboral, intensidad_personal,
                 interlocutores, tareas_contadas,
                 conflictos, logros, frustraciones, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (fecha, humor, energia, estres, horas_sueno, calidad_sueno,
               atencion_familia, ejercicio_min, intensidad_laboral, intensidad_personal,
               interlocutores, tareas_contadas, conflictos, logros, frustraciones, notas))
    bid = c.lastrowid
    conn.commit()
    conn.close()
    return bid


def get_bienestar_periodo(fecha_desde=None, fecha_hasta=None):
    """Obtener registros de bienestar en un período."""
    conn = get_connection()
    c = conn.cursor()
    if fecha_desde is None:
        from datetime import timedelta
        fecha_desde = (date.today() - timedelta(days=30)).isoformat()
    if fecha_hasta is None:
        fecha_hasta = date.today().isoformat()
    c.execute('''SELECT * FROM bienestar
                 WHERE fecha BETWEEN ? AND ?
                 ORDER BY fecha ASC''', (fecha_desde, fecha_hasta))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def reporte_bienestar(fecha_desde=None, dias=7):
    """Reporte de bienestar con tendencias y correlaciones."""
    if fecha_desde is None:
        from datetime import timedelta
        fecha_desde = (date.today() - timedelta(days=dias)).isoformat()

    registros = get_bienestar_periodo(fecha_desde)

    if not registros:
        print("Sin registros de bienestar en el período.")
        print("Usar: add_bienestar(fecha, humor=X, energia=X, ...)")
        return []

    print(f"\n{'='*65}")
    print(f"  BIENESTAR | {fecha_desde} a hoy ({len(registros)} días)")
    print(f"{'='*65}")
    print(f"  {'FECHA':12s} {'HUM':4s} {'ENE':4s} {'EST':4s} {'SUE':5s} {'FAM':4s} {'I.LAB':5s} {'I.PER':5s} {'INTER':5s}")
    print(f"  {'-'*60}")

    sum_humor = sum_energia = sum_estres = sum_sueno = sum_familia = 0
    sum_ilab = sum_iper = count = 0

    for r in registros:
        h = f"{r['humor']}" if r['humor'] else '-'
        e = f"{r['energia']}" if r['energia'] else '-'
        s = f"{r['estres']}" if r['estres'] else '-'
        sue = f"{r['horas_sueno']:.1f}" if r['horas_sueno'] else '-'
        fam = f"{r['atencion_familia']}" if r['atencion_familia'] else '-'
        il = f"{r['intensidad_laboral']}" if r['intensidad_laboral'] else '-'
        ip = f"{r['intensidad_personal']}" if r['intensidad_personal'] else '-'
        inter = f"{r['interlocutores']}" if r['interlocutores'] else '-'

        print(f"  {r['fecha']:12s} {h:4s} {e:4s} {s:4s} {sue:5s} {fam:4s} {il:5s} {ip:5s} {inter:5s}")

        if r['conflictos']:
            print(f"{'':14s} Conflictos: {r['conflictos']}")
        if r['frustraciones']:
            print(f"{'':14s} Frustraciones: {r['frustraciones']}")
        if r['logros']:
            print(f"{'':14s} Logros: {r['logros']}")

        # Acumular para promedios
        if r['humor']: sum_humor += r['humor']; count += 1
        if r['energia']: sum_energia += r['energia']
        if r['estres']: sum_estres += r['estres']
        if r['horas_sueno']: sum_sueno += r['horas_sueno']
        if r['atencion_familia']: sum_familia += r['atencion_familia']
        if r['intensidad_laboral']: sum_ilab += r['intensidad_laboral']
        if r['intensidad_personal']: sum_iper += r['intensidad_personal']

    if count > 0:
        print(f"\n  --- Promedios ({count} días) ---")
        print(f"  Humor: {sum_humor/count:.1f}/10 | Energía: {sum_energia/count:.1f}/10 | Estrés: {sum_estres/count:.1f}/10")
        if sum_sueno > 0:
            print(f"  Sueño: {sum_sueno/count:.1f}hs | Familia: {sum_familia/count:.1f}/5")
        if sum_ilab > 0:
            print(f"  Intensidad laboral: {sum_ilab/count:.1f}/10 | Personal: {sum_iper/count:.1f}/10")

        # Detectar patrones
        print(f"\n  --- Patrones ---")
        if sum_ilab/count >= 8 and sum_familia/count <= 2:
            print(f"  !! Alta carga laboral + baja atención familiar")
        if sum_estres/count >= 7 and sum_sueno/count < 7:
            print(f"  !! Alto estrés + poco sueño")
        if sum_humor/count <= 4:
            print(f"  !! Humor bajo sostenido — revisar causas")

    print(f"{'='*65}\n")
    return registros


# === MIGRACIÓN DESDE SEGUIMIENTO.MD ===

def migrar_datos_iniciales():
    """Migrar datos existentes de memoria ARGOS a la DB."""
    init_db()

    # --- PERSONAS ---
    richard = add_persona('Richard Serrats', 'jefe', 'Software By Design S.A.',
                          notas='Jefe directo de Hernán',
                          perfil='Controla con dinero. Demuestra poder. Recortó sueldo como castigo. Pide informes como gesto de autoridad.')
    marcelo = add_persona('Marcelo Hamra', 'socio/hermano', 'Software By Design S.A.',
                          notas='Presidente SBD, hermano mayor, Ing. Sistemas UTN')
    marino = add_persona('Marino', 'colega', 'Software By Design S.A.')
    leo = add_persona('Leo Martínez', 'subcontratista', 'DNET',
                      notas='Subcontratista cableado Posadas')
    ricardo_torres = add_persona('Ricardo Torres', 'cliente', None,
                                 notas='Cliente Posadas, otros proyectos. Hay que cuidarlo.')
    natalia = add_persona('Beatriz Natalia Indibo', 'esposa', None,
                          contacto='DNI 23.766.561', notas='Nac. 09/02/1974')
    uriel = add_persona('Uriel Aharon Hamra', 'hijo', None,
                        notas='Nac. 26/02/2007. Nombre hebreo Aharon por su abuelo materno.')
    sol = add_persona('Sol Chiara Hamra', 'hija', None,
                      notas='Nac. 11/04/2008. Nombre hebreo Mazal Shoshana.')
    matias = add_persona('Matías Iacov Hamra', 'hijo', None,
                         notas='Nac. 03/10/2011. Nombre hebreo Iacov por su abuelo paterno Raúl Jacobo.')
    margarita = add_persona('Margarita', 'suegra', None,
                            notas='Nombre hebreo Shoshana. Estudios médicos del pie.')
    esteban = add_persona('Esteban Marcucci', 'amigo/socio', 'AiControl',
                          notas='Amigo íntimo, mismo cumpleaños 31/07. Socio en instalaciones y AiControl.')
    hernan = add_persona('Hernán Hamra', 'yo', 'Software By Design S.A.',
                         contacto='hamrahernan@gmail.com / +5411-5317-1213')

    # --- PROYECTOS ---
    posadas = add_proyecto('Hospital Posadas - Cableado', 'laboral', 'SBD',
                           'activo', 'Cableado estructurado Hospital Posadas', '2025-12-01')
    sbase_cable = add_proyecto('SBASE LP 410/26 - Cableado', 'laboral', 'SBD',
                               'completado', 'Licitación privada 410/26. 384 folios, 4 carpetas.', '2026-01-01')
    sbase_cctv = add_proyecto('SBASE - CCTV', 'laboral', 'SBD',
                              'activo', 'Nueva licitación CCTV. En evaluación.', '2026-02-17')
    aicontrol = add_proyecto('AiControl Seguridad', 'personal', 'emprendimiento',
                             'activo', 'Seguridad electrónica + visión por computadora')
    agente_hosp = add_proyecto('agente_hospital', 'personal', 'desarrollo',
                               'pausado', 'Bot hospitalario Grupo Pediátrico (Groq+ChromaDB+Rasa)')
    busqueda = add_proyecto('Búsqueda laboral', 'personal', 'carrera',
                            'pausado', 'CV, LinkedIn, postulaciones')
    argos_prod = add_proyecto('ARGOS - Producto', 'personal', 'desarrollo',
                              'activo', 'Convertir ARGOS en producto vendible')

    # --- FECHAS IMPORTANTES ---
    add_fecha_importante(natalia, 'cumpleanos', '02-09', 'Cumpleaños Natalia')
    add_fecha_importante(uriel, 'cumpleanos', '02-26', 'Cumpleaños Uriel')
    add_fecha_importante(sol, 'cumpleanos', '04-11', 'Cumpleaños Sol Chiara')
    add_fecha_importante(hernan, 'cumpleanos', '07-31', 'Cumpleaños Hernán')
    add_fecha_importante(matias, 'cumpleanos', '10-03', 'Cumpleaños Matías')
    add_fecha_importante(esteban, 'cumpleanos', '07-31', 'Cumpleaños Esteban (mismo que Hernán!)')

    # Fallecimientos
    add_fecha_importante(None, 'fallecimiento', '2012-06-12',
                         '† Raúl Jacobo Hamra (padre). Ese día Hernán corrió una media maratón.')
    add_fecha_importante(None, 'fallecimiento', '2024-03-15',
                         '† Fortuna Jabbaz (madre, Mazal). Psicóloga pionera. 5 años postrada.')
    add_fecha_importante(None, 'fallecimiento', '2025-07-15',
                         '† Aharon (suegro). Uriel lleva su nombre hebreo.')

    # --- EVENTOS (registro histórico) ---
    # SBASE
    add_evento('2026-02-18', 'laboral', 'Presentación licitación SBASE 410/26 - 384 folios',
               'hito', proyecto_id=sbase_cable, resultado='presentado')
    # Posadas
    add_evento('2026-02-18', 'laboral', 'Envío informe gestión enero a Richard (68 items)',
               'email', proyecto_id=posadas, persona_id=richard, fuente='email', resultado='esperando')
    add_evento('2026-02-18', 'laboral', 'Email formal a Richard con informe adjunto + pedido USD 500',
               'email', proyecto_id=posadas, persona_id=richard, fuente='email', resultado='enviado')
    add_evento('2026-02-18', 'personal', 'WhatsApp a Richard - pedido USD 500 completos enero',
               'whatsapp', proyecto_id=posadas, persona_id=richard, fuente='whatsapp', resultado='pendiente')
    # ARGOS
    add_evento('2026-02-18', 'personal', 'Creación de DB SQLite para tracking ARGOS',
               'hito', proyecto_id=argos_prod, fuente='sistema')

    # --- SEGUIMIENTO ---
    add_seguimiento('Confirmar pago USD 500 enero - si no responde, reenviar recordatorio',
                    '2026-02-20', proyecto_id=posadas, persona_id=richard, prioridad='critica')
    add_seguimiento('Confirmar entrega materiales Posadas (ménsulas/articuladas)',
                    '2026-02-19', proyecto_id=posadas, persona_id=marino, prioridad='alta')
    add_seguimiento('Definir si vamos con SBASE CCTV (visita técnica 19/02)',
                    '2026-02-21', proyecto_id=sbase_cctv, persona_id=marcelo, prioridad='alta')
    add_seguimiento('Resultado apertura sobres SBASE cableado',
                    '2026-03-01', proyecto_id=sbase_cable, prioridad='media')
    add_seguimiento('Seguimiento cotización AiControl enviada a Richard',
                    '2026-02-25', proyecto_id=aicontrol, persona_id=richard, prioridad='media')
    add_seguimiento('Unificar CV - relato potente único',
                    '2026-03-15', proyecto_id=busqueda, prioridad='media')

    # --- SALUD ---
    add_salud(margarita, 'estudio', descripcion='Estudios médicos del pie. Carpeta MARAGA PIE en OneDrive.',
              especialidad='Traumatología/Podología')

    print("Migración completada.")
    print(f"Personas: {hernan}")
    print(f"Proyectos: {argos_prod}")

    return {
        'personas': {'richard': richard, 'marcelo': marcelo, 'marino': marino,
                     'leo': leo, 'ricardo_torres': ricardo_torres, 'natalia': natalia,
                     'uriel': uriel, 'sol': sol, 'matias': matias, 'margarita': margarita,
                     'esteban': esteban, 'hernan': hernan},
        'proyectos': {'posadas': posadas, 'sbase_cable': sbase_cable, 'sbase_cctv': sbase_cctv,
                      'aicontrol': aicontrol, 'agente_hosp': agente_hosp, 'busqueda': busqueda,
                      'argos_prod': argos_prod}
    }


if __name__ == '__main__':
    ids = migrar_datos_iniciales()
    print("\n=== IDs generados ===")
    for categoria, items in ids.items():
        print(f"\n{categoria}:")
        for nombre, id_val in items.items():
            print(f"  {nombre}: {id_val}")

    print("\n=== Próximas fechas (30 días) ===")
    for fecha_info, dias in get_proximas_fechas():
        print(f"  En {dias} días: {fecha_info['descripcion']} ({fecha_info['persona']})")

    print("\n=== Pendientes ===")
    for p in get_pendientes():
        print(f"  [{dict(p)['prioridad']}] {dict(p)['accion']} (límite: {dict(p)['fecha_limite']})")
