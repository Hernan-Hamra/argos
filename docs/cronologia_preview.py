"""Genera la cronología visual de Hernán con bloques alineados."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BIRTH_YEAR = 1973

def age_str(year):
    """Retorna la edad que cumple ese año."""
    return str(year - BIRTH_YEAR)

def age_range(y1, y2):
    """Retorna rango de edad."""
    a1 = y1 - BIRTH_YEAR
    a2 = y2 - BIRTH_YEAR
    if a1 == a2:
        return str(a1)
    return f"{a1}-{a2}"

def render_band(title, first_year, last_year, sections, label_width=26):
    years = list(range(first_year, last_year + 1))
    col_w = 4  # ancho por columna (3 chars + separador)
    lines = []
    lines.append(f"──── {title} " + "─" * max(0, 95 - len(title) - 6))
    lines.append("")

    # Header: años con separadores verticales
    header = " " * label_width
    for i, y in enumerate(years):
        header += f"{y % 100:02d}  "
    lines.append(header)

    # Age header
    age_hdr = " " * label_width
    for y in years:
        age_hdr += f"{(y - BIRTH_YEAR):2d}  "
    lines.append(age_hdr + " ← edad")

    # Línea separadora con cruces
    sep = " " * label_width
    for i in range(len(years)):
        sep += "┼───"
    lines.append(sep)

    for section_name, activities in sections:
        # Nombre de sección con línea de guías
        lines.append(section_name)
        for act in activities:
            name = act[0]
            year_ranges = act[1]
            year_set = set()
            for s, e in year_ranges:
                for y in range(s, e + 1):
                    year_set.add(y)
            suffix = act[2] if len(act) > 2 else ""

            # Add age to name
            if year_ranges:
                first_y = min(s for s, e in year_ranges)
                last_y = max(e for s, e in year_ranges)
                age_info = f"({age_range(first_y, last_y)})"
            else:
                age_info = ""

            display_name = f"{name} {age_info}".strip()
            padded = display_name.ljust(label_width)
            data = ""
            for i, y in enumerate(years):
                if y in year_set:
                    data += "██▌ "
                else:
                    data += "│   "

            line = padded + data
            if suffix:
                line = line.rstrip() + "  " + suffix
            lines.append(line)

        # Línea guía entre secciones
        guide = " " * label_width
        for i in range(len(years)):
            guide += "│   "
        lines.append(guide)
    return "\n".join(lines)


print("=" * 95)
print("  CRONOLOGÍA COMPLETA — HERNÁN FEDERICO HAMRA (1973-2026)")
print("  █ = año activo | ✓ = título obtenido | † = fallecimiento | ¿? = por confirmar")
print("=" * 95)

# ═══ PARTE 1: 1973-1992 ═══
print(render_band(
    "PARTE 1: INFANCIA Y SECUNDARIO (1973-1992)", 1973, 1992,
    [
        ("PERSONAL:", [
            ("Nacimiento", [(1973, 1973)], "(31/07/1973)"),
        ]),
        ("EDUCACIÓN:", [
            ("Payasín (sala 3)", [(1977, 1977)]),
            ("Ramat Shalom (4-5)", [(1978, 1979)]),
            ("Primaria CISO", [(1980, 1986)]),
            ("ORT → ENET Nº2", [(1987, 1992)], "✓ Téc.Nac.Electrónica"),
        ]),
        ("DEPORTES (CISO):", [
            ("Fútbol", [(1982, 1988)]),
            ("Natación (verano)", [(1983, 1985)], "competitivo"),
            ("Tenis mesa (verano)", [(1983, 1984)]),
        ]),
        ("ARTES / ACTIVIDADES:", [
            ("Kung fu", [(1983, 1987)]),
            ("Rikudim", [(1988, 1992)]),
            ("Agshama", [(1989, 1992)]),
        ]),
        ("CLUBES (socio deportivo):", [
            ("CISO", [(1980, 1988)]),
            ("CISSAB (rikudim)", [(1990, 1992)]),
        ]),
        ("TRABAJO:", [
            ("Negocio del papá (ver)", [(1984, 1986)]),
            ("Mano Emerg.Méd.(ver)", [(1987, 1987)]),
            ("Madrich (mov.juv.)", [(1989, 1992)]),
        ]),
    ]
))

# ═══ PARTE 2: 1993-2013 ═══
print(render_band(
    "PARTE 2: POST-SECUNDARIO Y ERA DEPORTES (1993-2013)", 1993, 2013,
    [
        ("DEPORTES / ENTRENAMIENTO:", [
            ("Gimnasio fuerza/hip.", [(1998, 2001)], "pico post-IMEF"),
            ("Running (entren+comp)", [(1998, 2012)], "2-3 media maratones"),
        ]),
        ("EDUCACIÓN / FORMACIÓN:", [
            ("Terciario IMEF", [(1994, 1997)], "✓ Prof.Ed.Física (98)"),
            ("Esc.Nac.Danzas", [(1993, 1993)], "6 meses"),
            ("Danza jazz", [(1993, 1994)]),
            ("Circo y acrobacia", [(1998, 1999)], "post-IMEF"),
            ("Teatro San Martín", [(1995, 1995)]),
            ("Teatro C.C.Sábato", [(2001, 2004)], "✓ Actor (~04)"),
            ("Esc.Teatro Rubén", [(2005, 2006)], "2 años"),
            ("Clown", [(2007, 2010)], "~3-4 años"),
            ("PNL", [(2010, 2010)]),
            ("FEMEC (investig.)", [(2011, 2012)]),
            ("Lic. UNSAM", [(2010, 2012)], "✓ Lic.Ed.Fís.(12) inicio¿?"),
        ]),
        ("TRABAJO 1 (principal):", [
            ("Port. eléctricos", [(1993, 1993)]),
            ("Hebraica", [(1994, 1995)], "inicio ¿93 o 94?"),
            ("Mi Refugio CC", [(1996, 2012)]),
            ("CSHA Dir.Cultura", [(2012, 2013)]),
        ]),
        ("TRABAJOS PARALELOS:", [
            ("Bialik de Devoto", [(1996, 1997)], "coord. adolescentes, 1ra PC"),
            ("Ser Dinámico", [(1996, 2013)], "→ sigue hasta 2017"),
            ("  └─ Personal trainer", [(1996, 2013)], "→ sigue hasta 2022"),
            ("  └─ Running/entren.", [(1996, 2013)], "2-3 media maratones"),
            ("Or Torá (Barracas)", [(1998, 2001)], "profe, fechas ¿?"),
            ("  └─ Escuelita fútbol", [(1999, 2000)], "extra-escolar, 2 años ¿?"),
            ("Esc.Deport. Filiol", [(1998, 1999)], "2 años, fechas ¿?"),
            ("Colegio en Ruta 11", [(1998, 2000)], "fechas ¿?"),
            ("Colonias verano:", []),
            ("  Hebraica", [(1995, 2000)], "fechas ¿?"),
            ("  Mi Refugio", [(1996, 2012)], "veranos"),
            ("  Barkojba", [(1998, 2002)], "fechas ¿?"),
        ]),
        ("CLUBES (socio deportivo):", [
            ("CSHA (con familia)", [(2012, 2013)]),
        ]),
        ("PERSONAL:", [
            ("Noviazgo Natalia", [(1997, 2001)]),
            ("Matrimonio Natalia", [(2002, 2013)], "→ sigue hasta hoy"),
            ("Nace Uriel", [(2007, 2007)], "(26/02)"),
            ("Nace Sol", [(2008, 2008)], "(11/04)"),
            ("Nace Matías", [(2011, 2011)], "(03/10)"),
            ("† Raúl (padre)", [(2012, 2012)], "(12/06/2012) mismo día media maratón"),
        ]),
    ]
))

# ═══ PARTE 3: 2014-2026 ═══
print(render_band(
    "PARTE 3: TRANSICIÓN Y ERA TECNOLOGÍA (2014-2026)", 2014, 2026,
    [
        ("TRABAJO 1 (principal):", [
            ("Asesor.licitaciones", [(2014, 2015)]),
            ("Silk Tecnologías", [(2015, 2016)]),
            ("SBD", [(2016, 2026)], "← Ventas→PM→Gte.Proy."),
        ]),
        ("TRABAJO 2 (paralelo):", [
            ("Ser Dinámico", [(2014, 2017)], "(fin 2017)"),
            ("Uno Mayorista", [(2017, 2019)], "(cae 2019)"),
            ("Muebles+Esteban", [(2020, 2021)]),
            ("Freelancer dev", [(2023, 2024)]),
            ("AiControl Seguridad", [(2024, 2026)]),
            ("ARGOS", [(2026, 2026)]),
        ]),
        ("TRABAJO 3 (paralelo):", [
            ("Personal trainer", [(2014, 2022)], "(última clase 2022, desde 96 dentro de Ser Dinámico)"),
        ]),
        ("DEPORTES / ENTRENAMIENTO:", [
            ("Gimnasio fuerza/hip.", [(2023, 2023)], "2do pico fuerte"),
            ("Pádel", [(2019, 2026)], "fecha inicio ¿?"),
        ]),
        ("FORMACIÓN:", [
            ("Python Coursera", [(2020, 2020)], "✓ (mar 2020)"),
            ("Google PM (3 cursos)", [(2022, 2023)], "✓ (nov22-mar23)"),
            ("Mauro (JS+NestJS)", [(2023, 2023)], "(verano 23, app TUP)"),
            ("Codo a Codo FullSt.", [(2023, 2023)], "✓ (feb-jul 23, 208h)"),
            ("PEI A2+ inglés", [(2023, 2023)]),
            ("IFTS18 Datos+IA", [(2023, 2025)], "✓ (egresó 2025)"),
            ("Gen.AI Leader Goog.", [(2025, 2025)]),
            ("Vertex AI badge", [(2025, 2025)]),
        ]),
        ("CLUBES (socio deportivo):", [
            ("CASA", [(2014, 2014)]),
            ("Lambroth a Kol", [(2015, 2018)]),
            ("Hacoaj", [(2019, 2026)], "← hasta hoy"),
        ]),
        ("PERSONAL:", [
            ("Matrimonio Natalia", [(2014, 2026)], "← continúa"),
            ("Bar Mitzvá Uriel", [(2020, 2020)], "(5/3/2020)"),
            ("Bat Mitzvá Sol", [(2021, 2021)], "(fecha ¿?)"),
            ("† Fortuna (madre)", [(2024, 2024)], "(marzo 2024)"),
            ("Bar Mitzvá Matías", [(2024, 2024)], "(7/10/2024)"),
            ("† Aharon (suegro)", [(2025, 2025)], "(jul/ago 2025)"),
        ]),
    ]
))

print()
print("=" * 95)
print("  ANÁLISIS DE CARGA LABORAL POR AÑO (solo trabajos, no colonias de verano)")
print("=" * 95)

# Definir todos los trabajos con sus períodos (sin colonias de verano que son estacionales)
trabajos = {
    # Era 1 (1993-2013)
    "Port. eléctricos":   (1993, 1993),
    "Hebraica":           (1994, 1995),
    "Mi Refugio CC":      (1996, 2012),
    "CSHA Dir.Cultura":   (2012, 2013),
    "Bialik de Devoto":   (1996, 1997),
    "Ser Dinámico":       (1996, 2017),
    "Personal trainer":   (1996, 2022),
    "Or Torá (Barracas)": (1998, 2001),
    "Esc.fútbol Or Torá": (1999, 2000),
    "Esc.Deport. Filiol": (1998, 1999),
    "Colegio Ruta 11":    (1998, 2000),
    # Era 2 (2014-2026)
    "Asesor.licitaciones":(2014, 2015),
    "Silk Tecnologías":   (2015, 2016),
    "SBD":                (2016, 2026),
    "Uno Mayorista":      (2017, 2019),
    "Muebles+Esteban":    (2020, 2021),
    "Freelancer dev":     (2023, 2024),
    "AiControl Seguridad":(2024, 2026),
    "ARGOS":              (2026, 2026),
}

# Calcular por año
for year in range(1993, 2027):
    age = year - BIRTH_YEAR
    activos = [name for name, (s, e) in trabajos.items() if s <= year <= e]
    n = len(activos)
    bar = "█" * n
    marker = " ◄◄◄ PICO" if n >= 7 else (" ◄◄" if n >= 5 else "")
    print(f"  {year} ({age:2d} años) │ {n} trabajos │ {bar:20s} │ {', '.join(activos)}{marker}")

# Encontrar el pico
max_year = max(range(1993, 2027), key=lambda y: len([n for n, (s, e) in trabajos.items() if s <= y <= e]))
max_count = len([n for n, (s, e) in trabajos.items() if s <= max_year <= e])
max_age = max_year - BIRTH_YEAR
print(f"\n  ★ PICO MÁXIMO: {max_count} trabajos simultáneos en {max_year} (edad {max_age})")

# Si incluimos colonias de verano
colonias = {
    "Colonia Hebraica":  (1995, 2000),
    "Colonia Mi Refugio":(1996, 2012),
    "Colonia Barkojba":  (1998, 2002),
}
todos = {**trabajos, **colonias}
max_year_all = max(range(1993, 2027), key=lambda y: len([n for n, (s, e) in todos.items() if s <= y <= e]))
max_count_all = len([n for n, (s, e) in todos.items() if s <= max_year_all <= e])
activos_all = [n for n, (s, e) in todos.items() if s <= max_year_all <= e]
print(f"  ★ CON COLONIAS: {max_count_all} actividades laborales en {max_year_all} (edad {max_year_all - BIRTH_YEAR})")
print(f"    → {', '.join(activos_all)}")

print()
print("=" * 95)
print("  Superposiciones destacadas:")
print("  • 1983-84 (10-11): Fútbol + Natación + Tenis mesa + Kung fu (4 deportes simultáneos)")
print("  • 1987-88 (14-15): Secundario + Fútbol + Kung fu")
print("  • 1989-92 (16-19): Secundario + Rikudim + Agshama + Madrich")
print("  • 1993-94 (20-21): IMEF + Danza jazz + Porteros/Hebraica")
print("  • 1996-97 (23-24): Mi Refugio + Bialik + Ser Dinámico/PT + Col.Hebraica + Col.Mi Refugio (5-6)")
print("  • 1998-2000 (25-27): PICO → Mi Refugio + Ser Dinámico/PT + Or Torá + Filiol + Ruta 11 + colonias (7-10!)")
print("  • 2001-04 (28-31): Mi Refugio + Ser Dinámico/PT + Or Torá + Teatro Sábato")
print("  • 2005-06 (32-33): Mi Refugio + Ser Dinámico/PT + Esc.Teatro Rubén")
print("  • 2007-10 (34-37): Mi Refugio + Ser Dinámico/PT + Clown (+ PNL en 10)")
print("  • 2011-12 (38-39): Mi Refugio + Ser Dinámico/PT + FEMEC + UNSAM + nace Matías")
print("  • 2014-17 (41-44): Asesor/Silk/SBD + Ser Dinámico + Personal trainer (3 trabajos)")
print("  • 2020-21 (47-48): SBD + Muebles Esteban + Personal trainer (3 trabajos)")
print("  • 2023 (50): Año explosivo — SBD + Freelancer + IFTS18 + Codo a Codo + Google PM + Mauro + PEI")
print("=" * 95)
print()
print("  Casado con Natalia desde 2002 (24 años de matrimonio). Novios desde ~1997.")
print("  Estado actual SBD: en búsqueda activa para salir.")
