import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_ID = os.getenv('ALLOWED_CHAT_ID')  # Legacy, mantener por compatibilidad

# Seguridad: lista de user_ids de Telegram autorizados
# Cada usuario de ARGOS registra su user_id. Solo ellos pueden hablar con el bot.
_raw_ids = os.getenv('ALLOWED_USER_IDS', '')
ALLOWED_USER_IDS = [uid.strip() for uid in _raw_ids.split(',') if uid.strip()]

# TTS
TTS_VOICE = "es-AR-TomasNeural"

# STT
WHISPER_MODEL = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE = "int8"

# Telegram API base
API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Paths
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BOT_DIR)
TEMP_DIR = os.path.join(PROJECT_DIR, 'output')
