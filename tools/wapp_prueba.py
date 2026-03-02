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

IMAGENES_DIR = r'C:\Users\HERNAN\OneDrive\PRUEBA ARGOS NATALIA\PURIM_5786\imagenes'
MEGUILAT_PDF = r'C:\Users\HERNAN\OneDrive\PRUEBA ARGOS NATALIA\PURIM_5786\MEGUILAT ESTER PARA NIÑOS .pdf'

PRUEBAS = [
    {'contacto': 'Natalia Indibo', 'nombre': 'Natalia'},
    {'contacto': 'Hernán Hamra', 'nombre': 'Hernán'},
    {'contacto': 'Ariel Indibo', 'nombre': 'Ariel'},
    {'contacto': 'Jonathan Indibo', 'nombre': 'Jonathan'},
]

def texto_intro(nombre):
    return (
        f"Hola {nombre}\n"
        f"Te envío una nota de parte del Gran Rabino Isaac Sacca con motivo de la festividad de Purim.\n"
        f"Enviamos también una Meguilat Esther para niños, una oportunidad ideal para compartir en familia."
    )

def enviar_archivo(driver, archivo_path):
    wait = WebDriverWait(driver, 30)
    attach_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@title="Adjuntar" or @title="Attach"]')
    ))
    attach_btn.click()
    time.sleep(1)

    if archivo_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        file_input = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    else:
        file_input = driver.find_element(By.XPATH, '//input[@accept="*"]')

    file_input.send_keys(archivo_path)
    time.sleep(3)

    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@role="button"][@aria-label="Enviar" or @aria-label="Send"]')
    ))
    send_btn.click()
    time.sleep(3)

def enviar_mensaje(driver, contacto, texto, imagen_path, pdf_path=None):
    wait = WebDriverWait(driver, 30)

    search_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    ))
    search_box.clear()
    search_box.click()
    time.sleep(0.5)
    search_box.send_keys(contacto)
    time.sleep(2)

    try:
        result = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//span[@title="{contacto}"]')
        ))
        result.click()
    except:
        results = driver.find_elements(By.XPATH, '//div[@role="listitem"]')
        if results:
            results[0].click()
        else:
            print(f"  NO ENCONTRADO: {contacto}")
            return False
    time.sleep(1)

    msg_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    ))
    msg_box.click()

    for i, linea in enumerate(texto.split('\n')):
        msg_box.send_keys(linea)
        if i < len(texto.split('\n')) - 1:
            msg_box.send_keys(Keys.SHIFT + Keys.ENTER)

    msg_box.send_keys(Keys.ENTER)
    time.sleep(2)

    enviar_archivo(driver, imagen_path)

    if pdf_path:
        enviar_archivo(driver, pdf_path)

    return True

if __name__ == '__main__':
    # Usar perfil local de Chrome para mantener sesion WhatsApp
    user_data = r'C:\Users\HERNAN\AppData\Local\Google\Chrome\User Data'
    options = Options()
    options.add_argument(f'--user-data-dir={user_data}')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--start-maximized')
    options.add_experimental_option('detach', True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://web.whatsapp.com')

    print("=== Chrome abierto con WhatsApp Web ===")
    print("Escanea el QR con tu celular.")
    print("Esperando conexion (5 minutos)...")

    wait = WebDriverWait(driver, 300)
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        ))
        print("WhatsApp Web conectado!\n")
    except:
        print("Timeout. Escanea el QR y volve a correr.")
        sys.exit(1)

    imagen_prueba = os.path.join(IMAGENES_DIR, 'ABAD ISAAC salutacion purim 5786.jpg')

    for prueba in PRUEBAS:
        contacto = prueba['contacto']
        nombre = prueba['nombre']
        texto = texto_intro(nombre)

        print(f"Enviando a {contacto}...")
        ok = enviar_mensaje(driver, contacto, texto, imagen_prueba, MEGUILAT_PDF)
        if ok:
            print(f"  OK - Enviado a {contacto}")
        else:
            print(f"  ERROR - {contacto}")
        time.sleep(3)

    print("\nPrueba completada!")
