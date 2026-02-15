import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz
import os
import re

base = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA A1 Documentación Legal'

# Get all PDFs
pdfs = [f for f in os.listdir(base) if f.lower().endswith('.pdf')]

# Sort numerically by the leading number
def sort_key(filename):
    m = re.match(r'(\d+)', filename)
    if m:
        num = int(m.group(1))
        # For sub-items like 2i, 2ii, 2iii, 16i, 16ii
        suffix = filename[m.end():m.end()+5].lower()
        sub = 0
        if suffix.startswith('i ') or suffix.startswith('i_') or suffix.startswith('i '):
            sub = 1
        elif suffix.startswith('ii ') or suffix.startswith('ii_') or suffix.startswith('ii '):
            sub = 2
        elif suffix.startswith('iii'):
            sub = 3
        return (num, sub)
    return (999, 0)

pdfs.sort(key=sort_key)

print('=== ORDEN DE MERGE ===')
folio = 1
for f in pdfs:
    doc = fitz.open(os.path.join(base, f))
    pages = doc.page_count
    print(f'  Folios {folio:3d}-{folio+pages-1:3d}  ({pages:2d} pág)  {f}')
    folio += pages
    doc.close()

print(f'\nTotal: {folio-1} folios')

# Merge all PDFs
merged = fitz.open()
for f in pdfs:
    src = fitz.open(os.path.join(base, f))
    merged.insert_pdf(src)
    src.close()

print(f'Merged: {merged.page_count} páginas')

# Add folio number to each page
for i in range(merged.page_count):
    page = merged[i]
    rect = page.rect
    # Position: bottom right, with margin
    x = rect.width - 80
    y = rect.height - 20

    text = f"Folio: {i + 1}"

    # Insert text
    page.insert_text(
        fitz.Point(x, y),
        text,
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

out = base + r'\CARPETA A1 Documentación Legal - FOLIADA.pdf'
merged.save(out)
merged.close()
print(f'\nGuardado: {out}')
