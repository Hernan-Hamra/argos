"""
ARGOS Tracker - Sistema de seguimiento personal y laboral
Base de datos SQLite para trackear: proyectos, eventos, personas,
seguimiento, fechas importantes, salud y métricas.
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


def init_db():
    """Crear todas las tablas si no existen."""
    conn = get_connection()
    c = conn.cursor()

    # --- PROYECTOS ---
    c.execute('''CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,          -- laboral, personal, salud, formacion
        categoria TEXT,              -- SBD, AiControl, familia, etc.
        estado TEXT DEFAULT 'activo', -- activo, pausado, completado, cancelado
        fecha_inicio TEXT,
        fecha_fin TEXT,
        descripcion TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # --- PERSONAS ---
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        relacion TEXT,               -- jefe, cliente, proveedor, familia, amigo, colega
        empresa TEXT,
        contacto TEXT,               -- tel, email
        notas TEXT,
        perfil_comportamiento TEXT,  -- patrones observados (ej: "controla con dinero")
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # --- EVENTOS (el corazón del tracking) ---
    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT,
        tipo TEXT NOT NULL,          -- laboral, personal, salud, familia, formacion, admin
        subtipo TEXT,                -- reunion, llamada, email, whatsapp, archivo, decision, hito
        proyecto_id INTEGER,
        persona_id INTEGER,
        descripcion TEXT NOT NULL,
        fuente TEXT,                 -- whatsapp, email, archivo, reunion, llamada, sistema
        resultado TEXT,              -- ok, pendiente, fallido, esperando
        duracion_min INTEGER,        -- duración estimada en minutos
        energia INTEGER,             -- 1-5 nivel de energía/esfuerzo
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    # --- SEGUIMIENTO (pendientes con deadline) ---
    c.execute('''CREATE TABLE IF NOT EXISTS seguimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        proyecto_id INTEGER,
        persona_id INTEGER,
        accion TEXT NOT NULL,        -- qué hay que hacer
        fecha_limite TEXT,           -- deadline
        estado TEXT DEFAULT 'pendiente', -- pendiente, en_curso, completado, vencido
        prioridad TEXT DEFAULT 'media',  -- critica, alta, media, baja
        recordatorio TEXT,           -- cuándo recordar
        resultado TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        completed_at TEXT,
        FOREIGN KEY (evento_id) REFERENCES eventos(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    # --- FECHAS IMPORTANTES ---
    c.execute('''CREATE TABLE IF NOT EXISTS fechas_importantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER,
        tipo TEXT NOT NULL,          -- cumpleanos, aniversario, fallecimiento, religioso
        fecha TEXT NOT NULL,         -- formato MM-DD o YYYY-MM-DD
        fecha_hebreo TEXT,           -- futuro: calendario hebreo
        descripcion TEXT,
        recurrente INTEGER DEFAULT 1, -- 1=anual, 0=una vez
        notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    # --- SALUD ---
    c.execute('''CREATE TABLE IF NOT EXISTS salud (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER,
        tipo TEXT NOT NULL,          -- turno, estudio, control, tratamiento, emergencia
        fecha TEXT,
        hora TEXT,
        profesional TEXT,
        lugar TEXT,
        especialidad TEXT,
        descripcion TEXT,
        estado TEXT DEFAULT 'pendiente', -- pendiente, realizado, cancelado, reprogramado
        resultado TEXT,
        proxima_cita TEXT,
        notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    # --- MÉTRICAS (snapshots periódicos) ---
    c.execute('''CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT NOT NULL,          -- diaria, semanal, mensual
        proyectos_activos INTEGER,
        eventos_dia INTEGER,
        eventos_semana INTEGER,
        horas_laboral REAL,
        horas_personal REAL,
        horas_salud REAL,
        horas_formacion REAL,
        balance_vida_trabajo REAL,   -- ratio personal/laboral (>1 = más personal)
        energia_promedio REAL,       -- promedio del campo energia en eventos
        pendientes_abiertos INTEGER,
        pendientes_vencidos INTEGER,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # --- TAGS (para categorización flexible) ---
    c.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        tag TEXT NOT NULL,
        FOREIGN KEY (evento_id) REFERENCES eventos(id)
    )''')

    # --- AGENDA (calendario hacia adelante) ---
    c.execute('''CREATE TABLE IF NOT EXISTS agenda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT,
        hora_fin TEXT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL,          -- turno, reunion, cita, compromiso, visita, deadline, personal
        proyecto_id INTEGER,
        persona_id INTEGER,
        lugar TEXT,
        descripcion TEXT,
        recurrente TEXT,             -- NULL=una vez, diario, semanal, mensual, anual
        recordatorio_dias INTEGER DEFAULT 1,  -- cuántos días antes avisar
        estado TEXT DEFAULT 'pendiente',      -- pendiente, confirmado, cancelado, realizado
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
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
