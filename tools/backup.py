"""
ARGOS Backup - Respalda la DB a OneDrive
Uso: python tools/backup.py
"""
import shutil
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'argos_tracker.db')
BACKUP_DIR = os.path.join(os.path.expanduser('~'), 'OneDrive', '1. ORGANIZACION FLIA', 'ARGOS_BACKUP')


def backup_db():
    """Copiar DB a OneDrive con timestamp."""
    if not os.path.exists(DB_PATH):
        print(f"ERROR: No se encuentra la DB en {DB_PATH}")
        return False

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f'argos_tracker_{timestamp}.db'
    dest = os.path.join(BACKUP_DIR, filename)

    shutil.copy2(DB_PATH, dest)
    size_kb = os.path.getsize(dest) / 1024

    # También mantener una copia "latest"
    latest = os.path.join(BACKUP_DIR, 'argos_tracker_latest.db')
    shutil.copy2(DB_PATH, latest)

    print(f"Backup OK: {filename} ({size_kb:.0f}KB)")
    print(f"Latest actualizado: argos_tracker_latest.db")
    print(f"Destino: {BACKUP_DIR}")

    # Limpiar backups viejos (mantener últimos 10)
    backups = sorted([f for f in os.listdir(BACKUP_DIR)
                      if f.startswith('argos_tracker_2') and f.endswith('.db')])
    if len(backups) > 10:
        for old in backups[:-10]:
            os.remove(os.path.join(BACKUP_DIR, old))
            print(f"  Borrado viejo: {old}")

    return True


if __name__ == '__main__':
    backup_db()
