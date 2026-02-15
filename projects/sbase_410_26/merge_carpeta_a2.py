import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz
import os
import re

base = r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA A2 Información Económico-Financiera'

# Build ordered file list by category
ordered_files = []

# 0. Carátula
ordered_files.append('0 Carátula.pdf')

# 1. Constancia inscripción Ingresos Brutos
ordered_files.append('1 Constancia de Inscripción Convenio Multilateral 2026.pdf')

# 2. DDJJ IIBB últimos 12 meses con presentación y pago
# For each month 01-12/2025: DDJJ_Mensual + PRESENTACION
iibb_months = {
    '01': ('DDJJ_Mensual_395620014 IIBB 01-2025 RECTIFICADO.pdf', 'PRESENTACION IIBB 01-2025 RECTIFICADO.pdf'),
    '02': ('DDJJ_Mensual_395621773 IIBB 02-2025 RECTIFICADO.pdf', 'PRESENTACION IIBB 02-2025 RECTIFICADO.pdf'),
    '03': ('DDJJ_Mensual_395623573 IIBB 03-2025 RECTIFICADO.pdf', 'PRESENTACION IIBB 03-2025 RECTIFICADO.pdf'),
    '04': ('DDJJ_Mensual_395626237 IIBB 04-2025 RECTIFICADO.pdf', 'PRESENTACION IIBB 04-2025 RECTIFICADO .pdf'),
    '05': ('DDJJ_Mensual_395629318 IIBB 05-2025.pdf', 'PRESENTACION IIBB 05-2025.pdf'),
    '06': ('DDJJ_Mensual_398505937 IIBB 06-2025.pdf', 'PRESENTACION IIBB 06-2025.pdf'),
    '07': ('DDJJ_Mensual_401414211 IIBB 07-2025.pdf', 'PRESENTACION IIBB 07-2025.pdf'),
    '08': ('DDJJ_Mensual_404117763 IIBB 08-2025.pdf', 'PRESENTACION IIBB 08-2025.pdf'),
    '09': ('DDJJ_Mensual_406768171 IIBB 09-2025.pdf', 'PRESENTACION IIBB 09-2025.pdf'),
    '10': ('DDJJ_Mensual_408898489  IIBB 10-2025.pdf', 'PRESENTACION IIBB 10-2025.pdf'),
    '11': ('DDJJ_Mensual_411635997 IIBB 11-2025.pdf', 'PRESENTACION IIBB 11-2025.pdf'),
    '12': ('DDJJ_Mensual_413799786 IIBB 12-2025.pdf', 'PRESENTACION IIBB 12-2025.pdf'),
}
for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
    ddjj, pres = iibb_months[m]
    ordered_files.append(ddjj)
    ordered_files.append(pres)

# 3. DDJJ IVA últimos 12 meses con constancia de pago
# Months 01-05: DJ IVA + ARCA-Presentación
# Months 06-12: F.2051 + ARCA-Presentación
# Plus payment proofs where available
iva_files = {
    '01': ['DJ IVA 01-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 01-2025.pdf',
           'Comprobante_2026-02-12 COMPENSADO 01-2025.pdf'],
    '02': ['DJ IVA 02-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 02-2025.pdf',
           'Comprobante_2025-05-19 COMPENSADO 02-2025.pdf'],
    '03': ['DJ IVA 03-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 03-2025.pdf'],
    '04': ['DJ IVA 04-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 04-2025.pdf'],
    '05': ['DJ IVA 05-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 05-2025.pdf'],
    '06': ['F.2051 - DJ IVA - SIMPLE 06-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 6-2025.pdf'],
    '07': ['F.2051 - DJ IVA - SIMPLE 07-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 7-2025.pdf'],
    '08': ['F.2051 - DJ IVA - SIMPLE 08-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 8-2025.pdf'],
    '09': ['F.2051 - DJ IVA - SIMPLE 09-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 9-2025.pdf'],
    '10': ['F.2051 - DJ IVA - SIMPLE 10-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 10-2025.pdf',
           'PAGO IVA 10-2025.pdf'],
    '11': ['F.2051 - DJ IVA - SIMPLE 11-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 11-2025.pdf'],
    '12': ['F.2051 - DJ IVA - SIMPLE 12-2025.pdf', 'ARCA-Presentación de DDJJ y Pagos IVA 12-2025.pdf'],
}
for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
    for f in iva_files[m]:
        ordered_files.append(f)

# 4. Constancia inscripción AFIP (ARCA)
ordered_files.append('4 ARCA - Constancia de inscrpcion.pdf')

# 5. Memoria y Balance últimos 2 ejercicios
ordered_files.append('5 balance 2023 SBD certificado y firmado.pdf')
ordered_files.append('5 balance 2024.pdf')

# 6. Constancia presentación balances en IGJ
ordered_files.append('6i EECC_30711908249_2023.pdf')
ordered_files.append('6ii EECC_30711908249_2024.pdf')

# 7. Certificación contable de ventas
ordered_files.append('7 Nota Certificación Contable de Ventas.pdf')
ordered_files.append('7 DDJJ de Ventas al 30-09-2025 (últimos 36 meses).pdf')

# 8. Listado de bancos
ordered_files.append('8 Listado de bancos con los que opera .pdf')

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

# Check if there are files we're NOT including
all_pdfs = set(f for f in os.listdir(base) if f.lower().endswith('.pdf'))
included = set(ordered_files)
not_included = all_pdfs - included
if not_included:
    print(f'\nArchivos NO incluidos:')
    for f in sorted(not_included):
        print(f'  - {f}')

print(f'\nArchivos a incluir: {len(ordered_files)}')

# Show order with folio numbers
FOLIO_START = 76
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

out = base + r'\CARPETA A2 Información Económico-Financiera - FOLIADA.pdf'
merged.save(out)
merged.close()
print(f'\nGuardado: {out}')
