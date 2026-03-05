"""
ARGOS Parser de Respuestas Naturales
Interpreta texto libre del usuario y extrae valores numéricos para bienestar.
"dormí 7 horas" → horas_sueno=7
"estoy como el orto" → humor=2
"bien de energía" → energia=7

Reutilizable: funciona en Claude Code (hooks) y en la app web (FastAPI).
"""

import re


# Mapeo de expresiones argentinas/coloquiales a valores numéricos
EXPRESIONES_HUMOR = {
    # Muy malo (1-2)
    'como el orto': 2, 'para el orto': 2, 'horrible': 1, 'pésimo': 1,
    'pesimo': 1, 'de mierda': 1, 'hecho mierda': 1, 'hecho pelota': 2,
    'destruido': 2, 'muy mal': 2, 'fatal': 1, 'bajón': 2, 'bajon': 2,
    'deprimido': 2, 'angustiado': 2,
    # Malo (3-4)
    'mal': 3, 'no muy bien': 4, 'más o menos': 4, 'mas o menos': 4,
    'maso': 4, 'medio pelo': 4, 'regular': 4, 'flojo': 3,
    'cansado': 4, 'agotado': 3, 'sin ganas': 3, 'de buen humor': 7, 'buen humor': 7,
    'medio bajón': 4,
    'medio bajon': 4, 'no estoy bien': 3, 'podría estar mejor': 4,
    'podria estar mejor': 4,
    # Normal (5-6)
    'ahí': 5, 'ahi': 5, 'normal': 5, 'neutro': 5, 'tranquilo': 6,
    'tranqui': 6, 'safando': 5, 'tirando': 5, 'pasable': 5,
    'bien pero cansado': 6, 'ok': 6, 'masomenos': 5,
    # Bien (7-8)
    'bien': 7, 'bastante bien': 8, 'contento': 7, 'piola': 7,
    'joya': 8, 'de diez': 8, 'todo bien': 7, 'muy bien': 8,
    'animado': 7, 'motivado': 8, 'con ganas': 8, 'activo': 7,
    # Muy bien (9-10)
    'excelente': 9, 'espectacular': 9, 'genial': 9, 'bárbaro': 9,
    'barbaro': 9, 'de primera': 9, 'increíble': 10, 'increible': 10,
    'feliz': 9, 'pleno': 10, 'al cien': 10, 'volando': 9,
    'eufórico': 10, 'euforico': 10,
}

EXPRESIONES_ESTRES = {
    # Bajo (1-3)
    'nada': 1, 'cero': 1, 'sin estrés': 1, 'sin estres': 1,
    'relajado': 2, 'tranquilo': 2, 'tranqui': 2, 'sin drama': 2,
    'poco': 3, 'bajo': 3, 'controlado': 3, 'manejable': 3,
    # Medio (4-6)
    'algo': 4, 'un poco': 4, 'moderado': 5, 'normal': 5,
    'medio tenso': 5, 'algo tenso': 5, 'tironeado': 6,
    'bastante': 6, 'varios frentes': 6,
    # Alto (7-8)
    'algo estresado': 4, 'algo tenso': 5, 'un poco estresado': 4,
    'estresado': 7, 'mucho': 7, 'alto': 7, 'bastante alto': 8,
    'tenso': 7, 'presionado': 7, 'contra reloj': 8,
    'desbordado': 8, 'saturado': 8, 'a mil': 8,
    # Muy alto (9-10)
    'al límite': 9, 'al limite': 9, 'reventado': 9,
    'no doy más': 9, 'no doy mas': 9, 'colapso': 10,
    'no puedo más': 10, 'no puedo mas': 10, 'quemado': 9,
    'burnout': 9, 'destruido': 9,
}

EXPRESIONES_ENERGIA = {
    # Baja (1-3)
    'sin energía': 1, 'sin energia': 1, 'muerto': 1, 'destruido': 2,
    'agotado': 2, 'fundido': 2, 'sin pilas': 2, 'muy cansado': 2,
    'cero': 1, 'nada': 1, 'baja': 3, 'poca': 3, 'cansado': 3,
    # Media (4-6)
    'media': 5, 'normal': 5, 'safando': 5, 'ahí': 5, 'ahi': 5,
    'más o menos': 4, 'mas o menos': 4, 'regular': 4,
    'pasable': 5, 'moderada': 5, 'tirando': 5,
    # Alta (7-8)
    'bien': 7, 'alta': 7, 'con energía': 7, 'con energia': 7,
    'pilas': 7, 'activo': 7, 'bastante': 8, 'recargado': 8,
    'muy bien': 8, 'con ganas': 8,
    # Muy alta (9-10)
    'al cien': 10, 'a full': 9, 'volando': 9, 'imparable': 10,
    'a tope': 9, 'excelente': 9, 'máxima': 10, 'maxima': 10,
}


def _extraer_numero(texto, campo):
    """Extrae un número directo del texto para un campo dado."""
    # Patrones: "humor 7", "humor: 7", "humor=7", "7 de humor", "humor 7/10"
    patrones = [
        rf'{campo}\s*[:=]?\s*(\d+(?:\.\d+)?)',
        rf'(\d+(?:\.\d+)?)\s*(?:de\s+)?{campo}',
        rf'{campo}\s+(\d+(?:\.\d+)?)\s*/\s*\d+',
    ]
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            if 0 < val <= 10:
                return val
    return None


def _extraer_horas_sueno(texto):
    """Extrae horas de sueño del texto."""
    patrones = [
        r'dorm[ií]\s*(?:unas?\s+)?(\d+(?:[.,]\d+)?)\s*(?:horas?|hs?)',
        r'(\d+(?:[.,]\d+)?)\s*(?:horas?|hs?)\s*(?:de\s+)?(?:sueño|sueno|dormid)',
        r'(?:sueño|sueno|dormir)\s*[:=]?\s*(\d+(?:[.,]\d+)?)',
        r'(\d+(?:[.,]\d+)?)\s*(?:horas?|hs?)\s*(?:de\s+)?(?:sueño|sueno)',
    ]
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            val = float(match.group(1).replace(',', '.'))
            if 0 < val <= 24:
                return val
    return None


def _extraer_ejercicio(texto):
    """Extrae minutos de ejercicio del texto."""
    # "hice 30 min de ejercicio", "nade 45 minutos", "fui al gym 1 hora"
    patrones = [
        r'(?:hice|entrené|entrenamiento|ejercicio|gym|natación|natacion|nadé|nade|caminé|camine|corrí|corri|bici)\s*(?:de\s+)?(\d+)\s*(?:min|minutos)',
        r'(\d+)\s*(?:min|minutos)\s*(?:de\s+)?(?:ejercicio|gym|natacion|natación|entrenamiento)',
        r'(?:fui al gym|entrené|entrenamiento)\s*(\d+(?:[.,]\d+)?)\s*(?:horas?|hs?)',
        r'(?:nadé|nade|natacion|natación)\s*(\d+)\s*(?:min|minutos)',
    ]
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            val = float(match.group(1).replace(',', '.'))
            # Si parece horas, convertir
            if 'hora' in patron or val <= 5:
                if any(w in texto.lower() for w in ['hora', 'hs']):
                    return int(val * 60)
            return int(val)

    # "sí" / "no" para ejercicio
    if re.search(r'(?:no\s+)?(?:hice\s+)?ejercicio\s*(?:no|tampoco|nada)', texto, re.IGNORECASE):
        return 0
    if re.search(r'(?:sí|si)\s*(?:,?\s*)?(?:hice\s+)?ejercicio', texto, re.IGNORECASE):
        return 30  # asumimos 30 min si dice sí sin especificar

    return None


def _extraer_familia(texto):
    """Extrae atención a familia (1-5)."""
    # Número directo
    val = _extraer_numero(texto, 'familia')
    if val and 1 <= val <= 5:
        return int(val)

    # Expresiones
    if re.search(r'(?:no\s+vi|no\s+hablé|no\s+hable|sin\s+contacto|nada)', texto, re.IGNORECASE):
        return 1
    if re.search(r'(?:poco|casi nada|un rato corto)', texto, re.IGNORECASE):
        return 2
    if re.search(r'(?:normal|como siempre|algo|un rato)', texto, re.IGNORECASE):
        return 3
    if re.search(r'(?:bastante|mucho rato|bien)', texto, re.IGNORECASE):
        return 4
    if re.search(r'(?:todo el día|todo el dia|full|mucho)', texto, re.IGNORECASE):
        return 5

    return None


def _buscar_expresion(texto, expresiones):
    """Busca la expresión más larga que matchee en el texto."""
    texto_lower = texto.lower()
    mejor = None
    mejor_len = 0
    for expr, val in expresiones.items():
        if expr in texto_lower and len(expr) > mejor_len:
            mejor = val
            mejor_len = len(expr)
    return mejor


def parsear_bienestar(texto):
    """
    Parsea texto libre del usuario y extrae valores de bienestar.

    Args:
        texto: string con la respuesta del usuario

    Returns:
        dict con campos extraídos (solo los que pudo parsear):
        {humor, energia, estres, horas_sueno, ejercicio_min, atencion_familia}
        Campos no detectados = None

    Ejemplo:
        parsear_bienestar("dormí 7 horas, estoy bien de humor, algo estresado")
        → {humor: 7, energia: None, estres: 4, horas_sueno: 7.0, ...}
    """
    resultado = {
        'humor': None,
        'energia': None,
        'estres': None,
        'horas_sueno': None,
        'ejercicio_min': None,
        'atencion_familia': None,
    }

    if not texto or not texto.strip():
        return resultado

    # 1. Intentar números directos primero
    for campo, campo_db in [('humor', 'humor'), ('energia', 'energia'),
                             ('energía', 'energia'), ('estres', 'estres'),
                             ('estrés', 'estres')]:
        val = _extraer_numero(texto, campo)
        if val:
            resultado[campo_db] = int(val)

    # 2. Horas de sueño
    resultado['horas_sueno'] = _extraer_horas_sueno(texto)

    # 3. Ejercicio
    resultado['ejercicio_min'] = _extraer_ejercicio(texto)

    # 4. Familia
    resultado['atencion_familia'] = _extraer_familia(texto)

    # 5. Si no encontró número directo, buscar expresiones
    if resultado['humor'] is None:
        resultado['humor'] = _buscar_expresion(texto, EXPRESIONES_HUMOR)

    if resultado['energia'] is None:
        resultado['energia'] = _buscar_expresion(texto, EXPRESIONES_ENERGIA)

    if resultado['estres'] is None:
        resultado['estres'] = _buscar_expresion(texto, EXPRESIONES_ESTRES)

    return resultado


def campos_faltantes(resultado):
    """
    Retorna lista de campos que no se pudieron parsear.
    Útil para saber qué preguntar de nuevo.
    """
    campos = ['humor', 'energia', 'estres', 'horas_sueno']
    return [c for c in campos if resultado.get(c) is None]


def formato_resumen(resultado):
    """Formatea el resultado parseado como texto legible."""
    partes = []
    if resultado.get('humor'):
        partes.append(f"humor={resultado['humor']}/10")
    if resultado.get('energia'):
        partes.append(f"energía={resultado['energia']}/10")
    if resultado.get('estres'):
        partes.append(f"estrés={resultado['estres']}/10")
    if resultado.get('horas_sueno'):
        partes.append(f"sueño={resultado['horas_sueno']}hs")
    if resultado.get('ejercicio_min') is not None:
        partes.append(f"ejercicio={resultado['ejercicio_min']}min")
    if resultado.get('atencion_familia'):
        partes.append(f"familia={resultado['atencion_familia']}/5")
    return ' | '.join(partes) if partes else 'Sin datos parseados'


def clasificar_seguimiento(texto, persona_id=None):
    """
    Clasifica automáticamente un seguimiento por responsable y tipo.
    Analiza el texto y devuelve best guess.

    Returns:
        dict con:
        - responsable: 'yo' | 'otro'
        - tipo: 'tarea' | 'comunicar' | 'cobro' | 'entregar' | 'visita' |
                'investigar' | 'vencimiento' | 'espera' | 'decidir'
        - confianza: 'alta' | 'media' | 'baja'
    """
    t = texto.lower()

    # Patrones de OTRO (tercero tiene la pelota)
    patrones_otro = {
        'espera': [
            'esperar', 'esperando', 'espera de', 'pendiente de',
            'tiene que mandar', 'tiene que enviar', 'debe enviar',
            'debe mandar', 'en manos de',
        ],
        'decidir': [
            'confirmar', 'definir', 'decidir', 'debe crear',
            'debe confirmar', 'debe definir', 'tiene que definir',
            'consultar si', 'pendiente confirmación',
        ],
        'entregar': [
            'tiene que llevar', 'tiene que entregar', 'debe llevar',
            'debe entregar', 'nos envía', 'envía los',
        ],
    }

    # Patrones de YO
    patrones_yo = {
        'cobro': [
            'cobrar', 'facturar', 'recurrente mensual', 'cobro',
            'usd', 'pago', 'remito',
        ],
        'comunicar': [
            'enviar', 'mandar', 'armar mail', 'armar propuesta',
            'reportar', 'avisar', 'escribir a', 'llamar',
            'armar minuta', 'armar cotizacion', 'armar presupuesto',
        ],
        'visita': [
            'visita', 'ir a', 'presencial', 'recorrer',
        ],
        'entregar': [
            'llevar equipos', 'entregar', 'despachar',
        ],
        'investigar': [
            'investigar', 'evaluar', 'analizar', 'diseñar',
            'pipeline', 'algoritmo', 'mejora:', 'curso',
            'testear', 'probar', 'migrar', 'implementar',
        ],
        'vencimiento': [
            'vence', 'vencimiento', 'renovacion', 'contrato',
            'poliza', 'deadline',
        ],
    }

    # Primero: ¿es de otro?
    for tipo, keywords in patrones_otro.items():
        for kw in keywords:
            if kw in t:
                # Si tiene persona_id, más confianza
                conf = 'alta' if persona_id else 'media'
                return {'responsable': 'otro', 'tipo': tipo, 'confianza': conf}

    # Segundo: ¿qué tipo mío es?
    for tipo, keywords in patrones_yo.items():
        for kw in keywords:
            if kw in t:
                return {'responsable': 'yo', 'tipo': tipo, 'confianza': 'media'}

    # Default: tarea mía
    return {'responsable': 'yo', 'tipo': 'tarea', 'confianza': 'baja'}


if __name__ == '__main__':
    # Tests rápidos
    tests = [
        "dormí 7 horas, estoy bien, algo estresado",
        "como el orto, no dormí nada",
        "todo bien, tranqui, sin estrés, dormí 8hs",
        "humor 6, energia 7, estres 3",
        "estoy agotado pero de buen humor",
        "bárbaro, al cien, cero estrés, nadé 45 minutos",
        "más o menos, dormí 5 horas y media",
        "no hice ejercicio, familia todo el día",
    ]

    for t in tests:
        r = parsear_bienestar(t)
        faltantes = campos_faltantes(r)
        print(f"\n>>> {t}")
        print(f"    {formato_resumen(r)}")
        if faltantes:
            print(f"    Faltantes: {', '.join(faltantes)}")
