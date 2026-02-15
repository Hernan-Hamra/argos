import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz

files = [
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Datasheet_UCM6300_Audio_Series_Spanish.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Datasheet_HT841_HT881_Spanish.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Kaise 1-3kVA Rack.pdf',
]

for i, f in enumerate(files, 1):
    fname = f.split('\\')[-1]
    print(f"\n{'='*80}")
    print(f"FILE: {fname} - PAGE 2")
    print('='*80)
    try:
        doc = fitz.open(f)
        if doc.page_count > 1:
            text = doc[1].get_text()
            print(text[:4000])
        else:
            print("Only 1 page in document")
        doc.close()
    except Exception as e:
        print(f"ERROR: {e}")
