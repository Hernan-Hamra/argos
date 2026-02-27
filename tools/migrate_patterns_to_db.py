"""
Migrar patrones de asesoramiento y licitaciones de .md a tabla patrones en DB.
Estos son protocolos universales de ARGOS (compartidos entre usuarios).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.tracker import get_connection
from datetime import datetime


def migrate():
    conn = get_connection()
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')

    # Verificar si ya se migraron
    c.execute("SELECT COUNT(*) as n FROM patrones WHERE tipo='protocolo_asesor'")
    if c.fetchone()['n'] > 0:
        print("ABORT: protocolos de asesor ya migrados.")
        conn.close()
        return

    # ============================================
    # PROTOCOLOS DE ASESORAMIENTO
    # ============================================

    # Flujo de trabajo
    asesor_flujo = [
        ("protocolo_asesor", "flujo", "Fase 1: Recopilar evidencia antes de asesorar",
         "Parsear chats WhatsApp, scan filesystem timestamps, cruzar fuentes en timeline verificable",
         "Caso Posadas/Richard feb 2026", "Siempre recopilar evidencia ANTES de opinar"),
        ("protocolo_asesor", "flujo", "Fase 2: Analizar situacion con contexto completo",
         "Consultar perfil_datos + personas + seguimiento. Identificar dinamicas de poder, evaluar posicion, detectar riesgos",
         "Caso Posadas/Richard feb 2026", "No opinar sin leer contexto completo primero"),
        ("protocolo_asesor", "flujo", "Fase 3: Asesorar con opinion honesta",
         "Sin condescendencia. Analisis de dinamicas de poder. Recomendar activamente (afirmar, no pedir). Descartar opciones riesgosas",
         "Caso Posadas/Richard feb 2026", "Llamar las cosas por su nombre"),
        ("protocolo_asesor", "flujo", "Fase 4: Redactar comunicacion calibrada",
         "Tono calibrado al interlocutor. Iterar con usuario. Tecnicas: afirmar no pedir, monto explicito, urgencia sin amenaza, amplitud sin detalle",
         "Caso Posadas/Richard: 6 versiones WhatsApp", "El usuario aprueba la version final"),
    ]

    # Principios
    asesor_principios = [
        ("protocolo_asesor", "principio", "Honestidad brutal cuando se pide",
         "Si el usuario dice 'no seas condescendiente', ir directo", None, None),
        ("protocolo_asesor", "principio", "Respetar agencia del usuario",
         "ARGOS asesora, el usuario decide. Nunca tomar decisiones por el", None, None),
        ("protocolo_asesor", "principio", "Nunca fabricar datos ni evidencia",
         "Ni datos, ni evidencia, ni argumentos sin base real", None, None),
        ("protocolo_asesor", "principio", "Iterar rapido con el usuario",
         "El usuario refina, ARGOS ajusta en cada vuelta", None, None),
        ("protocolo_asesor", "principio", "Calibrar tono al interlocutor",
         "El tono depende de a quien se le habla, no de lo que uno siente. Consultar personas.perfil_comportamiento", None, None),
        ("protocolo_asesor", "principio", "Proteger al usuario",
         "Detectar manipulacion, abuso de poder, patrones toxicos", None, None),
        ("protocolo_asesor", "principio", "Desaconsejar lo riesgoso",
         "Si algo debilita la posicion del usuario, decirlo explicitamente", None, None),
        ("protocolo_asesor", "principio", "Registrar toda intervencion en DB",
         "Cada accion de asesoramiento va a eventos. Si maniana importa, se registra", None, None),
    ]

    # Capacidades
    asesor_caps = [
        ("protocolo_asesor", "capacidad", "Redaccion de mensajes (WhatsApp, email, carta)",
         "Input: situacion + interlocutor + objetivo + tono. Output: mensaje listo para enviar. El usuario tiene la ultima palabra",
         None, None),
        ("protocolo_asesor", "capacidad", "Analisis de situaciones laborales/personales",
         "Input: contexto DB + evidencia. Output: opinion honesta + recomendacion. No ser condescendiente",
         None, None),
        ("protocolo_asesor", "capacidad", "Construccion de casos con evidencia",
         "Input: fuentes (chats, archivos, emails). Output: informe con timeline verificable. Solo datos reales",
         None, None),
        ("protocolo_asesor", "capacidad", "Seguimiento de reclamos y gestiones",
         "Input: accion + plazos + interlocutor. Registrar en seguimiento, alertar en proxima sesion",
         None, None),
    ]

    # ============================================
    # PROTOCOLOS DE LICITACIONES
    # ============================================

    licit_flujo = [
        ("protocolo_licitacion", "estructura", "Carpeta A1: Documentacion Legal",
         "Carta presentacion, garantia, DDJJs, estatuto, poderes, RIUPP. Caratula: 0 Caratula.pdf", None, None),
        ("protocolo_licitacion", "estructura", "Carpeta A2: Info Economico-Financiera",
         "IIBB, IVA 12 meses, ARCA, balances, IGJ, ventas, bancos", None, None),
        ("protocolo_licitacion", "estructura", "Carpeta B: Documentacion Tecnica",
         "Datos empresa, antecedentes+OC, organigrama, RT, CVs, memoria tecnica, proveedores, subcontratistas, garantia, datasheets", None, None),
        ("protocolo_licitacion", "estructura", "Carpeta C: Oferta Economica",
         "Formula oferta, planillas cotizacion, analisis de precios", None, None),
    ]

    licit_tecnico = [
        ("protocolo_licitacion", "tecnico", "Creacion documentos Word desde template",
         "Usar DDJJ existente como base (preserva header/footer). clear_body() limpia contenido manteniendo sectPr. add_para() con font, color, size via lxml. Siempre r'' para paths",
         "tools/doc_generator.py", None),
        ("protocolo_licitacion", "tecnico", "Conversion docx a PDF via Word COM",
         "Siempre taskkill /f /im WINWORD.EXE antes. win32com.client.Dispatch Word.Application, Visible=False, SaveAs FileFormat=17",
         "tools/pdf_converter.py", None),
        ("protocolo_licitacion", "tecnico", "Merge y foliacion de PDFs",
         "fitz.open() merged, insert_pdf cada archivo, agregar 'Folio: N' en bottom-right, fontsize=9, color gris (0.3,0.3,0.3). Foliacion continua entre carpetas",
         "tools/foliador.py", None),
        ("protocolo_licitacion", "tecnico", "Analisis de Precios (Anexo VII)",
         "Cadena: Costo Directo > GG% > CF% > Beneficio% > IVA > Total. IVA mix 21% + 10.5%. Trabajar hacia atras desde total. Celda cierre =TARGET-D68 para absorber floating point",
         "tools/cotizacion.py", None),
        ("protocolo_licitacion", "tecnico", "Manipulacion .docx existentes",
         "Buscar en doc.paragraphs Y doc.tables por separado. Reemplazar en run.text (no p.text) para preservar formato",
         None, None),
    ]

    licit_problemas = [
        ("protocolo_licitacion", "troubleshoot", "Encoding espaniol en paths OneDrive",
         "Usar Python scripts con r'', nunca heredoc bash", None, "Usar r'' raw strings siempre"),
        ("protocolo_licitacion", "troubleshoot", "OneDrive bloquea archivos",
         "Reintentar con time.sleep(), o pedir al usuario que cierre", None, None),
        ("protocolo_licitacion", "troubleshoot", ".docx desaparece (solo queda PDF)",
         "Buscar en subcarpeta varios/", None, None),
        ("protocolo_licitacion", "troubleshoot", "PDFs vacios (0 bytes)",
         "Skip con os.path.getsize() > 0", None, None),
        ("protocolo_licitacion", "troubleshoot", "Excel PermissionError",
         "Cerrar Excel, esperar sync OneDrive, reintentar", None, None),
        ("protocolo_licitacion", "troubleshoot", "Floating point en cadena Excel",
         "Celda de cierre referenciando target hardcodeado", None, None),
    ]

    licit_marcas = [
        ("protocolo_licitacion", "proveedor", "Furukawa (lightera.com): Cat6A, FO OM3, ODF, faceplates, patch panels",
         "Datasheets descargables directo del sitio", None, None),
        ("protocolo_licitacion", "proveedor", "Panduit: Racks 42U (4 postes, Net-Access)",
         "Datasheets descargables", None, None),
        ("protocolo_licitacion", "proveedor", "Ubiquiti (ui.com): Switches, APs, Gateways",
         "Datasheets descargables directo del sitio", None, None),
        ("protocolo_licitacion", "proveedor", "Grandstream: Centrales IP, telefonos, gateways FXO",
         "Datasheets descargables", None, None),
        ("protocolo_licitacion", "proveedor", "Kaise: UPS rack",
         "Datasheets descargables", None, None),
    ]

    # Insertar todo
    all_patterns = (asesor_flujo + asesor_principios + asesor_caps +
                    licit_flujo + licit_tecnico + licit_problemas + licit_marcas)

    for tipo, cat, desc, evidencia, evi2, sug in all_patterns:
        c.execute("""INSERT INTO patrones
                     (fecha_deteccion, tipo, categoria, descripcion, evidencia, frecuencia, confianza, estado, sugerencia, compartido)
                     VALUES (?, ?, ?, ?, ?, 1, 0.8, 'validado', ?, 1)""",
                  (hoy, tipo, cat, desc, evidencia or evi2, sug))

    conn.commit()

    # Resumen
    c.execute("SELECT tipo, categoria, COUNT(*) as n FROM patrones WHERE tipo LIKE 'protocolo_%' GROUP BY tipo, categoria ORDER BY tipo, categoria")
    print("=== PROTOCOLOS MIGRADOS ===")
    for r in c.fetchall():
        print(f"  {r['tipo']}/{r['categoria']}: {r['n']}")
    c.execute("SELECT COUNT(*) as n FROM patrones WHERE tipo LIKE 'protocolo_%'")
    print(f"  TOTAL: {c.fetchone()['n']}")

    conn.close()
    print("\nMigracion completada OK")


if __name__ == '__main__':
    migrate()
