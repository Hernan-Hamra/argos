import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz
import os

base = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica'
ds_dir = os.path.join(base, 'DATASHEET')
oc_dir = os.path.join(base, '2c OC Respaldatorias')

ordered_files = []

def add(filename, subdir=None):
    if subdir:
        ordered_files.append(os.path.join(subdir, filename))
    else:
        ordered_files.append(filename)

# 0. Carátula
add('0 Carátula.pdf')

# 1. Datos de la empresa
add('1 Datos de la Empresa.pdf')

# 2. Antecedentes
add('2a DDJJ Antecedentes e Idoneidad Técnica.pdf')
add('2b Listado Detallado de Antecedentes.pdf')

# 2c. OC Respaldatorias (sorted, skip empty files)
oc_files = sorted([f for f in os.listdir(oc_dir) if f.endswith('.pdf')])
for f in oc_files:
    fp = os.path.join(oc_dir, f)
    if os.path.getsize(fp) > 0:
        add(f, '2c OC Respaldatorias')
    else:
        print(f'  SKIP (vacío): {f}')

# 3. Organigrama
add('3 Organigrama del Proyecto.pdf')

# 4. Representante Técnico + CV
add('4 CV Marcelo Hamra - Director Técnico.pdf')
add('4a Carta de Designación Representante Técnico.pdf')
add('4b Carta de Aceptación Representante Técnico.pdf')

# 5. CV Director de Proyecto
add('5 CV Hernán Hamra - Director de Proyecto.pdf')

# 6. Memoria Técnica y Plan de Trabajo
add('6 Memoria Técnica y Plan de Trabajo.pdf')

# 7. Lista de Proveedores
add('7 Lista de Proveedores.pdf')

# 8. Nota Subcontratistas
add('8 Nota Subcontratistas.pdf')

# 9. DDJJ Plazo de Garantía
add('9 DDJJ Plazo de Garantía.pdf')

# 10. Carátula Datasheets
add('10 Carátula Datasheets.pdf')

# Datasheets - ordered by brand: Furukawa, Ubiquiti, Grandstream, Panduit, Kaise
ds_order = [
    # Furukawa Cat6A
    'Furukawa - Cable GigaLan Cat6A U-UTP.pdf',
    'Furukawa - Conector Hembra Cat6A.pdf',
    'Furukawa - Patch Cord Cat6A.pdf',
    'Furukawa - Patch Cord F-UTP Cat6A Cobre.pdf',
    'Furukawa - Patch Panel Modular GigaLan Cat6.pdf',
    'Furukawa - Faceplate Modular.pdf',
    # Furukawa Fibra
    'Furukawa - Cable Fiber-LAN Indoor OM3.pdf',
    'Furukawa - Cable Fiber-LAN Indoor-Outdoor.pdf',
    'Furukawa - DIO BW12 ODF.pdf',
    # 'Furukawa - Portfolio Datacenter.pdf',  # Sacado: 53 pág, muy pesado
    # Ubiquiti
    'UniFi Pro 48 PoE - Tech Specs.pdf',
    'UniFi Cloud Gateway Fiber - Tech Specs.pdf',
    'UniFi U6 Long-Range - Tech Specs.pdf',
    # Grandstream
    'Datasheet_UCM6300_Audio_Series_Spanish.pdf',
    'Datasheet_GRP2601_Spanish.pdf',
    'Datasheet_HT841_HT881_Spanish.pdf',
    # Panduit
    'Panduit - Rack 4 Postes 42U.pdf',
    'Panduit - Rack Net-Access.pdf',
    # Kaise
    'Kaise 1-3kVA Rack.pdf',
    'KAISE - UPS 6-10 kva battery pack user manual.pdf',
]
for f in ds_order:
    add(f, 'DATASHEET')

# Verify all files exist
print('=== VERIFICACIÓN ===')
missing = []
for f in ordered_files:
    fp = os.path.join(base, f)
    if not os.path.exists(fp):
        print(f'  FALTA: {f}')
        missing.append(f)

if missing:
    print(f'\n¡{len(missing)} archivos faltantes! Abortando.')
    sys.exit(1)
else:
    print('  Todos los archivos OK')

FOLIO_START = 194
folio = FOLIO_START

print(f'\n=== ORDEN DE MERGE (folio desde {FOLIO_START}) ===')
for f in ordered_files:
    doc = fitz.open(os.path.join(base, f))
    pages = doc.page_count
    name = os.path.basename(f)
    print(f'  Folios {folio:3d}-{folio+pages-1:3d}  ({pages:2d} pág)  {name}')
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

out = base + r'\CARPETA B Documentación Técnica - FOLIADA.pdf'
merged.save(out)
merged.close()
print(f'\nGuardado: {out}')
