import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz
import os

base = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA C Oferta Económica'

# Only PDFs in order (skip xlsx and varios annexos)
ordered_files = [
    '0 Carátula.pdf',
    '1 ANEXO V MODELO DE FÓRMULA DE LA OFERTA.pdf',
    '2 ANEXO VI PLANILLAS DE COTIZACIÓN Y DESGLOSE.pdf',
    '3 Anexo VII MODELO DE ANALISIS DE PRECIOS.pdf',
]

# Verify
print('=== VERIFICACIÓN ===')
for f in ordered_files:
    fp = os.path.join(base, f)
    if not os.path.exists(fp):
        print(f'  FALTA: {f}')
        sys.exit(1)
print('  Todos OK')

FOLIO_START = 377
folio = FOLIO_START

print(f'\n=== ORDEN DE MERGE (folio desde {FOLIO_START}) ===')
for f in ordered_files:
    doc = fitz.open(os.path.join(base, f))
    pages = doc.page_count
    print(f'  Folios {folio:3d}-{folio+pages-1:3d}  ({pages:2d} pág)  {f}')
    folio += pages
    doc.close()

print(f'\nTotal: {folio - FOLIO_START} folios (del {FOLIO_START} al {folio-1})')

# Merge
merged = fitz.open()
for f in ordered_files:
    src = fitz.open(os.path.join(base, f))
    merged.insert_pdf(src)
    src.close()

print(f'Merged: {merged.page_count} páginas')

# Add folio numbers
for i in range(merged.page_count):
    page = merged[i]
    rect = page.rect
    x = rect.width - 80
    y = rect.height - 20
    text = f"Folio: {FOLIO_START + i}"
    page.insert_text(
        fitz.Point(x, y),
        text,
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

out = base + r'\CARPETA C Oferta Económica - FOLIADA.pdf'
merged.save(out)
merged.close()
print(f'\nGuardado: {out}')
