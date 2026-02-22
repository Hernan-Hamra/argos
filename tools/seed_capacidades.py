"""Script para poblar el catálogo con TODAS las capacidades reales de ARGOS."""
import sys
sys.path.insert(0, r'C:\Users\HERNAN\argos')
sys.stdout.reconfigure(encoding='utf-8')
from tools.tracker import add_capacidad

nuevas = [
    # --- COMUNICACIÓN (sin tool dedicado — LLM directo) ---
    ('redaccion_email', 'Redacción de emails formales',
     'Redacta emails con tono calibrado: pedidos, reclamos, informes, seguimiento.',
     'LLM directo (sin tool)',
     ['Analizar contexto y destinatario', 'Calibrar tono', 'Redactar con estructura', 'Ofrecer versiones', 'Confirmar'],
     'comunicacion', ['profesional_independiente', 'pyme'],
     'email, formal, pedido, reclamo, informe, redactar'),

    ('redaccion_whatsapp', 'Redacción de WhatsApp',
     'Redacta mensajes WhatsApp con tono adecuado. Individuales o para grupos.',
     'LLM directo (sin tool)',
     ['Identificar destinatario', 'Adaptar tono', 'Redactar conciso', 'Confirmar'],
     'comunicacion', ['profesional_independiente', 'pyme', 'familia'],
     'whatsapp, mensaje, grupo, chat, redactar'),

    ('analisis_chat_whatsapp', 'Análisis de cadenas WhatsApp',
     'Analiza conversaciones WhatsApp: extrae decisiones, pendientes, timeline, conflictos.',
     'LLM directo (sin tool)',
     ['Recibir texto del chat', 'Identificar participantes', 'Extraer cronología', 'Detectar pendientes', 'Generar resumen'],
     'analisis', ['profesional_independiente', 'pyme'],
     'chat, whatsapp, analisis, conversacion, timeline'),

    # --- ESTRATEGIA Y ASESORÍA ---
    ('analisis_dinamicas', 'Análisis de dinámicas interpersonales',
     'Analiza relaciones laborales/personales, detecta patrones, sugiere estrategias.',
     'LLM directo (sin tool)',
     ['Relevar actores', 'Mapear dinámicas de poder', 'Detectar patrones', 'Proponer estrategia'],
     'asesoria', ['profesional_independiente'],
     'dinamica, relacion, conflicto, poder, comportamiento'),

    ('decision_estrategica', 'Apoyo en toma de decisiones',
     'Analiza opciones, trade-offs, riesgos. Ayuda a decidir con información completa.',
     'LLM directo (sin tool)',
     ['Presentar opciones', 'Analizar pros/contras', 'Evaluar riesgos', 'Recomendar'],
     'asesoria', ['profesional_independiente', 'pyme'],
     'decision, opciones, riesgo, evaluar, recomendar'),

    # --- ANÁLISIS DE DOCUMENTOS ---
    ('lectura_pliego', 'Lectura y análisis de pliegos',
     'Lee pliegos de licitación, extrae requisitos, identifica excluyentes, arma checklist.',
     'LLM + pdf (pymupdf)',
     ['Leer PDF del pliego', 'Identificar requisitos obligatorios', 'Detectar excluyentes', 'Armar checklist'],
     'analisis', ['tecnico', 'pyme'],
     'pliego, licitacion, requisito, excluyente, checklist'),

    ('lectura_remitos', 'Lectura de remitos escaneados',
     'Lee remitos en PDF/imagen, extrae items, cantidades, compara con pedidos.',
     'LLM + pdf (pymupdf)',
     ['Recibir PDF/imagen escaneado', 'Extraer texto', 'Parsear items', 'Cruzar con pedido', 'Generar tabla'],
     'analisis', ['tecnico', 'pyme'],
     'remito, escaneado, imagen, extraer, cantidad, comparar'),

    # --- DOCUMENTOS ESPECÍFICOS ---
    ('nota_membrete', 'Notas con membrete',
     'Genera notas formales con membrete de empresa.',
     'tools/doc_generator.py',
     ['Cargar template', 'Completar datos', 'Redactar cuerpo', 'Generar PDF'],
     'docs', ['pyme', 'tecnico'],
     'nota, membrete, autorizacion, formal'),

    ('dashboard_visual', 'Dashboard y gráficos',
     'Genera gráficos y dashboards visuales con matplotlib.',
     'matplotlib + seaborn',
     ['Consultar datos de DB', 'Definir métricas', 'Generar gráficos', 'Exportar imagen'],
     'analisis', ['profesional_independiente', 'pyme'],
     'dashboard, grafico, visual, matplotlib, metricas'),

    # --- GESTIÓN OPERATIVA ---
    ('gestion_materiales', 'Gestión de materiales (obra)',
     'Cruza pedidos vs entregas vs remitos. Detecta faltantes.',
     'tools/excel_tools.py + LLM',
     ['Leer pedido original', 'Leer remitos', 'Cruzar cantidades', 'Detectar faltantes', 'Generar Excel'],
     'tracking', ['tecnico'],
     'materiales, pedido, entrega, faltante, cruce, obra'),

    ('cotizacion_proveedores', 'Cotización a proveedores',
     'Redacta pedidos de cotización formales para proveedores.',
     'LLM directo (sin tool)',
     ['Identificar items', 'Redactar pedido formal', 'Incluir specs', 'Solicitar plazo'],
     'comunicacion', ['pyme', 'tecnico'],
     'cotizacion, proveedor, pedido, precio'),

    # --- ORGANIZACIÓN ---
    ('estructura_carpetas', 'Creación de estructura de carpetas',
     'Diseña y crea estructuras de carpetas para proyectos.',
     'LLM + bash/python (os.makedirs)',
     '{"windows": ["Diseñar estructura", "Crear con os.makedirs()", "Verificar en OneDrive"], "mac": ["Diseñar estructura", "Crear con os.makedirs()", "Verificar en iCloud"], "linux": ["Diseñar estructura", "Crear con os.makedirs()"]}',
     'sistema', ['profesional_independiente', 'pyme', 'tecnico'],
     'carpeta, estructura, organizar, onedrive, proyecto'),

    # --- DOCUMENTACIÓN ---
    ('documentacion_producto', 'Documentación de producto',
     'Genera documentos: README, plan negocio, competencia, método, backlog, alcance.',
     'LLM directo (sin tool)',
     ['Relevar estado actual', 'Estructurar documento', 'Redactar markdown', 'Iterar con usuario'],
     'docs', ['profesional_independiente', 'pyme'],
     'documentacion, producto, readme, plan, backlog, alcance'),

    # --- PDF AVANZADO ---
    ('firma_pdf', 'Firma automática en PDFs',
     'Inserta imagen de firma sobre documentos PDF.',
     'pymupdf directo',
     ['Recibir imagen firma', 'Convertir a PNG transparente', 'Insertar en coordenadas', 'Guardar PDF firmado'],
     'docs', ['profesional_independiente', 'pyme', 'tecnico'],
     'firma, pdf, imagen, insertar, automatica'),

    # --- INFORMES ---
    ('informe_gestion', 'Informes de gestión',
     'Genera informes periódicos de avance con métricas y detalle.',
     'LLM + tools/excel_tools.py',
     ['Relevar periodo', 'Consultar eventos', 'Estructurar informe', 'Incluir métricas', 'Generar documento'],
     'docs', ['profesional_independiente', 'pyme', 'tecnico'],
     'informe, gestion, mensual, avance, reporte'),

    # --- INVESTIGACIÓN ---
    ('investigacion_tecnica', 'Investigación técnica',
     'Investiga specs de productos, compara opciones, busca datasheets reales.',
     'LLM + web search',
     ['Identificar producto/tecnología', 'Buscar specs reales', 'Comparar opciones', 'Recomendar con fundamento'],
     'analisis', ['tecnico', 'pyme'],
     'investigar, specs, datasheet, comparar, producto, tecnico'),
]

insertados = 0
for n in nuevas:
    nombre, display, desc, herr, proto, cat, perfiles, kw = n
    try:
        cid = add_capacidad(nombre, display, descripcion=desc, herramienta=herr,
                           protocolo=proto, categoria=cat, perfiles=perfiles, keywords=kw)
        insertados += 1
        print(f'  + {display} [{cat}]')
    except Exception as e:
        print(f'  ! {display}: {e}')

print(f'\nInsertadas: {insertados} capacidades nuevas')

from tools.tracker import get_catalogo
cat = get_catalogo()
print(f'Catalogo total: {len(cat)} capacidades')
for c in cat:
    herr = (c.get('herramienta') or '?')[:35]
    print(f'  [{c["categoria"]:13s}] {c["nombre_display"]:45s} | {herr}')
