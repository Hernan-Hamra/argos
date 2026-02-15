"""
ARGOS - Conversor docx a PDF
Usa Word COM automation para conversión fiel.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess
import time
import os


def kill_word():
    """Cierra cualquier instancia de Word abierta."""
    subprocess.run(['taskkill', '/f', '/im', 'WINWORD.EXE'],
                   capture_output=True)
    time.sleep(1)


def docx_to_pdf(docx_path, pdf_path=None):
    """
    Convierte un .docx a .pdf usando Word COM.
    Si pdf_path es None, genera el PDF en el mismo directorio con mismo nombre.
    Retorna el path del PDF generado.
    """
    if pdf_path is None:
        pdf_path = os.path.splitext(docx_path)[0] + '.pdf'

    import win32com.client
    kill_word()

    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
        print(f'PDF: {pdf_path}')
    except Exception as e:
        print(f'Error PDF: {e}')
        raise
    finally:
        word.Quit()

    return pdf_path


def batch_docx_to_pdf(docx_dir, pdf_dir=None):
    """
    Convierte todos los .docx de un directorio a PDF.
    Si pdf_dir es None, genera los PDFs en el mismo directorio.
    """
    import win32com.client
    kill_word()

    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False

    converted = []
    try:
        for f in sorted(os.listdir(docx_dir)):
            if f.endswith('.docx') and not f.startswith('~$'):
                docx_path = os.path.join(docx_dir, f)
                if pdf_dir:
                    pdf_path = os.path.join(pdf_dir, f.replace('.docx', '.pdf'))
                else:
                    pdf_path = docx_path.replace('.docx', '.pdf')

                try:
                    doc = word.Documents.Open(os.path.abspath(docx_path))
                    doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
                    doc.Close()
                    print(f'OK: {f}')
                    converted.append(pdf_path)
                except Exception as e:
                    print(f'ERROR {f}: {e}')
    finally:
        word.Quit()

    return converted
