"""
Migración: datos de .md a DB.
Mueve toda la información de perfil-hernan.md y seguimiento.md
a tablas de la DB. Después de ejecutar, los .md se pueden eliminar.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tracker import get_connection
from datetime import datetime


def migrate():
    conn = get_connection()
    c = conn.cursor()

    # ============================================
    # 1. Crear tabla perfil_datos (key-value flexible)
    # ============================================
    c.execute('''CREATE TABLE IF NOT EXISTS perfil_datos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER,
        campo TEXT NOT NULL,
        valor TEXT NOT NULL,
        categoria TEXT,
        fecha_desde TEXT,
        fecha_hasta TEXT,
        notas TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )''')
    print("Tabla perfil_datos creada")

    # Verificar si ya se migró
    c.execute("SELECT COUNT(*) as n FROM perfil_datos")
    if c.fetchone()['n'] > 0:
        print("ABORT: perfil_datos ya tiene datos. No re-migrar.")
        conn.close()
        return

    # ============================================
    # 2. Educación formal de Hernán (persona_id=12)
    # ============================================
    educacion = [
        (12, "Tecnico Nacional en Electronica", "ENET N2 de Haedo (ORT ciclo basico)", "educacion_formal", "1987", "1992", "Egreso diciembre 1992"),
        (12, "Profesor Nacional en Educacion Fisica", "IMEF Dr. Enrique Romero Brest", "educacion_formal", "1993", "1998", None),
        (12, "Licenciado en Alto Rendimiento Deportivo y Salud", "UNSAM", "educacion_formal", None, "2012", "Fecha ingreso por confirmar"),
        (12, "Tecnico Superior en Ciencia de Datos e IA", "IFTS N18, GCBA", "educacion_formal", "2023", "2025", "Egreso 2025"),
        (12, "Actor", "Centro Cultural Sabato", "educacion_formal", "2001", "2004", "Titulo fisico no digitalizado"),
        (12, "Full Stack Python - Codo a Codo 4.0", "GCBA", "certificacion", "2023", "2023", "208 hrs, 20 semanas"),
        (12, "Google PM: Foundations + Initiation + Planning", "Coursera", "certificacion", "2022", "2023", "3 cursos completados"),
        (12, "Intro Programacion Python", "Universidad Austral / Coursera", "certificacion", "2020", "2020", "Certificado 2 mar 2020"),
        (12, "PNL", "Instituto PNL", "certificacion", "2010", "2010", None),
        (12, "FEMEC Catedra libre investigacion", "FEMEC", "certificacion", "2011", "2012", None),
        (12, "Generative AI Leader", "Google", "certificacion", "2025", "2025", None),
        (12, "Prompt Design in Vertex AI", "Google Cloud", "certificacion", "2025", "2025", "Skill Badge"),
        (12, "PEI Institute A2+", "PEI", "certificacion", "2023", "2023", "Ingles"),
        (12, "Clases privadas JS/NestJS con Mauro", "Privado", "certificacion", "2023", "2023", "Verano 2023, para app TUP"),
        (12, "Capacitacion ventas networking", "Silk Tecnologies", "certificacion", "2015", "2015", None),
    ]
    for e in educacion:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", e)
    print(f"Educacion: {len(educacion)} registros")

    # ============================================
    # 3. Experiencia laboral de Hernán
    # ============================================
    experiencia = [
        (12, "Madrich (lider juvenil)", "Movimiento judio", "experiencia", "1989", "1992", "Primer trabajo. Liderazgo de grupos"),
        (12, "Instalador porteros electricos", "Independiente", "experiencia", "1993", "1993", "Post-diploma. Conocio a Esteban Marcucci"),
        (12, "Deportes/Recreacion", "Hebraica", "experiencia", "1993", "1994", "Centro comunitario judio"),
        (12, "Director Escuelas Deportivas", "Mi Refugio Country Club", "experiencia", "1995", "2012", "18 anios. Prof > Coord > Director"),
        (12, "Ser Dinamico de Deporte y Nutricion", "Marca propia", "experiencia", "1996", "2017", "21 anios. PT, running, viandas, capacitaciones"),
        (12, "Director de Deportes y Cultura", "CSHA", "experiencia", "2012", "2013", "Circulo Social Hebreo Argentino. ~$12.500/mes en 2013"),
        (12, "Asesoramiento en licitaciones", "Independiente", "experiencia", "2014", "2015", "Min Planificacion, Min Seguridad PBA"),
        (12, "Ventas networking Cisco", "Silk Tecnologias", "experiencia", "2015", "2016", "Soporte tecnico, preventa"),
        (12, "Gerente de Proyectos", "Software By Design S.A.", "experiencia", "2016", None, "Ventas > PM > Gerente. Posadas, SBASE, CCTV"),
        (12, "Importacion gadgets", "Uno Mayorista Argentina", "experiencia", "2017", "2019", "Con hermano Alfredo. Cayo pre-pandemia"),
        (12, "Fabricacion muebles", "Con Esteban Marcucci", "experiencia", "2019", "2021", "Pandemia"),
        (12, "Personal Trainer", "Freelance", "experiencia", "1996", "2022", "Ultima clase 2022"),
        (12, "Freelancer developer", "Independiente", "experiencia", "2022", "2023", "Apps entrenamiento, prediccion bursatil"),
        (12, "AiControl Seguridad", "Emprendimiento propio", "experiencia", "2024", None, "Con Esteban. Seguridad + vision computadora"),
    ]
    for e in experiencia:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", e)
    print(f"Experiencia: {len(experiencia)} registros")

    # ============================================
    # 4. Skills técnicos e idiomas
    # ============================================
    skills = [
        (12, "Python", "Avanzado - pandas, numpy, sklearn, TF, PyTorch, LSTM, NLP, BERT", "skill", None, None, None),
        (12, "R", "Intermedio - ARIMA, GLM, XGBoost, clustering", "skill", None, None, None),
        (12, "JavaScript/React/Node", "En crecimiento - React, NextJS, NestJS, FastAPI, Django", "skill", None, None, None),
        (12, "SQL/NoSQL", "PostgreSQL, MongoDB, SQLite, ChromaDB, Power BI", "skill", None, None, None),
        (12, "AI/ML", "Groq API, Ollama, Google Colab+CUDA, RAG, embeddings", "skill", None, None, None),
        (12, "DevOps", "Docker, docker-compose, WSL, Git", "skill", None, None, None),
        (12, "Seguridad electronica", "Hikvision, DVR/NVR, control acceso", "skill", None, None, None),
        (12, "Hardware", "Arduino, armado PC, electronica", "skill", None, None, None),
        (12, "Espaniol", "Nativo", "idioma", None, None, None),
        (12, "Ingles", "Intermedio-avanzado", "idioma", None, None, "Technical writing, fluent communication"),
        (12, "Hebreo", "Oral y escrito nivel medio", "idioma", None, None, None),
    ]
    for s in skills:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", s)
    print(f"Skills/idiomas: {len(skills)} registros")

    # ============================================
    # 5. Familia extendida (no en tabla personas)
    # ============================================
    familia = [
        (12, "Raul Jacobo Hamra", "Padre. Fallecio 12/06/2012", "familia", None, "2012", None),
        (12, "Fortuna Jabbaz (Mazal)", "Madre. Psicologa pionera. Fallecio marzo 2024", "familia", "1939", "2024", "5 anios postrada antes de fallecer"),
        (12, "Susana Hamra", "Hermana (melliza mayor con Alfredo)", "familia", None, None, None),
        (12, "Alfredo Hamra", "Hermano mellizo mayor. Uno Mayorista", "familia", None, None, None),
        (12, "Valeria Hamra", "Hermana melliza menor (con Hernan)", "familia", None, None, None),
        (12, "Meitu", "Sobrina. Bat mitzva. Prodigia matematicas y hockey", "familia", None, None, None),
        (12, "Kiara", "Sobrina. Bat mitzva", "familia", None, None, None),
    ]
    for f in familia:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", f)
    print(f"Familia extendida: {len(familia)} registros")

    # ============================================
    # 6. Postulaciones laborales
    # ============================================
    postulaciones = [
        (12, "Veritran / VEC Fleet", "Lider de Proyecto", "postulacion", "2021", "2021", "Carta de presentacion"),
        (12, "Media.Monks", "Data Scientist", "postulacion", "2024", "2024", "Cover letter"),
        (12, "J.P. Morgan", "Senior Python Developer", "postulacion", "2025", "2025", "Cover letter formal con firma"),
    ]
    for p in postulaciones:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", p)
    print(f"Postulaciones: {len(postulaciones)} registros")

    # ============================================
    # 7. Plan nutricional (estaba solo en seguimiento.md)
    # ============================================
    c.execute("""INSERT INTO salud (persona_id, tipo, fecha, profesional, especialidad, descripcion, estado, notas)
        VALUES (12, 'plan_nutricional', '2026-02-18', 'Lic. Julieta Belen Iglesias (M.N. 12390)',
        'Nutricion', 'Recomposicion corporal. Alta proteina: 270g carne/pescado x comida. Plato: 1/2 proteina + 1/4 vegetales (2 colores) + 1/4 legumbres + grasa buena. Suplementos: whey, creatina 5g/dia, magnesio bisglicinato. Ejercicio: gym 2-3x/sem, cardio 3-4x/sem, 10k pasos. Hidratacion: 2-3L/dia.',
        'activo', 'Desayuno/merienda: 6 opciones rotativas. Tips glucemia: vegetales primero, caminata 10min post-comida, fruta entera. Snacks: banana+whey, barrita proteica, sandwich, yogur. Marcas: Ser Pro+, Kay Griego, Integra Proteica. PDF en OneDrive > SALUD FLIA > HERNAN > 2026')""")
    print("Plan nutricional migrado a salud")

    # ============================================
    # 8. Salud familia (Margarita - estaba solo en .md)
    # ============================================
    c.execute("""INSERT INTO salud (persona_id, tipo, especialidad, descripcion, estado, notas)
        VALUES (10, 'estudio', 'Pie/Podologia', 'Estudios medicos del pie. Carpeta MARAGA PIE en OneDrive personal.', 'pendiente', 'Seguimiento pendiente')""")
    print("Salud Margarita actualizado")

    # ============================================
    # 9. Situación laboral / compensación (estaba en MEMORY.md)
    # ============================================
    compensacion = [
        ("sueldo_hernan", "$1.100.000 ARS/mes", "compensacion_hernan", "Febrero 2026"),
        ("extra_usd_hernan", "USD 500/mes", "compensacion_hernan", "Por gestion proyectos"),
        ("comision_posadas", "3% sobre Posadas", "compensacion_hernan", None),
        ("claude_suscripcion", "USD 100/mes", "compensacion_hernan", "SBD lo paga desde feb 2026"),
    ]
    for campo, valor, cat, notas in compensacion:
        c.execute("INSERT INTO empresa_datos (campo, valor, categoria, notas) VALUES (?,?,?,?)",
                  (campo, valor, cat, notas))
    print(f"Compensacion: {len(compensacion)} registros en empresa_datos")

    # ============================================
    # 10. Estructura empresarial (Gervasio, empresas asociadas)
    # ============================================
    estructura = [
        ("gervasio_empresa_unipersonal", "Empresa unipersonal de Gervasio", "estructura_asociadas", None),
        ("tefiti", "Empresa de Gervasio + Marino", "estructura_asociadas", None),
        ("tercera_empresa_gervasio", "Empresa de Gervasio + Ezequiel", "estructura_asociadas", None),
        ("regla_recursos", "NO tocar recursos/empleados de empresas asociadas para proyectos propios", "estructura_asociadas", "Regla de SBD"),
    ]
    for campo, valor, cat, notas in estructura:
        c.execute("INSERT INTO empresa_datos (campo, valor, categoria, notas) VALUES (?,?,?,?)",
                  (campo, valor, cat, notas))
    print(f"Estructura empresarial: {len(estructura)} registros")

    # ============================================
    # 11. Decisiones estratégicas → eventos
    # ============================================
    decisiones = [
        ("2026-02-24", "decision", "ARGOS es ESPEJO no COACH - muestra patrones, no empuja cambio", "estrategia", 7, None, "agentes", "Documentado", None),
        ("2026-02-24", "decision", "Agentes invisibles para usuario final - habla con ARGOS, no con agentes", "estrategia", 7, None, "agentes", "Documentado", None),
        ("2026-02-24", "decision", "Metodo generico + contexto profundo = el producto", "estrategia", 7, None, "agentes", "Documentado", None),
    ]
    for d in decisiones:
        c.execute("""INSERT INTO eventos (fecha, tipo, descripcion, subtipo, proyecto_id, persona_id, fuente, resultado, notas)
                     VALUES (?,?,?,?,?,?,?,?,?)""", d)
    print(f"Decisiones estrategicas: {len(decisiones)} eventos")

    # ============================================
    # 12. Datos chicos (escuela/actividades - estaba incompleto en .md)
    # ============================================
    chicos = [
        (12, "Uriel - edad", "18 anios (nac 26/02/2007). Bar Mitzva 5/03/2020", "hijos_datos", None, None, "Nombre hebreo: Aharon"),
        (12, "Sol Chiara - edad", "17 anios (nac 11/04/2008). Bat Mitzva ~2020/21", "hijos_datos", None, None, "Nombre hebreo: Mazal Shoshana"),
        (12, "Matias - edad", "14 anios (nac 03/10/2011). Bar Mitzva 7/10/2024", "hijos_datos", None, None, "Nombre hebreo: Iacov"),
    ]
    for ch in chicos:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", ch)
    print(f"Datos hijos: {len(chicos)} registros")

    # ============================================
    # 13. Referencias profesionales
    # ============================================
    refs = [
        (12, "Juan Pablo Belluomo", "Account Manager en SYSTEMNET S.A.", "referencia_profesional", None, None, None),
        (12, "Marcelo Hamra", "Presidente Software By Design S.A.", "referencia_profesional", None, None, "Hermano"),
        (12, "Saul Hanono", "Commit IT SRL", "referencia_profesional", None, None, None),
    ]
    for r in refs:
        c.execute("INSERT INTO perfil_datos (persona_id, campo, valor, categoria, fecha_desde, fecha_hasta, notas) VALUES (?,?,?,?,?,?,?)", r)
    print(f"Referencias: {len(refs)} registros")

    conn.commit()

    # Resumen final
    c.execute("SELECT categoria, COUNT(*) as n FROM perfil_datos GROUP BY categoria ORDER BY n DESC")
    print("\n=== RESUMEN perfil_datos ===")
    for r in c.fetchall():
        print(f"  {r['categoria']}: {r['n']}")
    c.execute("SELECT COUNT(*) as n FROM perfil_datos")
    print(f"  TOTAL: {c.fetchone()['n']}")

    conn.close()
    print("\nMigracion completada OK")


if __name__ == '__main__':
    migrate()
