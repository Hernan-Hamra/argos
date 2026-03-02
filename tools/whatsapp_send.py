import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Perfil separado para Natalia
user_data_dir = r'C:\Users\HERNAN\AppData\Local\Google\Chrome\User Data\Natalia_WhatsApp'
os.makedirs(user_data_dir, exist_ok=True)

options = Options()
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument('--profile-directory=Default')
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)  # Mantiene Chrome abierto

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://web.whatsapp.com')

print("Chrome abierto con WhatsApp Web. Escanea el QR.")
print("Cuando estes conectada, avisame.")

# Guardar referencia para reutilizar
import pickle
pickle.dump(driver.service.port, open(r'C:\Users\HERNAN\argos\data\wapp_port.pkl', 'wb'))
print(f"Puerto guardado: {driver.service.port}")
