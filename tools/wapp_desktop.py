"""
WhatsApp Desktop automation via pywinauto
Envia mensajes personalizados con imagen y PDF
"""
import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')

from pywinauto import Desktop
import pyautogui
import win32clipboard

# ---------- CONFIG ----------
IMAGENES_DIR = r'C:\Users\HERNAN\OneDrive\PRUEBA ARGOS NATALIA\PURIM_5786\imagenes'
MEGUILAT_PDF = r'C:\Users\HERNAN\OneDrive\PRUEBA ARGOS NATALIA\PURIM_5786\MEGUILAT ESTER PARA NIÑOS .pdf'

PRUEBAS = [
    {'contacto': 'Natalia Indibo', 'nombre': 'Natalia'},
    {'contacto': 'Hernán Hamra',   'nombre': 'Hernán'},
    {'contacto': 'Ariel Indibo',   'nombre': 'Ariel'},
    {'contacto': 'Jonathan Indibo','nombre': 'Jonathan'},
]

IMAGEN_PRUEBA = os.path.join(IMAGENES_DIR, 'ABAD ISAAC salutacion purim 5786.jpg')

def texto_intro(nombre):
    return (
        f"Hola {nombre}\n"
        f"Te envío una nota de parte del Gran Rabino Isaac Sacca con motivo de la festividad de Purim.\n"
        f"Enviamos también una Meguilat Esther para niños, una oportunidad ideal para compartir en familia."
    )

def clipboard_paste(text):
    """Copia texto al clipboard y pega con Ctrl+V"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()
    pyautogui.hotkey('ctrl', 'v')

def get_app():
    """Conecta con la ventana de WhatsApp Desktop"""
    desktop = Desktop(backend='uia')
    app = desktop.window(title='WhatsApp')
    app.set_focus()
    time.sleep(0.5)
    return app

def buscar_contacto(app, nombre_contacto):
    """Busca y abre un chat por nombre de contacto"""
    print(f"  Buscando contacto: {nombre_contacto}")

    # Obtener el search box
    search = app.child_window(title="Cuadro de texto para ingresar la búsqueda", control_type="Edit")
    search.click_input()
    time.sleep(0.3)

    # Limpiar y escribir nombre
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    clipboard_paste(nombre_contacto)
    time.sleep(2)

    # Presionar Enter para seleccionar primer resultado
    pyautogui.press('enter')
    time.sleep(1)

    # Verificar que se abrio el chat (el titulo del header deberia tener el nombre)
    print(f"  Chat abierto")
    return True

def enviar_texto(app, texto):
    """Envia un mensaje de texto al chat abierto"""
    print(f"  Enviando texto...")

    # Buscar el message box (contiene "Escribe" en el nombre)
    edits = app.descendants(control_type='Edit')
    msg_box = None
    for e in edits:
        name = e.element_info.name or ''
        if 'Escribe' in name:
            msg_box = e
            break

    if not msg_box:
        print("  ERROR: No se encontro el campo de mensaje")
        return False

    msg_box.click_input()
    time.sleep(0.3)

    # Enviar cada linea con Shift+Enter para nueva linea
    lineas = texto.split('\n')
    for i, linea in enumerate(lineas):
        clipboard_paste(linea)
        time.sleep(0.2)
        if i < len(lineas) - 1:
            pyautogui.hotkey('shift', 'enter')
            time.sleep(0.1)

    # Enviar con Enter
    pyautogui.press('enter')
    time.sleep(2)
    print(f"  Texto enviado OK")
    return True

def enviar_archivo(app, filepath):
    """Adjunta y envia un archivo"""
    print(f"  Adjuntando: {os.path.basename(filepath)}")

    # Click en boton Adjuntar
    adj_btn = app.child_window(title="Adjuntar", control_type="Button")
    adj_btn.click_input()
    time.sleep(1)

    # Buscar la opcion adecuada en el menu
    if filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Buscar "Fotos y videos" o similar
        try:
            foto_btn = app.child_window(title_re=".*[Ff]oto.*|.*[Ii]mag.*", control_type="Button")
            foto_btn.click_input()
        except:
            # Si no encuentra, buscar "Documento" como fallback
            try:
                doc_btn = app.child_window(title_re=".*[Dd]ocument.*", control_type="Button")
                doc_btn.click_input()
            except:
                print("  No se encontro opcion de adjuntar. Intentando con teclado...")
                pyautogui.press('escape')
                return False
    else:
        # Para PDFs y otros: Documento
        try:
            doc_btn = app.child_window(title_re=".*[Dd]ocument.*", control_type="Button")
            doc_btn.click_input()
        except:
            print("  No se encontro opcion Documento")
            pyautogui.press('escape')
            return False

    time.sleep(2)

    # Deberia abrirse el dialogo de archivos de Windows
    # Escribir la ruta del archivo
    clipboard_paste(filepath)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    # Enviar el archivo (boton Enviar en la preview)
    pyautogui.press('enter')
    time.sleep(3)

    print(f"  Archivo enviado OK")
    return True

def enviar_mensaje_completo(app, contacto, nombre, imagen_path, pdf_path=None):
    """Flujo completo: buscar contacto, enviar texto, imagen y PDF"""
    print(f"\n{'='*50}")
    print(f"Enviando a: {contacto}")
    print(f"{'='*50}")

    # 1. Buscar y abrir chat
    if not buscar_contacto(app, contacto):
        return False

    # 2. Enviar texto introductorio
    texto = texto_intro(nombre)
    if not enviar_texto(app, texto):
        return False

    # 3. Enviar imagen
    if not enviar_archivo(app, imagen_path):
        print("  WARNING: Fallo envio de imagen")

    # 4. Enviar PDF si hay
    if pdf_path:
        if not enviar_archivo(app, pdf_path):
            print("  WARNING: Fallo envio de PDF")

    print(f"  COMPLETADO: {contacto}")
    return True

if __name__ == '__main__':
    print("=== WhatsApp Desktop Automation ===")
    print(f"Imagen de prueba: {IMAGEN_PRUEBA}")
    print(f"PDF: {os.path.basename(MEGUILAT_PDF)}")

    app = get_app()

    for prueba in PRUEBAS:
        ok = enviar_mensaje_completo(
            app,
            prueba['contacto'],
            prueba['nombre'],
            IMAGEN_PRUEBA,
            MEGUILAT_PDF
        )
        if ok:
            print(f"  >> OK")
        else:
            print(f"  >> ERROR")
        time.sleep(3)

    print("\n=== Prueba completada ===")
