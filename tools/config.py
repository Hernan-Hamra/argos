"""
ARGOS Config Centralizado
Toda la configuración en un solo lugar. Funciona en Win/Mac/Linux/Cloud.

Prioridad de configuración:
  1. Variables de entorno (ARGOS_DB_PATH, ARGOS_BACKUP_DIR, etc.)
  2. Archivo .env en raíz del proyecto
  3. Defaults calculados automáticamente

Uso:
    from tools.config import DB_PATH, BACKUP_DIR, BASE_DIR, get_connection
"""

import os
import sys
import sqlite3
import platform

# ============================================================
# PATHS BASE
# ============================================================

# Raíz del proyecto ARGOS (un nivel arriba de tools/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Directorio de datos
DATA_DIR = os.environ.get('ARGOS_DATA_DIR',
                          os.path.join(BASE_DIR, 'data'))

# Base de datos principal
DB_PATH = os.environ.get('ARGOS_DB_PATH',
                         os.path.join(DATA_DIR, 'argos_tracker.db'))

# Directorio de output (archivos generados)
OUTPUT_DIR = os.environ.get('ARGOS_OUTPUT_DIR',
                            os.path.join(BASE_DIR, 'output'))

# Directorio de templates
TEMPLATES_DIR = os.environ.get('ARGOS_TEMPLATES_DIR',
                               os.path.join(BASE_DIR, 'templates'))

# Directorio de tools
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')

# ============================================================
# BACKUP
# ============================================================

def _default_backup_dir():
    """Calcula directorio de backup según plataforma."""
    custom = os.environ.get('ARGOS_BACKUP_DIR')
    if custom:
        return custom

    home = os.path.expanduser('~')

    # Windows: OneDrive si existe
    if platform.system() == 'Windows':
        onedrive = os.path.join(home, 'OneDrive', '1. ORGANIZACION FLIA', 'ARGOS_BACKUP')
        if os.path.exists(os.path.dirname(onedrive)):
            return onedrive

    # Mac: iCloud si existe, sino Documents
    if platform.system() == 'Darwin':
        icloud = os.path.join(home, 'Library', 'Mobile Documents',
                              'com~apple~CloudDocs', 'ARGOS_BACKUP')
        if os.path.exists(os.path.dirname(os.path.dirname(icloud))):
            return icloud
        return os.path.join(home, 'Documents', 'ARGOS_BACKUP')

    # Linux/Cloud: directorio local
    return os.path.join(DATA_DIR, 'backups')


BACKUP_DIR = _default_backup_dir()

# ============================================================
# SAFETY LOG
# ============================================================

SAFETY_LOG_PATH = os.environ.get('ARGOS_SAFETY_LOG',
                                  os.path.join(DATA_DIR, 'safety_log.db'))

# ============================================================
# PLATAFORMA
# ============================================================

PLATFORM = platform.system()  # 'Windows', 'Darwin', 'Linux'
IS_WINDOWS = PLATFORM == 'Windows'
IS_MAC = PLATFORM == 'Darwin'
IS_LINUX = PLATFORM == 'Linux'
IS_CLOUD = os.environ.get('ARGOS_CLOUD', '').lower() in ('1', 'true', 'yes')

# ============================================================
# CONEXIÓN DB (función canónica)
# ============================================================

def get_connection(db_path=None):
    """Conectar a la DB. Crea directorio data/ si no existe.

    Args:
        db_path: path alternativo (default: DB_PATH principal)

    Returns:
        sqlite3.Connection con row_factory=Row y foreign_keys=ON
    """
    path = db_path or DB_PATH
    db_dir = os.path.dirname(path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# TELEGRAM / BOTS (lee de .env)
# ============================================================

def _load_env():
    """Carga .env si existe (sin depender de python-dotenv)."""
    env_path = os.path.join(BASE_DIR, '.env')
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        pass

# Cargar .env al importar config
_load_env()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('ALLOWED_CHAT_ID', '')
TELEGRAM_USER_IDS = [
    uid.strip() for uid in os.environ.get('ALLOWED_USER_IDS', '').split(',')
    if uid.strip()
]
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# ============================================================
# ESCANEO AUTO-APRENDIZAJE
# ============================================================

SCAN_DIRS = {
    'tools': os.path.join(BASE_DIR, 'tools'),
    'hooks': os.path.join(BASE_DIR, '.claude', 'hooks'),
    'agents': os.path.join(BASE_DIR, 'agents'),
    'bot': os.path.join(BASE_DIR, 'bot'),
}

SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.sh'}
SCAN_INTERVAL_MIN = 30
SCAN_CADA_N_MENSAJES = 20

# ============================================================
# DIAGNÓSTICO
# ============================================================

def diagnostico():
    """Muestra la configuración actual para debug."""
    info = {
        'BASE_DIR': BASE_DIR,
        'DATA_DIR': DATA_DIR,
        'DB_PATH': DB_PATH,
        'DB_EXISTS': os.path.exists(DB_PATH),
        'BACKUP_DIR': BACKUP_DIR,
        'PLATFORM': PLATFORM,
        'IS_CLOUD': IS_CLOUD,
        'TELEGRAM_CONFIGURED': bool(TELEGRAM_BOT_TOKEN),
        'GROQ_CONFIGURED': bool(GROQ_API_KEY),
        'ANTHROPIC_CONFIGURED': bool(ANTHROPIC_API_KEY),
        'EMAIL_CONFIGURED': bool(os.environ.get('EMAIL_ADDRESS')),
        'EMAIL2_CONFIGURED': bool(os.environ.get('EMAIL2_ADDRESS')),
    }
    return info


if __name__ == '__main__':
    import json
    print(json.dumps(diagnostico(), indent=2, ensure_ascii=False, default=str))
