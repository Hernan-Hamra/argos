import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz

f = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Kaise 1-3kVA Rack.pdf'
doc = fitz.open(f)
# Get full page 2 text
text = doc[1].get_text()
print(text)
doc.close()
