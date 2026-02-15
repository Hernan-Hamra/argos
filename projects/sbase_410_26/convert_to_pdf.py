import sys, subprocess, time, os
sys.stdout.reconfigure(encoding='utf-8')

# Kill any running Word instances
subprocess.run(['taskkill', '/f', '/im', 'WINWORD.EXE'], capture_output=True)
time.sleep(2)

import win32com.client

base = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica'

files = [
    '3 Organigrama del Proyecto.docx',
    '4 CV Marcelo Hamra - Director Técnico.docx',
    '5 CV Hernán Hamra - Director de Proyecto.docx',
]

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

for f in files:
    docx_path = os.path.join(base, f)
    pdf_path = docx_path.replace('.docx', '.pdf')
    print(f'Convirtiendo: {f}')
    try:
        doc = word.Documents.Open(docx_path)
        doc.SaveAs2(pdf_path, FileFormat=17)
        doc.Close()
        print(f'  -> OK: {pdf_path}')
    except Exception as e:
        print(f'  -> ERROR: {e}')

word.Quit()
print('\nTodos los PDFs generados.')
