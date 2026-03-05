"""
ARGOS Orquestador de Sesión
Fuerza el flujo de apertura/cierre por CÓDIGO, no por memoria del LLM.

Flujo:
  apertura() → muestra nudges + coherencia + agenda + pendientes vencidos
             → fuerza checkpoint apertura → registra bienestar
  cierre()   → fuerza checkpoint cierre → actualiza bienestar
             → resumen diario → backup

Reutilizable: funciona en Claude Code (hoy) y en la app web (mañana).

Uso desde Claude Code:
    from tools.orquestador_sesion import apertura, cierre, estado_sesion
    resultado = apertura()   # retorna dict con todo para mostrar al usuario
    resultado = cierre(respuestas_cierre="estuvo bien, algo cansado")

Uso desde FastAPI (futuro):
    @app.post("/session/open")
    def open_session():
        return apertura()
"""

import os
import sys
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tracker import (
    get_connection, get_checkpoints, get_resumen_ayer, get_pendientes,
    get_agenda_dia, add_bienestar, add_evento, resumen_diario, init_db,
    get_rutinas_pendientes, get_pendientes_agrupados, get_status_proyectos
)
from tools.session import abrir_sesion, cerrar_sesion, get_sesion_abierta
from tools.proactivo import generar_nudges
from tools.coherencia import reporte_coherencia
from tools.parsear_respuesta import parsear_bienestar, campos_faltantes, formato_resumen
from tools.aprendizaje import aprender_de_sesion
from tools.alertas import generar_alertas
from tools.email_reader import resumen_inbox, email_configurado


def _pendientes_vencidos():
    """Obtiene seguimientos vencidos con detalle."""
    hoy = date.today().isoformat()
    pendientes = get_pendientes(incluir_vencidos=True)
    vencidos = []
    urgentes = []
    for p in pendientes:
        p = dict(p)
        if p.get('fecha_limite') and p['fecha_limite'] < hoy:
            dias = (date.today() - datetime.strptime(p['fecha_limite'], '%Y-%m-%d').date()).days
            p['dias_vencido'] = dias
            vencidos.append(p)
        elif p.get('prioridad') in ('critica', 'alta'):
            urgentes.append(p)
    return vencidos, urgentes


def _bienestar_ya_registrado_hoy():
    """Verifica si ya hay registro de bienestar para hoy."""
    conn = get_connection()
    hoy = date.today().isoformat()
    row = conn.execute("SELECT * FROM bienestar WHERE fecha=?", (hoy,)).fetchone()
    conn.close()
    return dict(row) if row else None


def apertura(proyecto_id=None, notas=None):
    """
    Ejecuta el protocolo de apertura COMPLETO.
    Retorna un dict con toda la información para mostrar al usuario.

    El LLM recibe esto y lo presenta. No necesita recordar nada.

    Returns:
        dict con:
        - sesion_id: int
        - fecha: str
        - dia_semana: str
        - resumen_ayer: dict (bienestar + resumen del día anterior)
        - nudges: list (máx 3 nudges priorizados)
        - coherencia: list (estado de metas activas)
        - agenda_hoy: list (citas/eventos del día)
        - vencidos: list (seguimientos vencidos)
        - urgentes: list (seguimientos de prioridad alta/crítica)
        - checkpoints: list (preguntas obligatorias de apertura)
        - bienestar_hoy: dict o None (si ya se registró)
        - estado: 'esperando_checkpoint' | 'checkpoint_completo'
    """
    init_db()

    # Abrir sesión en DB
    sesion_id = abrir_sesion(proyecto_id=proyecto_id, notas=notas)

    # Fecha y día
    ahora = datetime.now()
    dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    dia_semana = dias_semana[ahora.weekday()]

    # Resumen de ayer
    resumen_ayer = get_resumen_ayer()

    # Nudges (seguimientos vencidos, áreas descuidadas, metas inactivas)
    nudges = generar_nudges(max_nudges=3)

    # Coherencia intención vs comportamiento
    try:
        coherencia = reporte_coherencia(dias=30, imprimir=False)
    except Exception:
        coherencia = []

    # Agenda del día
    agenda_hoy = get_agenda_dia()

    # Alertas (vencidos, próximos, agenda — motor automático)
    alertas = generar_alertas()

    # Pendientes vencidos y urgentes (para compatibilidad)
    vencidos = alertas['rojas']
    urgentes = alertas['amarillas']

    # Pendientes agrupados por tipo (3 bloques)
    try:
        pendientes_agrupados = get_pendientes_agrupados()
    except Exception:
        pendientes_agrupados = None

    # Status por proyecto
    try:
        status_proyectos = get_status_proyectos()
    except Exception:
        status_proyectos = []

    # Checkpoints de apertura (preguntas obligatorias)
    checkpoints = get_checkpoints('apertura')

    # ¿Ya se registró bienestar hoy?
    bienestar_hoy = _bienestar_ya_registrado_hoy()

    # Rutinas pendientes de hoy (no ejecutadas aún)
    try:
        rutinas_pendientes = get_rutinas_pendientes()
    except Exception:
        rutinas_pendientes = []

    # Email: resumen rápido del inbox (todas las cuentas)
    try:
        email_resumen = resumen_inbox() if email_configurado() else None
    except Exception:
        email_resumen = None

    resultado = {
        'sesion_id': sesion_id,
        'fecha': ahora.strftime('%Y-%m-%d'),
        'hora': ahora.strftime('%H:%M'),
        'dia_semana': dia_semana,
        'resumen_ayer': resumen_ayer,
        'nudges': nudges,
        'coherencia': [
            {
                'meta': r['meta']['descripcion'],
                'proyecto': r['meta']['proyecto'],
                'coherencia': r['coherencia'],
                'senal': r['senal'],
                'espejo': r['espejo']
            }
            for r in coherencia
        ] if coherencia else [],
        'agenda_hoy': agenda_hoy,
        'alertas': alertas,
        'vencidos': vencidos,
        'vencidos_count': len(vencidos),
        'urgentes': urgentes,
        'urgentes_count': len(urgentes),
        'checkpoints': checkpoints,
        'bienestar_hoy': bienestar_hoy,
        'rutinas_pendientes': rutinas_pendientes,
        'rutinas_overdue': [r for r in rutinas_pendientes if r.get('overdue')],
        'email': email_resumen,
        'pendientes_agrupados': pendientes_agrupados,
        'status_proyectos': status_proyectos,
        'estado': 'checkpoint_completo' if bienestar_hoy else 'esperando_checkpoint',
    }

    return resultado


def registrar_checkpoint_apertura(texto_respuesta, sesion_id=None):
    """
    Procesa la respuesta del usuario al checkpoint de apertura.
    Parsea texto libre → valores numéricos → registra en bienestar.

    Args:
        texto_respuesta: string con la respuesta del usuario
        sesion_id: sesión actual (opcional)

    Returns:
        dict con:
        - valores: dict con los valores parseados
        - faltantes: list de campos que no se pudieron parsear
        - resumen: string con el resumen legible
        - bienestar_id: int (ID del registro en DB)
        - completo: bool (True si se parsearon los 4 campos core)
    """
    # Parsear respuesta
    valores = parsear_bienestar(texto_respuesta)
    faltantes = campos_faltantes(valores)
    resumen = formato_resumen(valores)

    # Verificar si ya existe registro hoy (actualizar vs insertar)
    hoy = date.today().isoformat()
    existente = _bienestar_ya_registrado_hoy()

    if existente:
        # Actualizar solo los campos que se parsearon
        conn = get_connection()
        updates = []
        params = []
        for campo, valor in valores.items():
            if valor is not None:
                updates.append(f"{campo} = ?")
                params.append(valor)
        if updates:
            params.append(hoy)
            conn.execute(
                f"UPDATE bienestar SET {', '.join(updates)} WHERE fecha = ?",
                params
            )
            conn.commit()
        conn.close()
        bienestar_id = existente['id']
    else:
        # Insertar nuevo registro
        bienestar_id = add_bienestar(
            fecha=hoy,
            humor=valores['humor'],
            energia=valores['energia'],
            estres=valores['estres'],
            horas_sueno=valores['horas_sueno'],
            ejercicio_min=valores['ejercicio_min'],
            atencion_familia=valores['atencion_familia']
        )

    return {
        'valores': valores,
        'faltantes': faltantes,
        'resumen': resumen,
        'bienestar_id': bienestar_id,
        'completo': len(faltantes) == 0,
        'texto_original': texto_respuesta,
    }


def registrar_checkpoint_cierre(texto_respuesta, sesion_id=None):
    """
    Procesa la respuesta del usuario al checkpoint de cierre.
    Actualiza el bienestar del día con datos de cierre.

    Args:
        texto_respuesta: string con la respuesta del usuario
        sesion_id: sesión actual (opcional)

    Returns:
        dict con valores parseados + campos actualizados
    """
    valores = parsear_bienestar(texto_respuesta)
    hoy = date.today().isoformat()

    existente = _bienestar_ya_registrado_hoy()

    if existente:
        # Actualizar con datos de cierre
        conn = get_connection()
        updates = []
        params = []
        for campo, valor in valores.items():
            if valor is not None:
                updates.append(f"{campo} = ?")
                params.append(valor)

        # Extraer logros/frustraciones del texto libre
        texto_lower = texto_respuesta.lower()
        if any(w in texto_lower for w in ['bien', 'logr', 'avanz', 'terminé', 'termine']):
            updates.append("logros = ?")
            params.append(texto_respuesta[:200])
        if any(w in texto_lower for w in ['frustr', 'mal', 'no pude', 'falló', 'fallo']):
            updates.append("frustraciones = ?")
            params.append(texto_respuesta[:200])

        if updates:
            params.append(hoy)
            conn.execute(
                f"UPDATE bienestar SET {', '.join(updates)} WHERE fecha = ?",
                params
            )
            conn.commit()
        conn.close()
        bienestar_id = existente['id']
    else:
        bienestar_id = add_bienestar(
            fecha=hoy,
            humor=valores['humor'],
            energia=valores['energia'],
            estres=valores['estres'],
            horas_sueno=valores['horas_sueno'],
            ejercicio_min=valores['ejercicio_min'],
            atencion_familia=valores['atencion_familia']
        )

    return {
        'valores': valores,
        'resumen': formato_resumen(valores),
        'bienestar_id': bienestar_id,
        'texto_original': texto_respuesta,
    }


def cierre(sesion_id=None, respuestas_cierre=None):
    """
    Ejecuta el protocolo de cierre COMPLETO.

    Args:
        sesion_id: ID de la sesión a cerrar (si None, busca la abierta)
        respuestas_cierre: texto con respuestas del checkpoint de cierre

    Returns:
        dict con:
        - checkpoints: list (preguntas de cierre)
        - bienestar_cierre: dict (resultado del parseo, si hay respuestas)
        - metricas: dict (métricas de sesión, calculadas por detector_cierre)
        - resumen: str (resumen del día)
        - cierre_sesion: dict (datos del cierre)
        - estado: 'esperando_checkpoint' | 'completado'
    """
    # Buscar sesión abierta si no se especifica
    if sesion_id is None:
        sesion_abierta = get_sesion_abierta()
        if sesion_abierta:
            sesion_id = sesion_abierta['id']

    # Checkpoints de cierre
    checkpoints = get_checkpoints('cierre')

    resultado = {
        'sesion_id': sesion_id,
        'checkpoints': checkpoints,
        'bienestar_cierre': None,
        'resumen_diario': None,
        'cierre_sesion': None,
        'aprendizajes': None,
        'estado': 'esperando_checkpoint',
    }

    # Si hay respuestas de cierre, procesarlas
    if respuestas_cierre:
        resultado['bienestar_cierre'] = registrar_checkpoint_cierre(
            respuestas_cierre, sesion_id
        )

        # Generar resumen diario
        try:
            resumen = resumen_diario()
            resultado['resumen_diario'] = resumen
        except Exception as e:
            resultado['resumen_diario'] = f"Error generando resumen: {e}"

        # Aprender de la sesión (analizar patrones)
        try:
            resultado['aprendizajes'] = aprender_de_sesion(sesion_id)
        except Exception as e:
            resultado['aprendizajes'] = {'error': str(e)}

        # Cerrar sesión
        if sesion_id:
            resumen_texto = respuestas_cierre[:200] if respuestas_cierre else None
            cierre_data = cerrar_sesion(sesion_id, resumen=resumen_texto)
            resultado['cierre_sesion'] = cierre_data

        resultado['estado'] = 'completado'

    return resultado


def estado_sesion():
    """
    Retorna el estado actual de la sesión para diagnóstico.
    Útil para saber en qué punto del flujo estamos.
    """
    sesion = get_sesion_abierta()
    bienestar = _bienestar_ya_registrado_hoy()
    vencidos, urgentes = _pendientes_vencidos()

    return {
        'sesion_abierta': sesion is not None,
        'sesion_id': sesion['id'] if sesion else None,
        'sesion_inicio': f"{sesion['fecha']} {sesion['hora_inicio']}" if sesion else None,
        'bienestar_registrado': bienestar is not None,
        'bienestar_completo': bienestar is not None and all(
            bienestar.get(c) is not None for c in ['humor', 'energia', 'estres', 'horas_sueno']
        ),
        'vencidos': len(vencidos),
        'urgentes': len(urgentes),
        'fecha': date.today().isoformat(),
    }


def formato_apertura(data):
    """
    Formatea el resultado de apertura() como texto legible.
    Para mostrar al usuario en Claude Code o en la app web.
    """
    lines = []
    lines.append(f"Buenos días Hernán. {data['dia_semana'].capitalize()} {data['fecha']}.")
    lines.append("")

    # Resumen de ayer
    ayer = data.get('resumen_ayer', {})
    if ayer and ayer.get('bienestar_ayer'):
        b = ayer['bienestar_ayer']
        lines.append("--- Ayer ---")
        partes = []
        if b.get('humor'): partes.append(f"humor={b['humor']}")
        if b.get('energia'): partes.append(f"energía={b['energia']}")
        if b.get('estres'): partes.append(f"estrés={b['estres']}")
        if b.get('horas_sueno'): partes.append(f"sueño={b['horas_sueno']}hs")
        if partes:
            lines.append("  " + " | ".join(partes))
        if ayer.get('resumen_ayer'):
            lines.append(f"  Resumen: {ayer['resumen_ayer'][:100]}")
        lines.append("")

    # === PENDIENTES AGRUPADOS (3 bloques) ===
    pa = data.get('pendientes_agrupados')
    if pa:
        orden_mis = ['cobro', 'comunicar', 'visita', 'entregar', 'vencimiento', 'investigar', 'tarea']
        orden_terceros = ['decidir', 'espera', 'entregar']

        # Bloque 1: Mis compromisos
        lines.append(f"--- MIS COMPROMISOS ({pa['mis_total']}) ---")
        for tipo in orden_mis:
            items = pa['mis_compromisos'].get(tipo, [])
            if items:
                lines.append(f"  {tipo.upper()} ({len(items)}):")
                for item in items[:5]:
                    persona = f" — {item['persona']}" if item.get('persona') else ""
                    venc = f" [{item['dias_vencido']}d venc]" if item.get('dias_vencido') else ""
                    lines.append(f"    #{item['id']} {item['accion'][:60]}{persona}{venc}")
                if len(items) > 5:
                    lines.append(f"    ... y {len(items) - 5} más")
        lines.append("")

        # Bloque 2: Compromisos de terceros
        lines.append(f"--- COMPROMISOS DE TERCEROS ({pa['terceros_total']}) ---")
        for tipo in orden_terceros:
            items = pa['compromisos_terceros'].get(tipo, [])
            if items:
                lines.append(f"  {tipo.upper()} ({len(items)}):")
                for item in items[:5]:
                    persona = f" — {item['persona']}" if item.get('persona') else ""
                    venc = f" [{item['dias_vencido']}d venc]" if item.get('dias_vencido') else ""
                    lines.append(f"    #{item['id']} {item['accion'][:60]}{persona}{venc}")
                if len(items) > 5:
                    lines.append(f"    ... y {len(items) - 5} más")
        lines.append("")

        # Bloque 3: Vencimientos
        if pa['vencimientos']:
            lines.append(f"--- VENCIMIENTOS ({pa['vencimientos_total']}) ---")
            for item in pa['vencimientos']:
                lines.append(f"    #{item['id']} {item['accion'][:60]} — {item.get('fecha_limite', '?')}")
            lines.append("")

    # === STATUS POR PROYECTO ===
    sp = data.get('status_proyectos', {})
    if sp:
        def _fmt_proyecto(p):
            venc_txt = f", {p['vencidos']} vencidos" if p.get('vencidos') else ""
            dias_txt = ""
            if p.get('dias_sin_actividad') is not None:
                if p['dias_sin_actividad'] > 7:
                    dias_txt = f" — {p['dias_sin_actividad']}d sin mov"
                elif p['dias_sin_actividad'] == 0:
                    dias_txt = " — hoy"
                else:
                    dias_txt = f" — hace {p['dias_sin_actividad']}d"
            return f"    {p['nombre'][:35]:35} | {p['total_pend']} pend{venc_txt}{dias_txt}"

        lines.append("--- STATUS POR PROYECTO ---")
        if sp.get('laboral'):
            lines.append("  LABORAL:")
            for p in sp['laboral']:
                lines.append(_fmt_proyecto(p))
        if sp.get('personal'):
            lines.append("  PERSONAL:")
            for p in sp['personal']:
                lines.append(_fmt_proyecto(p))
        lines.append("")

    # Nudges
    if data.get('nudges'):
        lines.append("--- Sugerencias ---")
        for n in data['nudges']:
            lines.append(f"  [{n['tipo']}] {n['mensaje']}")
        lines.append("")

    # Coherencia
    if data.get('coherencia'):
        lines.append("--- Coherencia intención/acción ---")
        for c in data['coherencia']:
            icono = {'on_track': 'OK', 'en_riesgo': '~~', 'desalineada': 'XX', 'abandonada': '!!'}.get(c['senal'], '??')
            lines.append(f"  [{icono}] {c['meta'][:40]} | {c['espejo']}")
        lines.append("")

    # Agenda
    if data.get('agenda_hoy'):
        lines.append("--- Agenda de hoy ---")
        for a in data['agenda_hoy']:
            hora = a.get('hora', '??:??')
            lines.append(f"  {hora} {a['titulo']}")
        lines.append("")

    # Email
    em = data.get('email')
    if em and em.get('configurado'):
        lines.append(f"--- Email ---")
        lines.append(f"  {em['texto']}")
        if em.get('alertas'):
            for a in em['alertas'][:3]:
                lines.append(f"  [!] {a['asunto'][:60]} — de: {a['de'][:30]}")
        lines.append("")

    # Checkpoint
    if data['estado'] == 'esperando_checkpoint':
        lines.append("--- Checkpoint apertura (obligatorio) ---")
        for cp in data.get('checkpoints', []):
            lines.append(f"  - {cp['pregunta']}")
        lines.append("")
        lines.append("Contestá todo junto o de a una, como quieras.")

    return "\n".join(lines)


def formato_cierre(data):
    """Formatea el resultado de cierre() como texto legible."""
    lines = []

    if data['estado'] == 'esperando_checkpoint':
        lines.append("--- Checkpoint cierre (obligatorio) ---")
        for cp in data.get('checkpoints', []):
            lines.append(f"  - {cp['pregunta']}")
        lines.append("")
        lines.append("Contestá rápido, no hace falta mucho detalle.")
    elif data['estado'] == 'completado':
        lines.append("--- Sesión cerrada ---")
        if data.get('bienestar_cierre'):
            lines.append(f"  Bienestar: {data['bienestar_cierre']['resumen']}")
        if data.get('cierre_sesion'):
            cs = data['cierre_sesion']
            lines.append(f"  Duración: {cs.get('duracion_min', 0)} min | {cs.get('total_mensajes', 0)} mensajes")

    return "\n".join(lines)


if __name__ == '__main__':
    import sys as _sys

    if len(_sys.argv) > 1:
        cmd = _sys.argv[1]
        if cmd == 'apertura':
            data = apertura()
            print(formato_apertura(data))
        elif cmd == 'cierre':
            data = cierre()
            print(formato_cierre(data))
        elif cmd == 'estado':
            import json
            print(json.dumps(estado_sesion(), indent=2, ensure_ascii=False))
        else:
            print("Uso: python tools/orquestador_sesion.py [apertura|cierre|estado]")
    else:
        print("Uso: python tools/orquestador_sesion.py [apertura|cierre|estado]")
