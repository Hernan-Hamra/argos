"""
ARGOS - Foliador de PDFs
Merge múltiples PDFs en orden y agrega número de folio a cada página.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import fitz
import os


def merge_and_foliate(pdf_list, output_path, folio_start=1,
                      fontsize=9, color=(0.3, 0.3, 0.3),
                      prefix="Folio: ", position="bottom_right",
                      margin_x=80, margin_y=20):
    """
    Merge una lista de PDFs y agrega foliación.

    Args:
        pdf_list: lista de paths a PDFs (en orden)
        output_path: path del PDF resultante
        folio_start: número del primer folio
        fontsize: tamaño de fuente del folio
        color: color RGB (0-1) del texto
        prefix: texto antes del número ("Folio: ")
        position: "bottom_right" o "bottom_left"
        margin_x: margen horizontal desde el borde
        margin_y: margen vertical desde el borde inferior

    Returns:
        dict con total_pages y folio_range
    """
    merged = fitz.open()
    file_info = []

    for pdf_path in pdf_list:
        if not os.path.exists(pdf_path):
            print(f'  SKIP (no existe): {pdf_path}')
            continue
        if os.path.getsize(pdf_path) == 0:
            print(f'  SKIP (vacío): {os.path.basename(pdf_path)}')
            continue

        src = fitz.open(pdf_path)
        start_page = merged.page_count
        merged.insert_pdf(src)
        file_info.append({
            'file': os.path.basename(pdf_path),
            'pages': src.page_count,
            'folio_start': folio_start + start_page,
        })
        src.close()

    # Agregar foliación
    for i in range(merged.page_count):
        page = merged[i]
        rect = page.rect
        folio_num = folio_start + i
        text = f"{prefix}{folio_num}"

        if position == "bottom_right":
            x = rect.width - margin_x
        else:
            x = margin_x

        y = rect.height - margin_y

        page.insert_text(
            fitz.Point(x, y),
            text,
            fontsize=fontsize,
            fontname="helv",
            color=color,
        )

    merged.save(output_path)
    total = merged.page_count
    merged.close()

    return {
        'total_pages': total,
        'folio_start': folio_start,
        'folio_end': folio_start + total - 1,
        'files': file_info,
    }


def print_folio_summary(result):
    """Imprime resumen de foliación."""
    for fi in result['files']:
        end = fi['folio_start'] + fi['pages'] - 1
        print(f"  Folios {fi['folio_start']:3d}-{end:3d}  ({fi['pages']:2d} pág)  {fi['file']}")
    print(f"\nTotal: {result['total_pages']} folios "
          f"(del {result['folio_start']} al {result['folio_end']})")
