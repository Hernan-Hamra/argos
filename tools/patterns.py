"""
ARGOS Patterns - Motor de detección automática de patrones v3
Catálogo DINÁMICO de capacidades (herramienta + protocolo) en DB.

Cada pedido a ARGOS tiene:
  - HERRAMIENTA: tool/función/script usado
  - PROTOCOLO: pasos/método seguido (puede variar por plataforma)

El motor detecta:
  1. Funcionalidades NUEVAS vs las existentes en el catálogo
  2. MEJORAS a funcionalidades existentes
  3. Patrones de COMPORTAMIENTO del usuario
  4. Capacidades DORMIDAS o no usadas
"""

import sqlite3
import os
import json
import platform
from datetime import datetime, date, timedelta
from collections import Counter, defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'argos_tracker.db')
TOOLS_PATH = os.path.join(os.path.dirname(__file__))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _plataforma_actual():
    """Detectar plataforma del usuario."""
    sistema = platform.system().lower()
    if sistema == 'windows':
        return 'windows'
    elif sistema == 'darwin':
        return 'mac'
    else:
        return 'linux'


# =========================================================
# CATÁLOGO DINÁMICO — lee de tabla `capacidades` en DB
# =========================================================

# Catálogo estático de fallback (se usa SOLO si la tabla capacidades está vacía)
# Una vez migrado a DB, este dict ya no se consulta.
CATALOGO_SEMILLA = {
    'generacion_docs': {
        'nombre': 'Generación de documentos',
        'herramienta': 'tools/doc_generator.py',
        'protocolo': ['Cargar template .docx', 'Reemplazar placeholders en runs', 'Generar PDF via COM'],
        'categoria': 'docs',
        'keywords': 'docx, word, documento, ddjj, nota, membrete, caratula, cv',
        'perfiles': ['pyme', 'tecnico', 'profesional_independiente'],
    },
    'foliacion_pdf': {
        'nombre': 'Foliación de PDFs',
        'herramienta': 'tools/foliador.py',
        'protocolo': ['Merge PDFs por carpeta', 'Agregar overlay "Folio: N"', 'Numeración continua'],
        'categoria': 'docs',
        'keywords': 'foliar, foliacion, folio, merge pdf, folios',
        'perfiles': ['tecnico'],
    },
    'analisis_precios': {
        'nombre': 'Análisis de precios',
        'herramienta': 'tools/cotizacion.py',
        'protocolo': ['Leer estructura de costos', 'Calcular IVA mix 21/10.5', 'Álgebra inversa desde total', 'Generar Excel'],
        'categoria': 'analisis',
        'keywords': 'iva, cotizacion, precio, presupuesto, anexo vii, costos',
        'perfiles': ['pyme', 'tecnico'],
    },
    'excel': {
        'nombre': 'Herramientas Excel',
        'herramienta': 'tools/excel_tools.py',
        'protocolo': ['Leer con openpyxl', 'Cruce de datos', 'Escribir con formato/color'],
        'categoria': 'analisis',
        'keywords': 'excel, openpyxl, planilla, hoja, spreadsheet',
        'perfiles': ['pyme', 'tecnico'],
    },
    'extraccion_datos': {
        'nombre': 'Extracción de datos',
        'herramienta': 'tools/pdf_converter.py + pymupdf',
        'protocolo': ['Extraer texto de PDF', 'Parsear estructura', 'Normalizar datos'],
        'categoria': 'analisis',
        'keywords': 'extraer, parsear, remito, escaneado, ocr, whatsapp',
        'perfiles': ['pyme', 'tecnico'],
    },
    'redaccion': {
        'nombre': 'Redacción calibrada',
        'herramienta': 'LLM directo (sin tool)',
        'protocolo': ['Analizar contexto y relación', 'Calibrar tono', 'Generar versiones', 'Confirmar con usuario'],
        'categoria': 'comunicacion',
        'keywords': 'redaccion, email, whatsapp, tono, versiones, carta',
        'perfiles': ['profesional_independiente', 'pyme'],
    },
    'estrategia': {
        'nombre': 'Elaboración de estrategias',
        'herramienta': 'LLM directo (sin tool)',
        'protocolo': ['Mapear actores y dinámicas', 'Analizar posiciones', 'Proponer acciones', 'Evaluar riesgos'],
        'categoria': 'asesoria',
        'keywords': 'estrategia, analisis, dinamica, reclamo, negociacion',
        'perfiles': ['profesional_independiente'],
    },
    'tracking': {
        'nombre': 'Tracking y seguimiento',
        'herramienta': 'tools/tracker.py',
        'protocolo': ['Registrar evento en DB', 'Clasificar por tipo/subtipo', 'Vincular a proyecto/persona'],
        'categoria': 'tracking',
        'keywords': 'seguimiento, pendiente, tracking, evento, registrar',
        'perfiles': ['profesional_independiente', 'pyme', 'familia', 'salud'],
    },
    'agenda': {
        'nombre': 'Agenda y calendario',
        'herramienta': 'tools/tracker.py::add_agenda',
        'protocolo': ['Registrar evento futuro', 'Calcular recordatorios', 'Alertar al inicio de sesión'],
        'categoria': 'tracking',
        'keywords': 'agenda, turno, deadline, recordatorio, calendario',
        'perfiles': ['profesional_independiente', 'pyme', 'familia', 'salud'],
    },
    'planificacion_crosslife': {
        'nombre': 'Planificación cross-life',
        'herramienta': 'LLM + tracker.py',
        'protocolo': ['Relevar áreas de vida', 'Asignar horas disponibles', 'Cruzar trabajo+salud+familia+desarrollo'],
        'categoria': 'asesoria',
        'keywords': 'cronograma, cross-life, balance, semana a semana, horas disponibles',
        'perfiles': ['profesional_independiente'],
    },
    'nutricion': {
        'nombre': 'Seguimiento nutricional',
        'herramienta': 'tools/tracker.py::registrar_comida',
        'protocolo': ['Registrar comida del día', 'Evaluar adherencia al plan', 'Reportes diarios/semanales'],
        'categoria': 'salud',
        'keywords': 'nutricion, comida, proteina, dieta, plan nutricional',
        'perfiles': ['salud', 'familia'],
    },
    'onboarding_proyecto': {
        'nombre': 'Onboarding de proyectos',
        'herramienta': 'tools/tracker.py::add_proyecto',
        'protocolo': ['Relevar proyecto existente', 'Crear en DB', 'Vincular personas y seguimiento'],
        'categoria': 'tracking',
        'keywords': 'onboarding, incorporar proyecto, sincronizar, nuevo proyecto',
        'perfiles': ['profesional_independiente', 'pyme'],
    },
    'backup': {
        'nombre': 'Backup automático',
        'herramienta': 'tools/backup.py',
        'protocolo': ['Copiar DB a OneDrive', 'Rotación de backups', 'Verificar integridad'],
        'categoria': 'sistema',
        'keywords': 'backup, respaldo, copia',
        'perfiles': ['profesional_independiente', 'pyme', 'tecnico'],
    },
    'pdf_overlay': {
        'nombre': 'PDF overlay (formularios)',
        'herramienta': 'pymupdf directo',
        'protocolo': ['Leer PDF base', 'Insertar texto en coordenadas', 'Guardar con overlay'],
        'categoria': 'docs',
        'keywords': 'overlay, pymupdf, anexo, formulario pdf, firma',
        'perfiles': ['tecnico'],
    },
    'bot_telegram': {
        'nombre': 'Bot Telegram',
        'herramienta': 'tools/telegram_bot.py',
        'protocolo': ['Recibir mensaje texto/audio', 'Procesar con LLM', 'Responder texto + TTS'],
        'categoria': 'comunicacion',
        'keywords': 'telegram, bot, stt, tts, audio',
        'perfiles': ['profesional_independiente'],
    },
}


def migrar_catalogo_a_db():
    """Migrar el catálogo estático CATALOGO_SEMILLA a la tabla capacidades.
    Solo inserta las que no existen. Idempotente.
    """
    from tools.tracker import add_capacidad, get_catalogo
    existentes = {c['nombre'] for c in get_catalogo(solo_activas=False)}

    insertados = 0
    for nombre, info in CATALOGO_SEMILLA.items():
        if nombre not in existentes:
            add_capacidad(
                nombre=nombre,
                nombre_display=info['nombre'],
                descripcion=info.get('descripcion', info['nombre']),
                herramienta=info.get('herramienta'),
                protocolo=info.get('protocolo'),
                categoria=info.get('categoria'),
                origen='sistema',
                es_generalizable=1,
                perfiles=info.get('perfiles'),
                keywords=info.get('keywords'),
            )
            insertados += 1
    return insertados


def get_catalogo_activo():
    """Obtener catálogo desde DB. Si está vacío, migrar semilla."""
    from tools.tracker import get_catalogo
    catalogo = get_catalogo(solo_activas=True)
    if not catalogo:
        migrar_catalogo_a_db()
        catalogo = get_catalogo(solo_activas=True)
    return catalogo


# =========================================================
# DETECCIÓN DE FUNCIONALIDADES NUEVAS vs EXISTENTES
# =========================================================

def detectar_si_es_nueva(descripcion_pedido, herramienta_usada=None):
    """Dado un pedido del usuario, determinar si es una funcionalidad NUEVA,
    una MEJORA a una existente, o algo YA CONOCIDO.

    Retorna dict:
      tipo: 'nueva' | 'mejora' | 'conocida'
      capacidad_match: nombre de la capacidad más cercana (si aplica)
      confianza: 0.0-1.0
      sugerencia: texto explicativo
    """
    catalogo = get_catalogo_activo()
    desc_lower = descripcion_pedido.lower()

    # Buscar match en catálogo por keywords
    mejor_match = None
    mejor_score = 0

    for cap in catalogo:
        score = 0
        keywords = (cap.get('keywords') or '').lower().split(',')
        keywords = [k.strip() for k in keywords if k.strip()]

        for kw in keywords:
            if kw in desc_lower:
                score += 1

        # Match por herramienta
        if herramienta_usada and cap.get('herramienta'):
            if herramienta_usada.lower() in cap['herramienta'].lower():
                score += 2

        # Match por nombre
        nombre = (cap.get('nombre_display') or '').lower()
        if any(word in desc_lower for word in nombre.split() if len(word) > 3):
            score += 1

        if score > mejor_score:
            mejor_score = score
            mejor_match = cap

    if mejor_score == 0:
        return {
            'tipo': 'nueva',
            'capacidad_match': None,
            'confianza': 0.8,
            'sugerencia': f'Funcionalidad nueva detectada: "{descripcion_pedido}". No coincide con ninguna capacidad existente.'
        }
    elif mejor_score <= 1:
        return {
            'tipo': 'mejora',
            'capacidad_match': mejor_match['nombre'],
            'confianza': 0.5,
            'sugerencia': f'Posible variante/mejora de "{mejor_match["nombre_display"]}". Evaluar si amerita nueva versión.'
        }
    else:
        return {
            'tipo': 'conocida',
            'capacidad_match': mejor_match['nombre'],
            'confianza': min(mejor_score / 5, 0.95),
            'sugerencia': f'Coincide con "{mejor_match["nombre_display"]}" (v{mejor_match.get("version", 1)}, usada {mejor_match.get("veces_usada", 0)}x).'
        }


def registrar_interaccion(descripcion_pedido, herramienta_usada=None, protocolo_seguido=None,
                          resultado='ok', categoria=None, perfiles=None, plataforma=None):
    """Registrar una interacción completa y evaluar si es nueva.
    Esta es LA FUNCIÓN PRINCIPAL que se llama al cierre de cada pedido exitoso.

    Flujo:
    1. Detectar si es nueva vs conocida vs mejora
    2. Si es nueva → crear capacidad en catálogo
    3. Si es conocida → incrementar uso
    4. Si es mejora → registrar mejora con protocolo actualizado
    5. Retornar resultado de la evaluación

    plataforma: 'windows', 'mac', 'linux' o None (auto-detectar)
    """
    from tools.tracker import add_capacidad, usar_capacidad, mejorar_capacidad

    if plataforma is None:
        plataforma = _plataforma_actual()

    evaluacion = detectar_si_es_nueva(descripcion_pedido, herramienta_usada)

    if evaluacion['tipo'] == 'nueva' and resultado == 'ok':
        # Generar nombre automático
        nombre_auto = descripcion_pedido.lower()[:50].replace(' ', '_').replace(',', '')
        nombre_auto = ''.join(c for c in nombre_auto if c.isalnum() or c == '_')

        # Empaquetar protocolo con plataforma
        proto = protocolo_seguido
        if proto and plataforma:
            if isinstance(proto, list):
                proto = {plataforma: proto, 'general': proto}
            elif isinstance(proto, str):
                proto = {plataforma: proto, 'general': proto}

        try:
            cid = add_capacidad(
                nombre=nombre_auto,
                nombre_display=descripcion_pedido[:100],
                descripcion=descripcion_pedido,
                herramienta=herramienta_usada,
                protocolo=proto,
                categoria=categoria,
                origen='usuario',
                es_generalizable=1,
                perfiles=perfiles,
                keywords=None,
            )
            evaluacion['accion'] = 'creada'
            evaluacion['capacidad_id'] = cid
        except Exception as e:
            evaluacion['accion'] = 'error'
            evaluacion['error'] = str(e)

    elif evaluacion['tipo'] == 'conocida':
        usar_capacidad(evaluacion['capacidad_match'])
        evaluacion['accion'] = 'uso_registrado'

    elif evaluacion['tipo'] == 'mejora' and resultado == 'ok':
        # Buscar capacidad existente para mejorar
        from tools.tracker import get_capacidad_por_nombre
        cap_existente = get_capacidad_por_nombre(evaluacion['capacidad_match'])
        if cap_existente:
            # Empaquetar protocolo con plataforma
            proto = protocolo_seguido
            if proto and plataforma:
                # Leer protocolo actual y agregar variante de plataforma
                proto_actual = cap_existente.get('protocolo')
                try:
                    proto_actual = json.loads(proto_actual) if proto_actual else {}
                except (json.JSONDecodeError, TypeError):
                    proto_actual = {'general': proto_actual}

                if isinstance(proto_actual, dict):
                    proto_actual[plataforma] = proto if isinstance(proto, str) else json.dumps(proto, ensure_ascii=False)
                    proto = proto_actual
                else:
                    proto = {plataforma: proto, 'general': proto_actual}

            new_id = mejorar_capacidad(
                cap_existente['id'],
                nuevo_protocolo=proto,
                nueva_herramienta=herramienta_usada,
                notas_mejora=f'Mejorada desde interacción: {descripcion_pedido[:80]}'
            )
            evaluacion['accion'] = 'mejorada'
            evaluacion['nueva_version_id'] = new_id
        else:
            usar_capacidad(evaluacion['capacidad_match'])
            evaluacion['accion'] = 'uso_registrado'

    return evaluacion


# =========================================================
# FUNCIONES DE INSERCIÓN / ACTUALIZACIÓN DE PATRONES
# =========================================================

def add_patron(tipo, categoria, descripcion, evidencia=None, sugerencia=None,
               confianza=0.5, notas=None):
    """Registrar un patrón detectado.
    tipo: general, perfil, personal
    """
    conn = get_connection()
    c = conn.cursor()
    hoy = date.today().isoformat()
    ev_json = json.dumps(evidencia, ensure_ascii=False) if evidencia else None
    c.execute('''INSERT INTO patrones (fecha_deteccion, tipo, categoria, descripcion,
                 evidencia, confianza, sugerencia, ultimo_visto, notas)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (hoy, tipo, categoria, descripcion, ev_json, confianza, sugerencia, hoy, notas))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid


def reforzar_patron(patron_id):
    """Incrementar frecuencia de un patrón existente."""
    conn = get_connection()
    c = conn.cursor()
    hoy = date.today().isoformat()
    c.execute('''UPDATE patrones SET frecuencia = frecuencia + 1,
                 ultimo_visto = ?, updated_at = datetime('now','localtime')
                 WHERE id = ?''', (hoy, patron_id))
    conn.commit()
    conn.close()


def validar_patron(patron_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE patrones SET estado = 'validado',
                 updated_at = datetime('now','localtime')
                 WHERE id = ?''', (patron_id,))
    conn.commit()
    conn.close()


def descartar_patron(patron_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE patrones SET estado = 'descartado',
                 updated_at = datetime('now','localtime')
                 WHERE id = ?''', (patron_id,))
    conn.commit()
    conn.close()


# =========================================================
# FUNCIONES DE CONSULTA DE PATRONES (lee de ambas DBs)
# =========================================================

def get_patrones_activos():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM patrones
                 WHERE estado IN ('detectado', 'validado', 'aplicado')
                 ORDER BY frecuencia DESC, confianza DESC''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_sugerencias():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM patrones
                 WHERE estado = 'validado' AND sugerencia IS NOT NULL
                 AND frecuencia >= 3
                 ORDER BY frecuencia DESC, confianza DESC
                 LIMIT 5''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# =========================================================
# DETECCIÓN DE CAPACIDADES (lee del catálogo dinámico)
# =========================================================

def detectar_capacidades_usadas():
    """Escanear eventos (usuario) y cruzar con catálogo (sistema)."""
    catalogo = get_catalogo_activo()

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT fecha, subtipo, descripcion FROM eventos ORDER BY fecha ASC')
    eventos = [dict(r) for r in c.fetchall()]
    conn.close()

    uso = {}
    for cap in catalogo:
        keywords = [k.strip().lower() for k in (cap.get('keywords') or '').split(',') if k.strip()]
        if not keywords:
            continue

        matches = []
        for ev in eventos:
            desc = (ev['descripcion'] or '').lower()
            if any(kw in desc for kw in keywords):
                matches.append(ev['fecha'])

        if matches:
            uso[cap['nombre']] = {
                'usos': len(matches),
                'primera_vez': matches[0],
                'ultimo_uso': matches[-1],
                'nombre': cap['nombre_display'],
                'herramienta': cap.get('herramienta'),
                'categoria': cap.get('categoria'),
            }

    return uso


def detectar_capacidades_nuevas():
    """Capacidades usadas por primera vez en los últimos 7 días."""
    uso = detectar_capacidades_usadas()
    hace_7_dias = (date.today() - timedelta(days=7)).isoformat()
    return [
        {**info, 'capacidad': cap_id}
        for cap_id, info in uso.items()
        if info['primera_vez'] >= hace_7_dias
    ]


def detectar_capacidades_no_usadas():
    """Capacidades del catálogo que nunca se usaron."""
    uso = detectar_capacidades_usadas()
    catalogo = get_catalogo_activo()
    return [
        {'capacidad': c['nombre'], 'nombre': c['nombre_display'],
         'descripcion': c.get('descripcion', ''), 'herramienta': c.get('herramienta')}
        for c in catalogo if c['nombre'] not in uso
    ]


def detectar_capacidades_dormidas():
    """Capacidades usadas antes pero no en los últimos 30 días."""
    uso = detectar_capacidades_usadas()
    hace_30_dias = (date.today() - timedelta(days=30)).isoformat()
    return [
        {**info, 'capacidad': cap_id}
        for cap_id, info in uso.items()
        if info['ultimo_uso'] < hace_30_dias and info['usos'] >= 2
    ]


def detectar_herramientas_nuevas():
    """Escanear tools/ para detectar archivos .py nuevos o modificados."""
    herramientas = []
    for f in os.listdir(TOOLS_PATH):
        if f.endswith('.py') and not f.startswith('__'):
            filepath = os.path.join(TOOLS_PATH, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            herramientas.append({
                'archivo': f,
                'modificado': mtime.isoformat(),
                'tamano': os.path.getsize(filepath),
                'dias_desde_modif': (datetime.now() - mtime).days,
            })
    recientes = [h for h in herramientas if h['dias_desde_modif'] <= 7]
    return {'todas': herramientas, 'recientes': recientes}


# =========================================================
# PERFILES DE USUARIO (para recomendaciones)
# =========================================================

PERFILES_USUARIO = {
    'profesional_independiente': ['tracking', 'agenda', 'redaccion', 'estrategia', 'planificacion_crosslife'],
    'pyme': ['tracking', 'agenda', 'generacion_docs', 'analisis_precios', 'excel', 'redaccion'],
    'familia': ['nutricion', 'agenda', 'tracking'],
    'salud': ['nutricion', 'agenda', 'tracking'],
    'tecnico': ['generacion_docs', 'foliacion_pdf', 'excel', 'extraccion_datos', 'pdf_overlay'],
}


def sugerir_funciones_para_perfil(perfil):
    """Recomendar funciones no usadas para un perfil dado."""
    if perfil not in PERFILES_USUARIO:
        return []

    caps_perfil = PERFILES_USUARIO[perfil]
    uso = detectar_capacidades_usadas()
    catalogo = get_catalogo_activo()

    # Mapear nombre → capacidad
    catalogo_map = {c['nombre']: c for c in catalogo}

    recomendaciones = []
    for cap_id in caps_perfil:
        if cap_id not in uso and cap_id in catalogo_map:
            cap = catalogo_map[cap_id]
            recomendaciones.append({
                'capacidad': cap_id,
                'nombre': cap['nombre_display'],
                'herramienta': cap.get('herramienta'),
                'descripcion': cap.get('descripcion', ''),
                'razon': f'Recomendada para perfil "{perfil}"',
            })

    # También buscar capacidades con perfiles en DB
    for cap in catalogo:
        if cap['nombre'] in uso or cap['nombre'] in caps_perfil:
            continue
        perfiles_cap = cap.get('perfiles')
        if perfiles_cap:
            try:
                perfiles_list = json.loads(perfiles_cap) if isinstance(perfiles_cap, str) else perfiles_cap
            except (json.JSONDecodeError, TypeError):
                perfiles_list = []
            if perfil in perfiles_list:
                recomendaciones.append({
                    'capacidad': cap['nombre'],
                    'nombre': cap['nombre_display'],
                    'herramienta': cap.get('herramienta'),
                    'descripcion': cap.get('descripcion', ''),
                    'razon': f'Marcada para perfil "{perfil}" en catálogo',
                })

    return recomendaciones


# =========================================================
# PATRONES DE COMPORTAMIENTO
# =========================================================

def detectar_patrones_horario():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT hora, COUNT(*) as total FROM eventos
                 WHERE hora IS NOT NULL AND duracion_min > 0
                 GROUP BY hora ORDER BY total DESC''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if not rows:
        return None

    franjas = {'manana': 0, 'tarde': 0, 'noche': 0}
    for r in rows:
        try:
            hora = int(r['hora'].split(':')[0])
        except (ValueError, AttributeError):
            continue
        if 6 <= hora < 12:
            franjas['manana'] += r['total']
        elif 12 <= hora < 19:
            franjas['tarde'] += r['total']
        else:
            franjas['noche'] += r['total']

    total = sum(franjas.values())
    if total < 5:
        return None

    franja_top = max(franjas, key=franjas.get)
    pct = round(franjas[franja_top] / total * 100)
    if pct >= 60:
        nombres = {'manana': 'por la mañana', 'tarde': 'por la tarde', 'noche': 'por la noche'}
        return {
            'categoria': 'timing',
            'descripcion': f'Trabaja principalmente {nombres[franja_top]} ({pct}%)',
            'sugerencia': f'Trabajas mas {nombres[franja_top]}. Agendamos tareas importantes en esa franja?',
            'confianza': min(pct / 100, 0.95)
        }
    return None


def detectar_patrones_proyecto():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT p.nombre, SUM(e.duracion_min) as total_min, COUNT(*) as sesiones
                 FROM eventos e JOIN proyectos p ON e.proyecto_id = p.id
                 WHERE e.duracion_min > 0
                 GROUP BY p.nombre ORDER BY total_min DESC''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if len(rows) < 2:
        return None

    total_min = sum(r['total_min'] for r in rows)
    top = rows[0]
    pct = round(top['total_min'] / total_min * 100)
    if pct >= 50:
        return {
            'categoria': 'workflow',
            'descripcion': f'"{top["nombre"]}" consume {pct}% del tiempo ({top["sesiones"]} sesiones)',
            'sugerencia': f'"{top["nombre"]}" domina tu agenda ({pct}%). Queres balancear?',
            'confianza': 0.7
        }
    return None


def detectar_patrones_pendientes():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT s.accion, p.nombre as proyecto FROM seguimiento s
                 LEFT JOIN proyectos p ON s.proyecto_id = p.id
                 WHERE s.estado = 'vencido' ORDER BY s.fecha_limite DESC''')
    vencidos = [dict(r) for r in c.fetchall()]
    conn.close()

    if len(vencidos) < 2:
        return None

    por_proyecto = Counter(r['proyecto'] or 'sin proyecto' for r in vencidos)
    top_proyecto, count = por_proyecto.most_common(1)[0]
    if count >= 2:
        return {
            'categoria': 'workflow',
            'descripcion': f'"{top_proyecto}" tiene {count} pendientes vencidos',
            'sugerencia': f'Tenes {count} pendientes vencidos en "{top_proyecto}". Los revisamos?',
            'confianza': 0.8
        }
    return None


# =========================================================
# FUNCIÓN PRINCIPAL — ejecutar todo el análisis
# =========================================================

def analizar_patrones():
    """Ejecutar todos los detectores y registrar patrones nuevos."""
    existentes = get_patrones_activos()
    desc_existentes = {p['descripcion'][:30].lower(): p for p in existentes}

    nuevos = []
    reforzados = []

    # --- CATÁLOGO DINÁMICO ---
    catalogo = get_catalogo_activo()
    capacidades_usadas = detectar_capacidades_usadas()
    capacidades_nuevas = detectar_capacidades_nuevas()
    capacidades_no_usadas = detectar_capacidades_no_usadas()
    capacidades_dormidas = detectar_capacidades_dormidas()
    herramientas = detectar_herramientas_nuevas()

    # Registrar capacidades nuevas como patrones
    for cap in capacidades_nuevas:
        desc = f'Nueva capacidad: {cap["nombre"]} (desde {cap["primera_vez"]})'
        key = desc[:30].lower()
        if key not in desc_existentes:
            pid = add_patron(
                tipo='general', categoria='capacidad',
                descripcion=desc,
                evidencia={'capacidad': cap['capacidad'], 'usos': cap['usos'],
                           'herramienta': cap.get('herramienta')},
                confianza=0.7,
                notas=f'Herramienta: {cap.get("herramienta")} | Cat: {cap.get("categoria")}'
            )
            nuevos.append({'id': pid, 'categoria': 'capacidad', 'descripcion': desc})

    # Registrar herramientas modificadas
    for h in herramientas['recientes']:
        desc = f'Herramienta actualizada: {h["archivo"]} ({h["dias_desde_modif"]}d atras)'
        key = desc[:30].lower()
        if key not in desc_existentes:
            pid = add_patron(
                tipo='general', categoria='herramienta',
                descripcion=desc,
                evidencia={'archivo': h['archivo'], 'tamano': h['tamano']},
                confianza=0.8
            )
            nuevos.append({'id': pid, 'categoria': 'herramienta', 'descripcion': desc})

    # Registrar recomendaciones para no usadas
    for cap in capacidades_no_usadas[:5]:  # limitar a 5
        desc = f'Capacidad disponible no usada: {cap["nombre"]}'
        key = desc[:30].lower()
        if key not in desc_existentes:
            pid = add_patron(
                tipo='general', categoria='recomendacion',
                descripcion=desc,
                sugerencia=f'Nunca usaste "{cap["nombre"]}": {cap.get("descripcion", "")}. Herramienta: {cap.get("herramienta")}',
                confianza=0.4
            )
            nuevos.append({'id': pid, 'categoria': 'recomendacion', 'descripcion': desc})

    # Registrar dormidas
    for cap in capacidades_dormidas:
        desc = f'Capacidad dormida: {cap["nombre"]} (ultima vez: {cap["ultimo_uso"]})'
        key = desc[:30].lower()
        if key not in desc_existentes:
            pid = add_patron(
                tipo='personal', categoria='recomendacion',
                descripcion=desc,
                sugerencia=f'Hace rato no usas "{cap["nombre"]}". Herramienta: {cap.get("herramienta")}',
                confianza=0.5
            )
            nuevos.append({'id': pid, 'categoria': 'recomendacion', 'descripcion': desc})

    # --- COMPORTAMIENTO ---
    for detector in [detectar_patrones_horario, detectar_patrones_proyecto, detectar_patrones_pendientes]:
        try:
            resultado = detector()
        except Exception:
            continue
        if resultado is None:
            continue

        desc = resultado['descripcion']
        key = desc[:30].lower()
        if key in desc_existentes:
            p = desc_existentes[key]
            reforzar_patron(p['id'])
            reforzados.append(p)
            if p['frecuencia'] + 1 >= 3 and p['estado'] == 'detectado':
                validar_patron(p['id'])
        else:
            pid = add_patron(
                tipo='personal', categoria=resultado['categoria'],
                descripcion=desc, sugerencia=resultado.get('sugerencia'),
                confianza=resultado.get('confianza', 0.5)
            )
            nuevos.append({'id': pid, 'categoria': resultado['categoria'], 'descripcion': desc})

    return {
        'nuevos': nuevos,
        'reforzados': reforzados,
        'catalogo_total': len(catalogo),
        'capacidades_usadas': len(capacidades_usadas),
        'capacidades_nuevas': capacidades_nuevas,
        'capacidades_no_usadas': capacidades_no_usadas,
        'capacidades_dormidas': capacidades_dormidas,
        'herramientas_recientes': herramientas['recientes'],
        'total_activos': len(existentes) + len(nuevos),
    }


# =========================================================
# REPORTE — para mostrar al inicio de sesión
# =========================================================

def reporte_patrones():
    """Generar reporte legible para el inicio de sesión."""
    resultado = analizar_patrones()
    sugerencias = get_sugerencias()

    lines = []
    lines.append("=" * 60)
    lines.append("  ARGOS AUTO-APRENDIZAJE v3 — Catálogo dinámico")
    lines.append("=" * 60)

    # Catálogo
    usadas = resultado['capacidades_usadas']
    total = resultado['catalogo_total']
    lines.append(f"\n  CATÁLOGO: {total} capacidades registradas, {usadas} en uso")
    lines.append(f"  Plataforma: {_plataforma_actual()}")

    if resultado['capacidades_nuevas']:
        lines.append(f"\n  NUEVAS CAPACIDADES (últimos 7 días):")
        for cap in resultado['capacidades_nuevas']:
            tool = cap.get('herramienta', '?')
            lines.append(f"    + {cap['nombre']} [{tool}] (desde {cap['primera_vez']}, {cap['usos']} usos)")

    if resultado['herramientas_recientes']:
        lines.append(f"\n  HERRAMIENTAS ACTUALIZADAS:")
        for h in resultado['herramientas_recientes']:
            lines.append(f"    * {h['archivo']} (hace {h['dias_desde_modif']}d)")

    if resultado['capacidades_dormidas']:
        lines.append(f"\n  CAPACIDADES DORMIDAS (>30 días):")
        for cap in resultado['capacidades_dormidas']:
            lines.append(f"    ~ {cap['nombre']} (último: {cap['ultimo_uso']})")

    if resultado['capacidades_no_usadas']:
        lines.append(f"\n  DISPONIBLES (nunca usadas):")
        for cap in resultado['capacidades_no_usadas'][:3]:
            lines.append(f"    ? {cap['nombre']}: {cap.get('herramienta', '?')}")

    if resultado['reforzados']:
        lines.append(f"\n  PATRONES REFORZADOS:")
        for p in resultado['reforzados']:
            lines.append(f"    [{p['categoria']}] {p['descripcion']} (x{p['frecuencia']+1})")

    if sugerencias:
        lines.append(f"\n  SUGERENCIAS:")
        for s in sugerencias:
            lines.append(f"    > {s['sugerencia']}")

    lines.append(f"\n  Total patrones: {resultado['total_activos']}")
    lines.append("=" * 60)

    output = "\n".join(lines)
    print(output)
    return output


# =========================================================
# EXPORTAR / IMPORTAR (multi-usuario futuro)
# =========================================================

def exportar_patrones_anonimos():
    """Exportar patrones generales (sin datos personales). DB SISTEMA."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT categoria, descripcion, frecuencia, confianza, sugerencia
                 FROM patrones
                 WHERE tipo IN ('general', 'perfil') AND estado = 'validado' AND frecuencia >= 3''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def exportar_capacidades_anonimas():
    """Exportar capacidades generalizables (proceso sin data).
    Esto es lo que se comparte entre usuarios: HERRAMIENTA + PROTOCOLO.
    """
    catalogo = get_catalogo_activo()
    exportables = []
    for cap in catalogo:
        if not cap.get('es_generalizable'):
            continue
        exportables.append({
            'nombre': cap['nombre'],
            'nombre_display': cap['nombre_display'],
            'descripcion': cap.get('descripcion'),
            'herramienta': cap.get('herramienta'),
            'protocolo': cap.get('protocolo'),  # el proceso, sin data
            'categoria': cap.get('categoria'),
            'perfiles': cap.get('perfiles'),
            'veces_usada': cap.get('veces_usada', 0),
        })
    return exportables


def importar_capacidad_comunitaria(nombre, nombre_display, herramienta, protocolo,
                                    categoria=None, perfiles=None):
    """Importar una capacidad compartida por la comunidad."""
    from tools.tracker import add_capacidad
    return add_capacidad(
        nombre=f'comunidad_{nombre}',
        nombre_display=f'[Comunidad] {nombre_display}',
        herramienta=herramienta,
        protocolo=protocolo,
        categoria=categoria,
        origen='comunidad',
        perfiles=perfiles,
        notas='Importada de la comunidad ARGOS'
    )


# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    reporte_patrones()
