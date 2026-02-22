"""
ARGOS DB Manager - Gestión de bases de datos separadas

Arquitectura:
  DB SISTEMA (argos_sistema.db) — compartible entre usuarios
    - capacidades: catálogo dinámico herramienta + protocolo
    - patrones: tipo 'general' y 'perfil' (generalizados)
    - perfiles_tipo: definiciones de perfiles de usuario

  DB USUARIO (argos_usuario.db) — privada, encriptada por usuario
    - proyectos, personas, eventos, seguimiento, agenda
    - fechas_importantes, salud, nutricion, metricas, tags
    - patrones: tipo 'personal' (solo del usuario)

Principio: SE COMPARTE EL PROCESO (sistema), NUNCA LA DATA (usuario).
"""

import sqlite3
import os
from datetime import datetime, date

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Paths de las DBs
SISTEMA_DB = os.path.join(DATA_DIR, 'argos_sistema.db')
USUARIO_DB = os.path.join(DATA_DIR, 'argos_usuario.db')
# DB legacy (para migración)
LEGACY_DB = os.path.join(DATA_DIR, 'argos_tracker.db')


def _ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_sistema():
    """Conexión a la DB de sistema (catálogo, patrones generales)."""
    _ensure_dir()
    conn = sqlite3.connect(SISTEMA_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_usuario():
    """Conexión a la DB de usuario (datos privados)."""
    _ensure_dir()
    conn = sqlite3.connect(USUARIO_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_legacy():
    """Conexión a la DB legacy (solo para migración)."""
    if not os.path.exists(LEGACY_DB):
        return None
    conn = sqlite3.connect(LEGACY_DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# INIT — crear tablas en cada DB
# =========================================================

def init_sistema():
    """Crear tablas de la DB de sistema."""
    conn = get_sistema()
    c = conn.cursor()

    # --- CAPACIDADES (catálogo dinámico de herramienta + protocolo) ---
    c.execute('''CREATE TABLE IF NOT EXISTS capacidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        nombre_display TEXT NOT NULL,
        descripcion TEXT,
        herramienta TEXT,
        protocolo TEXT,
        categoria TEXT,
        version INTEGER DEFAULT 1,
        origen TEXT DEFAULT 'sistema',
        es_generalizable INTEGER DEFAULT 1,
        perfiles TEXT,
        keywords TEXT,
        veces_usada INTEGER DEFAULT 1,
        ultima_vez TEXT,
        estado TEXT DEFAULT 'activa',
        mejora_de INTEGER,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (mejora_de) REFERENCES capacidades(id)
    )''')

    # --- PATRONES GENERALES (compartibles) ---
    c.execute('''CREATE TABLE IF NOT EXISTS patrones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_deteccion TEXT NOT NULL,
        tipo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        evidencia TEXT,
        frecuencia INTEGER DEFAULT 1,
        confianza REAL DEFAULT 0.5,
        estado TEXT DEFAULT 'detectado',
        sugerencia TEXT,
        compartido INTEGER DEFAULT 0,
        anonimizado_en TEXT,
        ultimo_visto TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    conn.commit()
    conn.close()


def init_usuario():
    """Crear tablas de la DB de usuario."""
    conn = get_usuario()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        categoria TEXT,
        estado TEXT DEFAULT 'activo',
        fecha_inicio TEXT,
        fecha_fin TEXT,
        descripcion TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        relacion TEXT,
        empresa TEXT,
        contacto TEXT,
        notas TEXT,
        perfil_comportamiento TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT,
        tipo TEXT NOT NULL,
        subtipo TEXT,
        proyecto_id INTEGER,
        persona_id INTEGER,
        descripcion TEXT NOT NULL,
        fuente TEXT,
        resultado TEXT,
        duracion_min INTEGER,
        energia INTEGER,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS seguimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        proyecto_id INTEGER,
        persona_id INTEGER,
        accion TEXT NOT NULL,
        fecha_limite TEXT,
        estado TEXT DEFAULT 'pendiente',
        prioridad TEXT DEFAULT 'media',
        recordatorio TEXT,
        resultado TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        completed_at TEXT,
        FOREIGN KEY (evento_id) REFERENCES eventos(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS fechas_importantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER,
        tipo TEXT NOT NULL,
        fecha TEXT NOT NULL,
        fecha_hebreo TEXT,
        descripcion TEXT,
        recurrente INTEGER DEFAULT 1,
        notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS salud (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER,
        tipo TEXT NOT NULL,
        fecha TEXT,
        hora TEXT,
        profesional TEXT,
        lugar TEXT,
        especialidad TEXT,
        descripcion TEXT,
        estado TEXT DEFAULT 'pendiente',
        resultado TEXT,
        proxima_cita TEXT,
        notas TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT NOT NULL,
        proyectos_activos INTEGER,
        eventos_dia INTEGER,
        eventos_semana INTEGER,
        horas_laboral REAL,
        horas_personal REAL,
        horas_salud REAL,
        horas_formacion REAL,
        balance_vida_trabajo REAL,
        energia_promedio REAL,
        pendientes_abiertos INTEGER,
        pendientes_vencidos INTEGER,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        tag TEXT NOT NULL,
        FOREIGN KEY (evento_id) REFERENCES eventos(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS agenda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT,
        hora_fin TEXT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL,
        proyecto_id INTEGER,
        persona_id INTEGER,
        lugar TEXT,
        descripcion TEXT,
        recurrente TEXT,
        recordatorio_dias INTEGER DEFAULT 1,
        estado TEXT DEFAULT 'pendiente',
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
        FOREIGN KEY (persona_id) REFERENCES personas(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS nutricion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        comida TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        del_plan INTEGER DEFAULT 1,
        proteina INTEGER DEFAULT 0,
        vegetales INTEGER DEFAULT 0,
        agua_litros REAL,
        suplementos TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Patrones PERSONALES del usuario (no compartibles)
    c.execute('''CREATE TABLE IF NOT EXISTS patrones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_deteccion TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'personal',
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        evidencia TEXT,
        frecuencia INTEGER DEFAULT 1,
        confianza REAL DEFAULT 0.5,
        estado TEXT DEFAULT 'detectado',
        sugerencia TEXT,
        ultimo_visto TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    )''')

    conn.commit()
    conn.close()


def init_all():
    """Inicializar ambas DBs."""
    init_sistema()
    init_usuario()
    print(f"DB sistema: {os.path.abspath(SISTEMA_DB)}")
    print(f"DB usuario: {os.path.abspath(USUARIO_DB)}")


# =========================================================
# MIGRACIÓN desde DB legacy
# =========================================================

def migrar_desde_legacy():
    """Migrar datos de argos_tracker.db a las dos DBs nuevas.
    Idempotente: no duplica si ya hay datos.
    """
    legacy = get_legacy()
    if legacy is None:
        print("No se encontró DB legacy. Nada que migrar.")
        return

    init_all()

    # --- Migrar a SISTEMA ---
    sistema = get_sistema()
    sc = sistema.cursor()

    # Capacidades
    sc.execute("SELECT COUNT(*) FROM capacidades")
    if sc.fetchone()[0] == 0:
        lc = legacy.cursor()
        lc.execute("SELECT * FROM capacidades")
        rows = lc.fetchall()
        for r in rows:
            r = dict(r)
            try:
                sc.execute('''INSERT INTO capacidades (nombre, nombre_display, descripcion,
                    herramienta, protocolo, categoria, version, origen, es_generalizable,
                    perfiles, keywords, veces_usada, ultima_vez, estado, mejora_de, notas,
                    created_at, updated_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (r['nombre'], r['nombre_display'], r.get('descripcion'),
                     r.get('herramienta'), r.get('protocolo'), r.get('categoria'),
                     r.get('version', 1), r.get('origen', 'sistema'),
                     r.get('es_generalizable', 1), r.get('perfiles'), r.get('keywords'),
                     r.get('veces_usada', 1), r.get('ultima_vez'), r.get('estado', 'activa'),
                     r.get('mejora_de'), r.get('notas'), r.get('created_at'), r.get('updated_at')))
            except sqlite3.IntegrityError:
                pass  # ya existe
        print(f"  Capacidades migradas: {len(rows)}")

    # Patrones generales/perfil → sistema
    sc.execute("SELECT COUNT(*) FROM patrones")
    if sc.fetchone()[0] == 0:
        lc = legacy.cursor()
        lc.execute("SELECT * FROM patrones WHERE tipo IN ('general', 'perfil')")
        rows = lc.fetchall()
        for r in rows:
            r = dict(r)
            sc.execute('''INSERT INTO patrones (fecha_deteccion, tipo, categoria, descripcion,
                evidencia, frecuencia, confianza, estado, sugerencia, compartido,
                anonimizado_en, ultimo_visto, notas, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (r['fecha_deteccion'], r['tipo'], r['categoria'], r['descripcion'],
                 r.get('evidencia'), r.get('frecuencia', 1), r.get('confianza', 0.5),
                 r.get('estado', 'detectado'), r.get('sugerencia'), r.get('compartido', 0),
                 r.get('anonimizado_en'), r.get('ultimo_visto'), r.get('notas'),
                 r.get('created_at'), r.get('updated_at')))
        print(f"  Patrones sistema migrados: {len(rows)}")

    sistema.commit()
    sistema.close()

    # --- Migrar a USUARIO ---
    usuario = get_usuario()
    uc = usuario.cursor()

    tablas_usuario = ['proyectos', 'personas', 'eventos', 'seguimiento',
                      'fechas_importantes', 'salud', 'metricas', 'tags',
                      'agenda', 'nutricion']

    lc = legacy.cursor()
    for tabla in tablas_usuario:
        uc.execute(f"SELECT COUNT(*) FROM {tabla}")
        if uc.fetchone()[0] > 0:
            continue  # ya tiene datos

        try:
            lc.execute(f"SELECT * FROM {tabla}")
        except sqlite3.OperationalError:
            continue  # tabla no existe en legacy

        rows = lc.fetchall()
        if not rows:
            continue

        cols = [desc[0] for desc in lc.description]
        # Excluir 'id' para que AUTOINCREMENT genere nuevos
        # Pero necesitamos preservar IDs por las FK
        placeholders = ', '.join(['?'] * len(cols))
        col_names = ', '.join(cols)
        for r in rows:
            try:
                uc.execute(f"INSERT INTO {tabla} ({col_names}) VALUES ({placeholders})",
                           tuple(dict(r)[c] for c in cols))
            except (sqlite3.IntegrityError, sqlite3.OperationalError):
                pass
        print(f"  {tabla} migrada: {len(rows)} registros")

    # Patrones personales → usuario
    uc.execute("SELECT COUNT(*) FROM patrones")
    if uc.fetchone()[0] == 0:
        lc.execute("SELECT * FROM patrones WHERE tipo = 'personal'")
        rows = lc.fetchall()
        for r in rows:
            r = dict(r)
            uc.execute('''INSERT INTO patrones (fecha_deteccion, tipo, categoria, descripcion,
                evidencia, frecuencia, confianza, estado, sugerencia, ultimo_visto, notas,
                created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (r['fecha_deteccion'], r['tipo'], r['categoria'], r['descripcion'],
                 r.get('evidencia'), r.get('frecuencia', 1), r.get('confianza', 0.5),
                 r.get('estado', 'detectado'), r.get('sugerencia'), r.get('ultimo_visto'),
                 r.get('notas'), r.get('created_at'), r.get('updated_at')))
        print(f"  Patrones usuario migrados: {len(rows)}")

    usuario.commit()
    usuario.close()
    legacy.close()

    print("\nMigración completada.")
    print(f"  Sistema: {os.path.abspath(SISTEMA_DB)}")
    print(f"  Usuario: {os.path.abspath(USUARIO_DB)}")
    print(f"  Legacy:  {os.path.abspath(LEGACY_DB)} (conservada como backup)")


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    migrar_desde_legacy()
