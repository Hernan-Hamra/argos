"""
Seed de TODOS los protocolos de ARGOS.
Genera seeds para las 8 capacidades que faltan.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.tracker import get_connection
from datetime import datetime


def seed():
    conn = get_connection()
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')

    # Verificar si ya se seedearon
    c.execute("SELECT COUNT(*) as n FROM patrones WHERE tipo='protocolo_salud'")
    if c.fetchone()['n'] > 0:
        print("ABORT: protocolos de salud ya existen. No re-seedear.")
        conn.close()
        return

    todos = []

    # ============================================
    # 1. SEGUIMIENTO DE SALUD
    # ============================================
    todos.extend([
        ("protocolo_salud", "flujo", "Registrar turno medico",
         "Preguntar: fecha, profesional, especialidad, lugar. Insertar en tabla salud con estado=pendiente. Crear seguimiento con fecha_limite=fecha del turno. Alertar en inicio de sesion si hay turno proximo (3 dias).",
         None),
        ("protocolo_salud", "flujo", "Registrar resultado de consulta",
         "Actualizar registro en salud: estado=realizado, resultado=diagnostico/indicacion, proxima_cita si hay. Si hay cirugia indicada, crear seguimiento con prioridad alta.",
         None),
        ("protocolo_salud", "flujo", "Registrar estudio medico",
         "Tipo=estudio en tabla salud. Registrar donde queda el archivo (path en OneDrive). Si es de familiar, usar persona_id correspondiente de tabla personas.",
         None),
        ("protocolo_salud", "flujo", "Registrar plan medico/nutricional",
         "Tipo=plan_nutricional o plan_medico en salud. Descripcion con el plan completo. Estado=activo. Notas con detalles (marcas, suplementos, rutina).",
         None),
        ("protocolo_salud", "principio", "Salud familiar incluida",
         "No solo el usuario principal. Registrar turnos, estudios y planes de familiares con su persona_id correspondiente. Tabla salud soporta cualquier persona_id.",
         None),
        ("protocolo_salud", "principio", "Alertar turnos proximos",
         "En inicio de sesion, consultar: SELECT * FROM salud WHERE estado='pendiente' AND fecha >= date('now') AND fecha <= date('now', '+3 days'). Mostrar como alerta urgente.",
         None),
        ("protocolo_salud", "principio", "No diagnosticar",
         "ARGOS registra y alerta, nunca diagnostica ni recomienda tratamientos. Solo reproduce lo que dijo el profesional.",
         None),
    ])

    # ============================================
    # 2. NUTRICION / DIETA
    # ============================================
    todos.extend([
        ("protocolo_nutricion", "flujo", "Registrar comida",
         "Usuario dice que comio (texto libre o audio). Extraer: tipo_comida (desayuno/almuerzo/merienda/cena/snack), descripcion, calorias_est si es posible. Insertar en tabla nutricion.",
         None),
        ("protocolo_nutricion", "flujo", "Reporte semanal nutricion",
         "Consultar nutricion ultimos 7 dias. Comparar contra plan activo (salud WHERE tipo=plan_nutricional). Detectar: dias sin registro, comidas que no siguen el plan, patrones.",
         None),
        ("protocolo_nutricion", "flujo", "Cargar plan nutricional",
         "Recibir plan del nutricionista (texto, PDF, foto). Extraer reglas: proteinas, vegetales, suplementos, hidratacion, ejercicio. Guardar en salud tipo=plan_nutricional con detalle completo en descripcion+notas.",
         None),
        ("protocolo_nutricion", "principio", "Registro debe ser facil",
         "El usuario dice 'comi pollo con ensalada' y ARGOS lo registra completo. No pedir formularios largos. Extraer datos del texto libre.",
         None),
        ("protocolo_nutricion", "principio", "Nudge sin presion",
         "Si hace 3+ dias sin registrar comida, proactivo.py genera nudge suave. No juzgar, no presionar. Solo recordar.",
         None),
    ])

    # ============================================
    # 3. BIENESTAR DIARIO
    # ============================================
    todos.extend([
        ("protocolo_bienestar", "flujo", "Registro diario de bienestar",
         "Campos: humor (1-5), energia (1-5), estres (1-10), horas_sueno, calidad_sueno, ejercicio_min, logros, frustraciones, conflictos, notas. Insertar en tabla bienestar. No todos los campos son obligatorios.",
         None),
        ("protocolo_bienestar", "flujo", "Reporte semanal bienestar",
         "Consultar bienestar ultimos 7 dias. Calcular promedios. Detectar tendencias (estres subiendo, energia bajando). Cruzar con eventos del mismo periodo para correlacionar.",
         None),
        ("protocolo_bienestar", "principio", "Espejo no coach",
         "Mostrar los numeros y las tendencias. No decir 'deberias descansar mas'. Dejar que el usuario saque sus conclusiones.",
         None),
        ("protocolo_bienestar", "principio", "Nudge si hace 2+ dias sin registro",
         "proactivo.py detecta dias sin bienestar. Nudge: 'Hace X dias sin registrar bienestar. Como estas hoy? (rapido: humor/energia/estres)'",
         None),
    ])

    # ============================================
    # 4. REFLEXIONES / EMOCIONAL
    # ============================================
    todos.extend([
        ("protocolo_reflexion", "flujo", "Capturar reflexion de texto libre",
         "Usuario dice algo emocional/reflexivo. Usar proactivo.extraer_reflexion() para detectar sentimiento, intensidad, area, tags. Insertar en tabla reflexiones con revisado=0.",
         None),
        ("protocolo_reflexion", "flujo", "Revisar reflexiones pendientes",
         "SELECT * FROM reflexiones WHERE revisado=0 ORDER BY fecha DESC. Mostrar al usuario en inicio de sesion si hay reflexiones sin retomar. Preguntar si quiere revisarlas.",
         None),
        ("protocolo_reflexion", "flujo", "Generar reporte emocional",
         "Analizar reflexiones de un periodo. Agrupar por sentimiento, area, intensidad. Detectar patrones: temas recurrentes, areas de frustracion, momentos positivos.",
         None),
        ("protocolo_reflexion", "principio", "No juzgar",
         "Las reflexiones son del usuario. ARGOS registra y refleja, no opina sobre sentimientos. Solo muestra patrones.",
         None),
        ("protocolo_reflexion", "principio", "Detectar automaticamente",
         "Si el usuario dice algo con carga emocional en una conversacion normal, ofrecer registrarlo como reflexion. No forzar.",
         None),
    ])

    # ============================================
    # 5. GESTION DE METAS / COHERENCIA
    # ============================================
    todos.extend([
        ("protocolo_metas", "flujo", "Registrar meta nueva",
         "Campos: descripcion, area (laboral/personal/salud/proyecto), estado=activa, indicadores de avance. Insertar en tabla metas. Crear seguimiento asociado si tiene deadline.",
         None),
        ("protocolo_metas", "flujo", "Medir coherencia intencion vs comportamiento",
         "Usar tools/coherencia.py: medir_coherencia_meta() cruza lo que el usuario dice que quiere con lo que realmente hace (eventos). Puntaje 0-1. Mostrar como espejo.",
         None),
        ("protocolo_metas", "flujo", "Reporte de coherencia semanal",
         "coherencia.reporte_coherencia() genera reporte de todas las metas activas. Muestra: coherencia promedio, metas avanzando, metas abandonadas, sugerencias.",
         None),
        ("protocolo_metas", "principio", "Espejo no presion",
         "Mostrar los numeros. Si coherencia es baja, no decir 'estas fallando'. Decir 'la meta X no tuvo actividad en Y dias. Que queres hacer con esto?'",
         None),
        ("protocolo_metas", "principio", "Detectar metas implicitas",
         "Si el usuario dice repetidamente 'quiero X' pero no tiene meta registrada, sugerir crearla. Solo sugerir, no crear automaticamente.",
         None),
    ])

    # ============================================
    # 6. TELEGRAM BRIDGE
    # ============================================
    todos.extend([
        ("protocolo_telegram", "flujo", "Arrancar bridge",
         "Verificar si loop.py esta corriendo (ps aux | grep loop.py). Si no, ofrecer arrancarlo con nohup. El bridge escribe al inbox JSONL, Claude Code lee con bridge.py --check.",
         None),
        ("protocolo_telegram", "flujo", "Procesar mensaje de texto",
         "loop.py recibe > escribir_mensaje('in', contenido) al inbox > Claude Code lee > procesa > responder() envia a Telegram Y registra en inbox.",
         None),
        ("protocolo_telegram", "flujo", "Procesar audio",
         "loop.py recibe voice > download_voice() > stt.transcribe() con Whisper small > escribir_mensaje('in', transcripcion, tipo='audio') > procesar como texto.",
         None),
        ("protocolo_telegram", "principio", "Canal lo controla el usuario",
         "El usuario abre y cierra el canal Telegram. ARGOS puede proponer cerrar pero no decidirlo. Si el usuario escribe por PC, no mandar por Telegram.",
         None),
        ("protocolo_telegram", "principio", "Nunca silencio mayor a 20 seg",
         "Si algo tarda, avisar 'procesando, X seg'. El usuario no debe quedarse esperando sin feedback.",
         None),
    ])

    # ============================================
    # 7. BACKUP Y SEGURIDAD DB
    # ============================================
    todos.extend([
        ("protocolo_backup", "flujo", "Backup al cerrar sesion",
         "Ejecutar python tools/backup.py. Copia DB con timestamp a carpeta de backup del usuario. Mantiene ultimos 10 backups. El mas reciente se llama _latest.db.",
         None),
        ("protocolo_backup", "flujo", "Safe delete y safe update",
         "Usar db_safety.safe_delete() y safe_update() en vez de DELETE/UPDATE directo. Registra en _papelera antes de borrar. Registra en _operaciones_log.",
         None),
        ("protocolo_backup", "principio", "WAL mode activo",
         "DB usa WAL (Write-Ahead Logging). Permite lecturas concurrentes. Se activa en db_safety.py al arrancar.",
         None),
        ("protocolo_backup", "principio", "Nunca borrar sin papelera",
         "Todo delete pasa por safe_delete que guarda copia en _papelera. Se puede recuperar.",
         None),
    ])

    # ============================================
    # 8. MULTI-AGENTE
    # ============================================
    todos.extend([
        ("protocolo_agentes", "flujo", "Consulta multi-agente",
         "Usar agents/orquestador.py: consultar_agentes(pregunta). El orquestador distribuye a los agentes relevantes (Estratega, Neuro, UX, Etico, Datos, Operaciones, Comunicacion). Cada uno responde desde su perspectiva.",
         None),
        ("protocolo_agentes", "flujo", "Panel de estado",
         "panel_agentes() muestra estado de cada agente: activo/inactivo, ultima consulta, especialidad. Se ejecuta al inicio de sesion.",
         None),
        ("protocolo_agentes", "principio", "Agentes invisibles para el usuario",
         "El usuario habla con ARGOS. Los agentes trabajan internamente. No decir 'el agente Neuro opina que...'. Integrar las perspectivas en una sola respuesta.",
         None),
        ("protocolo_agentes", "principio", "Registrar consultas",
         "Cada consulta multi-agente se registra en tabla consultas_agente con la pregunta, agentes consultados, y respuestas. Sirve para mejorar el sistema.",
         None),
    ])

    # Insertar todo
    for tipo, cat, desc, evi, sug in todos:
        c.execute("""INSERT INTO patrones
                     (fecha_deteccion, tipo, categoria, descripcion, evidencia, frecuencia, confianza, estado, sugerencia, compartido)
                     VALUES (?, ?, ?, ?, ?, 1, 0.8, 'validado', ?, 1)""",
                  (hoy, tipo, cat, desc, evi, sug))

    conn.commit()

    # Resumen
    print("=== PROTOCOLOS AGREGADOS ===")
    c.execute("""SELECT tipo, COUNT(*) as n FROM patrones
                 WHERE tipo LIKE 'protocolo_%' AND compartido=1
                 GROUP BY tipo ORDER BY tipo""")
    total = 0
    for r in c.fetchall():
        print(f"  {r['tipo']}: {r['n']}")
        total += r['n']
    print(f"  TOTAL: {total}")

    conn.close()
    print("\nSeed completado OK")


if __name__ == '__main__':
    seed()
