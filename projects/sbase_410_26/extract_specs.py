import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz

files = [
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\UniFi Pro 48 PoE - Tech Specs.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\UniFi Cloud Gateway Fiber - Tech Specs.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\UniFi U6 Long-Range - Tech Specs.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Datasheet_UCM6300_Audio_Series_Spanish.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Datasheet_GRP2601_Spanish.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Datasheet_HT841_HT881_Spanish.pdf',
    r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\1 LICITACIONES EN PRESENTACIÓN\3 SBASE CABLEADO ESTRUCTURADO\LICI SBASE CABLEADO 2026\DOC A PRESENTAR\CARPETA B Documentación Técnica\DATASHEET\Kaise 1-3kVA Rack.pdf',
]

for i, f in enumerate(files, 1):
    fname = f.split('\\')[-1]
    print(f"\n{'='*80}")
    print(f"FILE {i}: {fname}")
    print('='*80)
    try:
        doc = fitz.open(f)
        print(f"Total pages: {doc.page_count}")
        # Read page 1
        text = doc[0].get_text()
        print(f"\n--- PAGE 1 ---")
        print(text[:4000])
        if len(text) > 4000:
            print(f"\n... [truncated, total {len(text)} chars on page 1]")
        # If page 1 is very short, also read page 2
        if len(text.strip()) < 300 and doc.page_count > 1:
            print(f"\n--- PAGE 2 (page 1 was short) ---")
            text2 = doc[1].get_text()
            print(text2[:3000])
        doc.close()
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n{'='*80}")
print("DONE - All PDFs processed")
print('='*80)
