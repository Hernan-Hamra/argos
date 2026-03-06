"""
Form Filler - Herramienta genérica para completar formularios documentales.

Enfoque: detectar campos (espacios entre labels), calcular área disponible,
e insertar texto centrado sin pisar labels ni bordes.

Compatible: Windows, macOS, WSL/Linux.
Formatos entrada: PDF
Formatos salida: PDF, PNG, JPG, HTML (multi-página)

Uso genérico:
    from tools.pdf_form_filler import FormFiller
    filler = FormFiller("formulario.pdf")
    filler.add_field("empresa", page=1, x=100, y=200, width=150, height=12)
    filler.set_value("empresa", "SOFTWARE BY DESIGN S.A.")
    filler.save("completado.pdf")                    # PDF
    filler.export("completado.png", pages=[3])        # PNG por página
    filler.export("completado.jpg", pages=[3,4])      # JPG por página
    filler.export("completado.html")                  # HTML multi-página

Uso Woranz:
    from tools.pdf_form_filler import fill_woranz
    fill_woranz()
"""
import fitz
import os
import platform
from pathlib import Path


# ── FormFiller genérico ──────────────────────────────────────────────────────

class FormFiller:
    """Rellena formularios PDF insertando texto en campos definidos."""

    def __init__(self, input_path):
        self.input_path = str(input_path)
        self.doc = fitz.open(self.input_path)
        self.fields = {}   # name -> FieldDef
        self.values = {}   # name -> value

    class FieldDef:
        """Definición de un campo en el formulario."""
        def __init__(self, page, x, y, width, height=12, fontsize=9,
                     font="helv", align="left", field_type="text",
                     color=(0, 0, 0), padding_left=2, padding_top=0):
            self.page = page          # 0-indexed
            self.x = x               # x inicio del área del campo
            self.y = y               # y inicio del área del campo (top)
            self.width = width        # ancho disponible para texto
            self.height = height      # alto del campo
            self.fontsize = fontsize
            self.font = font
            self.align = align        # left, center, right
            self.field_type = field_type  # text, check
            self.color = color
            self.padding_left = padding_left
            self.padding_top = padding_top

        @property
        def rect(self):
            return fitz.Rect(self.x, self.y, self.x + self.width, self.y + self.height)

    def add_field(self, name, page, x, y, width, height=12, fontsize=9,
                  font="helv", align="left", field_type="text",
                  color=(0, 0, 0), padding_left=2, padding_top=0):
        """Define un campo en el formulario."""
        self.fields[name] = self.FieldDef(
            page=page, x=x, y=y, width=width, height=height,
            fontsize=fontsize, font=font, align=align,
            field_type=field_type, color=color,
            padding_left=padding_left, padding_top=padding_top
        )

    def set_value(self, name, value):
        """Asigna un valor a un campo."""
        self.values[name] = value

    def set_values(self, data_dict):
        """Asigna múltiples valores desde un dict."""
        self.values.update(data_dict)

    def _write_text(self, page, field, text):
        """Escribe texto dentro de un campo respetando límites."""
        if not text:
            return
        text = str(text)
        f = fitz.Font(field.font)
        text_width = f.text_length(text, fontsize=field.fontsize)

        # Calcular posición x según alineación
        available = field.width - field.padding_left * 2
        if field.align == "center":
            x = field.x + field.padding_left + (available - text_width) / 2
        elif field.align == "right":
            x = field.x + field.width - field.padding_left - text_width
        else:  # left
            x = field.x + field.padding_left

        # Clamp x para no salirse del campo
        x = max(x, field.x + field.padding_left)

        # Posición y: centrar verticalmente en el campo
        y = field.y + field.height - field.padding_top - (field.height - field.fontsize) / 2

        # Truncar texto si excede el ancho
        if text_width > available and available > 0:
            while f.text_length(text, fontsize=field.fontsize) > available and len(text) > 1:
                text = text[:-1]

        tw = fitz.TextWriter(page.rect)
        tw.append((x, y), text, fontsize=field.fontsize, font=f)
        tw.write_text(page, color=field.color)

    def _write_check(self, page, field):
        """Escribe una X de checkbox centrada en el campo."""
        f = fitz.Font(field.font)
        mark = "X"
        mark_width = f.text_length(mark, fontsize=field.fontsize)
        x = field.x + (field.width - mark_width) / 2
        y = field.y + field.height - (field.height - field.fontsize) / 2
        tw = fitz.TextWriter(page.rect)
        tw.append((x, y), mark, fontsize=field.fontsize, font=f)
        tw.write_text(page, color=field.color)

    def fill(self):
        """Rellena todos los campos con sus valores."""
        for name, field in self.fields.items():
            value = self.values.get(name)
            if value is None or value == '':
                continue
            page = self.doc[field.page]
            if field.field_type == 'check' and value:
                self._write_check(page, field)
            else:
                self._write_text(page, field, value)

    def verify(self):
        """
        Auto-verificación: extrae texto del PDF llenado y verifica que cada
        campo fue escrito correctamente (no truncado, no fuera de área).
        Retorna lista de problemas encontrados.
        """
        problems = []
        self.fill()
        for name, field in self.fields.items():
            value = self.values.get(name)
            if not value or value == '' or field.field_type == 'check':
                continue
            value = str(value)
            page = self.doc[field.page]
            # Buscar el texto insertado en el área del campo (con margen)
            search_rect = fitz.Rect(
                field.x - 2, field.y - 2,
                field.x + field.width + 2, field.y + field.height + 2
            )
            found_text = page.get_text("text", clip=search_rect).strip()
            # Verificar que el texto aparece completo
            if value not in found_text and found_text not in value:
                # Puede estar truncado
                if len(found_text) > 0 and len(found_text) < len(value) * 0.8:
                    problems.append({
                        'field': name,
                        'expected': value,
                        'found': found_text,
                        'issue': 'truncado',
                        'page': field.page + 1,
                    })
            # Verificar que el texto no se sale del campo
            f = fitz.Font(field.font)
            text_width = f.text_length(value, fontsize=field.fontsize)
            available = field.width - field.padding_left * 2
            if text_width > available * 1.05:  # 5% tolerance
                problems.append({
                    'field': name,
                    'expected': value,
                    'issue': f'desborda ({text_width:.0f}px > {available:.0f}px disponible)',
                    'page': field.page + 1,
                })
        return problems

    def fill_and_verify(self, output_path, max_iterations=3):
        """
        Llena el formulario y ejecuta N rondas de auto-verificación.
        En cada ronda, detecta problemas y ajusta automáticamente.
        Retorna (path, problemas_restantes).
        """
        self.fill()
        all_problems = []
        for iteration in range(max_iterations):
            problems = self.verify()
            if not problems:
                print(f"  Verificación {iteration+1}/{max_iterations}: OK — sin problemas")
                break
            print(f"  Verificación {iteration+1}/{max_iterations}: {len(problems)} problema(s)")
            fixed = 0
            for p in problems:
                if p['issue'] == 'truncado' or 'desborda' in p['issue']:
                    field = self.fields[p['field']]
                    # Auto-fix: reducir fontsize 1pt
                    if field.fontsize > 5:
                        old_fs = field.fontsize
                        field.fontsize -= 1
                        print(f"    → {p['field']}: fontsize {old_fs} → {field.fontsize}")
                        fixed += 1
            if fixed == 0:
                all_problems = problems
                break
            # Re-render con los ajustes
            self.doc.close()
            self.doc = fitz.open(self.input_path)
            self.fill()
        else:
            all_problems = self.verify()

        output_path = str(output_path)
        self.doc.save(output_path)
        return output_path, all_problems

    def save(self, output_path):
        """Guarda el PDF completado."""
        self.fill()
        output_path = str(output_path)
        self.doc.save(output_path)
        return output_path

    def close(self):
        """Cierra el documento."""
        self.doc.close()

    def export(self, output_path, pages=None, dpi=150, quality=95):
        """
        Exporta el formulario completado a múltiples formatos.

        Args:
            output_path: Path de salida. El formato se deduce de la extensión:
                .pdf → PDF, .png → PNG, .jpg/.jpeg → JPG, .html → HTML multi-página
            pages: Lista de páginas a exportar (1-indexed). None = todas.
            dpi: Resolución para formatos imagen (default 150).
            quality: Calidad JPEG 0-100 (default 95).

        Returns:
            Lista de paths generados (uno por archivo).
        """
        self.fill()
        output_path = Path(output_path)
        ext = output_path.suffix.lower()
        total_pages = len(self.doc)
        page_list = pages or list(range(1, total_pages + 1))
        results = []

        if ext == '.pdf':
            self.doc.save(str(output_path))
            results.append(str(output_path))

        elif ext in ('.png', '.jpg', '.jpeg'):
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            for p in page_list:
                page = self.doc[p - 1]
                pix = page.get_pixmap(matrix=mat)
                if len(page_list) == 1:
                    fname = output_path
                else:
                    fname = output_path.with_name(f"{output_path.stem}_p{p}{ext}")
                if ext in ('.jpg', '.jpeg'):
                    pix.save(str(fname), jpg_quality=quality)
                else:
                    pix.save(str(fname))
                results.append(str(fname))

        elif ext == '.html':
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            html_parts = ['<!DOCTYPE html><html><head><meta charset="utf-8">',
                          '<style>body{background:#eee;text-align:center;font-family:sans-serif}',
                          'img{max-width:100%;margin:10px auto;display:block;box-shadow:0 2px 8px rgba(0,0,0,.2)}</style>',
                          '</head><body>']
            import base64
            for p in page_list:
                page = self.doc[p - 1]
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                b64 = base64.b64encode(img_data).decode()
                html_parts.append(f'<h3>Página {p}</h3>')
                html_parts.append(f'<img src="data:image/png;base64,{b64}" alt="Página {p}">')
            html_parts.append('</body></html>')
            output_path.write_text('\n'.join(html_parts), encoding='utf-8')
            results.append(str(output_path))

        else:
            raise ValueError(f"Formato no soportado: {ext}. Use .pdf, .png, .jpg o .html")

        return results

    def render_page(self, page_num, output_path=None, dpi=150):
        """Renderiza una página como PNG para revisión visual."""
        page = self.doc[page_num - 1]
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        if output_path is None:
            out_dir = Path(__file__).parent.parent / 'output'
            out_dir.mkdir(exist_ok=True)
            output_path = str(out_dir / f'form_p{page_num}.png')
        pix.save(str(output_path))
        return str(output_path)

    def detect_fields(self, page_num):
        """
        Detecta campos potenciales en una página analizando labels y espacios.
        Útil para mapear un formulario nuevo.
        Retorna lista de dicts con label, posición estimada del campo.
        """
        page = self.doc[page_num]
        blocks = page.get_text('dict')['blocks']
        detected = []
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    bbox = span['bbox']
                    if text.endswith(':') and len(text) > 2:
                        detected.append({
                            'label': text,
                            'label_bbox': list(bbox),
                            'field_x': bbox[2] + 4,
                            'field_y': bbox[1],
                            'field_height': bbox[3] - bbox[1],
                            'estimated_width': 150,
                            'fontsize': span['size'],
                            'page': page_num,
                        })
        return detected


# ── Helpers cross-platform ───────────────────────────────────────────────────

def _resolve_path(path):
    """Resuelve path independiente de plataforma."""
    return str(Path(path).resolve())


def render_page(pdf_path, page_num, output_png=None, dpi=150):
    """Renderiza una página de un PDF como PNG."""
    doc = fitz.open(str(pdf_path))
    page = doc[page_num - 1]
    zoom = dpi / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    if output_png is None:
        out_dir = Path(__file__).parent.parent / 'output'
        out_dir.mkdir(exist_ok=True)
        output_png = str(out_dir / f'form_p{page_num}.png')
    pix.save(str(output_png))
    doc.close()
    return str(output_png)


# ── Woranz: definición específica ────────────────────────────────────────────

def _get_woranz_source():
    """Encuentra el PDF original de Woranz (multiplataforma)."""
    # Intentar paths conocidos según plataforma
    candidates = [
        Path(r'C:\Users\HERNAN\OneDrive - SOFTWARE BY DESIGN SA\5. ORGANIZACION\2 DOC SBD'),
        Path.home() / 'OneDrive - SOFTWARE BY DESIGN SA' / '5. ORGANIZACION' / '2 DOC SBD',
        Path('/mnt/c/Users/HERNAN/OneDrive - SOFTWARE BY DESIGN SA/5. ORGANIZACION/2 DOC SBD'),  # WSL
    ]
    # También buscar via config.py si existe
    try:
        from tools.config import PATHS
        if 'doc_sbd' in PATHS:
            candidates.insert(0, Path(PATHS['doc_sbd']))
    except (ImportError, KeyError):
        pass

    for folder in candidates:
        if folder.exists():
            for f in folder.iterdir():
                if 'Woranz' in f.name and 'COMPLETADA' not in f.name and f.suffix == '.pdf':
                    return str(f)

    raise FileNotFoundError(
        "No se encontró el PDF original de Woranz. "
        "Buscado en: " + ", ".join(str(c) for c in candidates)
    )


def _define_woranz_fields(filler):
    """Define los campos del formulario Woranz con coordenadas exactas."""

    # ── PÁGINA 1 (idx 0): Firma carta de vinculación ──
    # Labels: Firma(51,688), Aclaración(318,688), DNI(51,717), Cargo(319,716)
    # Domicilio: campo G) constituimos domicilio en _______
    filler.add_field('p1_aclaracion', page=0, x=358, y=686, width=190, height=13, fontsize=8)
    filler.add_field('p1_dni',        page=0, x=68,  y=715, width=240, height=13, fontsize=8)
    filler.add_field('p1_cargo',      page=0, x=344, y=715, width=200, height=13, fontsize=8)

    # ── PÁGINA 2 (idx 1): Firma al pie ──
    # Labels detectados: Empresa(42-74), Cargo(309-330), Domicilio(42-75), Tel(309-359), Email(42-65), Aclaración(309-346)
    filler.add_field('p2_empresa',    page=1, x=76,  y=636, width=220, height=13, fontsize=8)
    filler.add_field('p2_cargo',      page=1, x=332, y=636, width=210, height=13, fontsize=8)
    filler.add_field('p2_domicilio',  page=1, x=78,  y=664, width=220, height=13, fontsize=8)
    filler.add_field('p2_telefono',   page=1, x=362, y=664, width=180, height=13, fontsize=8)
    filler.add_field('p2_email',      page=1, x=68,  y=692, width=230, height=13, fontsize=8)
    filler.add_field('p2_aclaracion', page=1, x=348, y=738, width=200, height=13, fontsize=8)

    # ── PÁGINA 3 (idx 2): Header empresa ──
    # Lugar:(41-65) → campo desde 68.  Fecha:(305-328) → campo desde 332.
    # "de" separators at x=373 and x=431
    filler.add_field('p3_lugar',       page=2, x=68,  y=116, width=230, height=13, fontsize=8)
    filler.add_field('p3_fecha_dia',   page=2, x=332, y=116, width=38,  height=13, fontsize=8, align="center")
    filler.add_field('p3_fecha_mes',   page=2, x=385, y=116, width=43,  height=13, fontsize=8, align="center")
    filler.add_field('p3_fecha_anio',  page=2, x=443, y=115, width=50,  height=13, fontsize=8, align="center")

    # Razón social / inscripción
    filler.add_field('p3_razon_social',     page=2, x=152, y=133, width=120, height=13, fontsize=8)
    filler.add_field('p3_nro_inscripcion',  page=2, x=397, y=133, width=155, height=13, fontsize=7)
    filler.add_field('p3_fecha_inscripcion', page=2, x=118, y=148, width=110, height=13, fontsize=8)
    filler.add_field('p3_actividad',        page=2, x=272, y=148, width=280, height=13, fontsize=7)
    filler.add_field('p3_fecha_contrato',   page=2, x=262, y=163, width=100, height=13, fontsize=8)
    filler.add_field('p3_cuit',             page=2, x=62,  y=178, width=160, height=13, fontsize=8)
    filler.add_field('p3_act_principal',    page=2, x=302, y=178, width=250, height=13, fontsize=7)
    filler.add_field('p3_domicilio_legal',  page=2, x=100, y=193, width=125, height=13, fontsize=7)
    filler.add_field('p3_localidad',        page=2, x=268, y=193, width=58,  height=13, fontsize=7)
    filler.add_field('p3_cp',               page=2, x=386, y=193, width=25,  height=13, fontsize=7, align="center")
    filler.add_field('p3_provincia',        page=2, x=451, y=193, width=24,  height=13, fontsize=7, align="center")
    filler.add_field('p3_pais',             page=2, x=499, y=193, width=54,  height=13, fontsize=7)
    filler.add_field('p3_telefono_sede',    page=2, x=117, y=209, width=108, height=13, fontsize=7)
    filler.add_field('p3_email_sede',       page=2, x=300, y=209, width=250, height=13, fontsize=7)

    # Representante Legal checkbox SI
    # "SI" exact rect: (309.3, 237.0, 317.2, 249.2)  "NO" rect: (333.5, 237.0, 347.0, 249.2)
    filler.add_field('p3_rep_si', page=2, x=309.3, y=237.0, width=7.9, height=12.2, fontsize=9, field_type="check")

    # ── Datos del representante ──
    # Nombre y apellido:(40-115) → campo desde 118
    filler.add_field('p3_rep_nombre',     page=2, x=118, y=304, width=430, height=14, fontsize=9)
    filler.add_field('p3_rep_lugar_nac',  page=2, x=130, y=320, width=128, height=14, fontsize=9)
    # Fecha nacimiento: separada por "de" en x=418 y x=484
    filler.add_field('p3_rep_fn_dia',     page=2, x=355, y=320, width=58,  height=14, fontsize=9, align="center")
    filler.add_field('p3_rep_fn_mes',     page=2, x=432, y=320, width=48,  height=14, fontsize=9, align="center")
    filler.add_field('p3_rep_fn_anio',    page=2, x=498, y=320, width=55,  height=14, fontsize=9, align="center")
    filler.add_field('p3_rep_nacionalidad', page=2, x=98,  y=336, width=160, height=14, fontsize=9)
    filler.add_field('p3_rep_tipo_doc',   page=2, x=367, y=336, width=185, height=14, fontsize=9)
    # Sexo: M(72) F  Estado Civil: — checkbox M
    filler.add_field('p3_rep_sexo_m',     page=2, x=69,  y=351, width=12,  height=15, fontsize=9, field_type="check")
    filler.add_field('p3_rep_estado_civil', page=2, x=166, y=351, width=90,  height=15, fontsize=9)
    filler.add_field('p3_rep_cuit',       page=2, x=313, y=351, width=240, height=15, fontsize=9)
    # Ocupación label ends at x=240
    filler.add_field('p3_rep_ocupacion',  page=2, x=243, y=383, width=310, height=14, fontsize=9)
    filler.add_field('p3_rep_domicilio',  page=2, x=103, y=399, width=168, height=14, fontsize=9)
    filler.add_field('p3_rep_localidad',  page=2, x=317, y=399, width=235, height=14, fontsize=9)
    filler.add_field('p3_rep_cp',         page=2, x=101, y=415, width=168, height=14, fontsize=9)
    filler.add_field('p3_rep_provincia',  page=2, x=318, y=415, width=235, height=14, fontsize=9)
    filler.add_field('p3_rep_telefono',   page=2, x=80,  y=430, width=188, height=15, fontsize=9)
    filler.add_field('p3_rep_email',      page=2, x=353, y=430, width=200, height=15, fontsize=9)

    # Beneficiarios finales: checkbox "Existen"
    # "No existen" checkbox at y=549, "Existen" at y=560
    filler.add_field('p3_benef_existen', page=2, x=60, y=557, width=14, height=14, fontsize=9, field_type="check")

    # Tabla beneficiarios — líneas reales: y=620, 638.3, 656.7, 675.0 | cols: x=41, 208.7, 326.6, 433.7, 544
    # Row 1: entre y=620 y y=638.3 (height=18.3), Row 2: entre y=638.3 y y=656.7
    R1Y = 620;  R1H = 18.3
    R2Y = 638.3; R2H = 18.4
    filler.add_field('p3_b1_nombre', page=2, x=43,    y=R1Y, width=163, height=R1H, fontsize=7)
    filler.add_field('p3_b1_doc',    page=2, x=210.7, y=R1Y, width=114, height=R1H, fontsize=6)
    filler.add_field('p3_b1_nac',    page=2, x=328.6, y=R1Y, width=103, height=R1H, fontsize=7, align="center")
    filler.add_field('p3_b1_pct',    page=2, x=435.7, y=R1Y, width=106, height=R1H, fontsize=7, align="center")
    filler.add_field('p3_b2_nombre', page=2, x=43,    y=R2Y, width=163, height=R2H, fontsize=7)
    filler.add_field('p3_b2_doc',    page=2, x=210.7, y=R2Y, width=114, height=R2H, fontsize=6)
    filler.add_field('p3_b2_nac',    page=2, x=328.6, y=R2Y, width=103, height=R2H, fontsize=7, align="center")
    filler.add_field('p3_b2_pct',    page=2, x=435.7, y=R2Y, width=106, height=R2H, fontsize=7, align="center")

    # ── PÁGINA 4 (idx 3): Capital social, PEP, Sujeto Obligado ──
    # Tabla capital social — líneas: y=160.3, 178.6, 196.9, 215.3 | cols: x=34.3, 201.9, 319.8, 426.9, 537.3
    # Row 1: y=160.3 to 178.6 (h=18.3), Row 2: y=178.6 to 196.9 (h=18.3)
    CS1Y = 160.3; CS2Y = 178.6; CSH = 18.3
    filler.add_field('p4_s1_nombre', page=3, x=36.3,  y=CS1Y, width=163, height=CSH, fontsize=7)
    filler.add_field('p4_s1_doc',    page=3, x=203.9, y=CS1Y, width=114, height=CSH, fontsize=6)
    filler.add_field('p4_s1_nac',    page=3, x=321.8, y=CS1Y, width=103, height=CSH, fontsize=7, align="center")
    filler.add_field('p4_s1_pct',    page=3, x=428.9, y=CS1Y, width=106, height=CSH, fontsize=7, align="center")
    filler.add_field('p4_s2_nombre', page=3, x=36.3,  y=CS2Y, width=163, height=CSH, fontsize=7)
    filler.add_field('p4_s2_doc',    page=3, x=203.9, y=CS2Y, width=114, height=CSH, fontsize=6)
    filler.add_field('p4_s2_nac',    page=3, x=321.8, y=CS2Y, width=103, height=CSH, fontsize=7, align="center")
    filler.add_field('p4_s2_pct',    page=3, x=428.9, y=CS2Y, width=106, height=CSH, fontsize=7, align="center")

    # PEP: "NO" exact rect: (52.6, 348.7, 66.1, 360.9) — X a la derecha del "NO"
    filler.add_field('p4_pep_no', page=3, x=67, y=348.7, width=12, height=12.2, fontsize=9, field_type="check")

    # Sujeto Obligado: "No" exact rect: (237.6, 492.5, 249.2, 504.7) — X a la derecha del "No"
    filler.add_field('p4_so_no', page=3, x=250, y=492.5, width=12, height=12.2, fontsize=9, field_type="check")

    # Firma página 4
    filler.add_field('p4_aclaracion', page=3, x=348, y=712, width=200, height=13, fontsize=8)
    filler.add_field('p4_dni',        page=3, x=348, y=736, width=200, height=13, fontsize=8)

    # ── PÁGINA 7 (idx 6): Firma al pie ──
    filler.add_field('p7_aclaracion', page=6, x=348, y=712, width=200, height=13, fontsize=8)


def _load_woranz_data():
    """Carga datos para el formulario Woranz desde la DB."""
    from tools.tracker import get_connection
    conn = get_connection()
    c = conn.cursor()

    # Empresa
    emp_rows = c.execute("SELECT campo, valor FROM empresa_datos").fetchall()
    emp = {r[0]: r[1] for r in emp_rows}

    # Hernán (id=12)
    hernan = c.execute("SELECT * FROM personas WHERE id=12").fetchone()
    h_cols = [d[0] for d in c.description]
    h = {h_cols[i]: hernan[i] for i in range(len(h_cols))} if hernan else {}

    # Marcelo (id=2)
    marcelo = c.execute("SELECT * FROM personas WHERE id=2").fetchone()
    m_cols = [d[0] for d in c.description]
    m = {m_cols[i]: marcelo[i] for i in range(len(m_cols))} if marcelo else {}

    conn.close()

    fn = str(h.get('fecha_nacimiento', '')).split('-')

    return {
        # Página 1 - Firma carta vinculación
        'p1_aclaracion': h.get('nombre', ''),
        'p1_dni': f"DNI {h.get('dni', '')}",
        'p1_cargo': 'Apoderado',

        # Página 2
        'p2_empresa': emp.get('razon_social', ''),
        'p2_cargo': 'Apoderado',
        'p2_domicilio': emp.get('domicilio_legal', ''),
        'p2_telefono': emp.get('telefono', ''),
        'p2_email': emp.get('email', ''),
        'p2_aclaracion': h.get('nombre', ''),

        # Página 3 header
        'p3_lugar': 'Buenos Aires',
        'p3_fecha_dia': '',  # se setea en fill_woranz
        'p3_fecha_mes': '',
        'p3_fecha_anio': '',
        'p3_razon_social': emp.get('razon_social', ''),
        'p3_nro_inscripcion': emp.get('nro_inscripcion_igj', ''),
        'p3_fecha_inscripcion': '16/06/2011',
        'p3_actividad': 'Tecnología, cableado, seguridad electrónica',
        'p3_fecha_contrato': '07/06/2011',
        'p3_cuit': emp.get('cuit', ''),
        'p3_act_principal': 'Serv. tecnología, cableado, seguridad',
        'p3_domicilio_legal': 'Uspallata 2977 P1 D19',
        'p3_localidad': 'CABA',
        'p3_cp': 'C1437',
        'p3_provincia': 'CABA',
        'p3_pais': 'Argentina',
        'p3_telefono_sede': emp.get('telefono', ''),
        'p3_email_sede': emp.get('email', ''),

        # Representante
        'p3_rep_si': True,
        'p3_rep_nombre': h.get('nombre', ''),
        'p3_rep_lugar_nac': h.get('lugar_nacimiento', ''),
        'p3_rep_fn_dia': fn[2] if len(fn) == 3 else '',
        'p3_rep_fn_mes': fn[1] if len(fn) == 3 else '',
        'p3_rep_fn_anio': fn[0] if len(fn) == 3 else '',
        'p3_rep_nacionalidad': h.get('nacionalidad', ''),
        'p3_rep_tipo_doc': f"DNI {h.get('dni', '')}",
        'p3_rep_sexo_m': True,
        'p3_rep_estado_civil': h.get('estado_civil', ''),
        'p3_rep_cuit': h.get('cuit', ''),
        'p3_rep_ocupacion': 'Gerente de Proyectos',
        'p3_rep_domicilio': 'Av. Ricardo Balbín 2535 2D',
        'p3_rep_localidad': 'CABA',
        'p3_rep_cp': 'C1428',
        'p3_rep_provincia': 'CABA',
        'p3_rep_telefono': '+54 11 5317-1213',
        'p3_rep_email': 'hamrahernan@gmail.com',

        # Beneficiarios finales
        'p3_benef_existen': True,
        'p3_b1_nombre': 'Marcelo Ariel Hamra',
        'p3_b1_doc': f"DNI {m.get('dni','')} / CUIT {m.get('cuit','')}",
        'p3_b1_nac': 'Argentina',
        'p3_b1_pct': '50%',
        'p3_b2_nombre': 'Jorge Ricardo Serrats',
        'p3_b2_doc': 'DNI 22.430.271 / CUIT 20-22430271-2',
        'p3_b2_nac': 'Argentina',
        'p3_b2_pct': '50%',

        # Capital social (pág 4)
        'p4_s1_nombre': 'Marcelo Ariel Hamra',
        'p4_s1_doc': f"DNI {m.get('dni','')} / CUIT {m.get('cuit','')}",
        'p4_s1_nac': 'Argentina',
        'p4_s1_pct': '50%',
        'p4_s2_nombre': 'Jorge Ricardo Serrats',
        'p4_s2_doc': 'DNI 22.430.271 / CUIT 20-22430271-2',
        'p4_s2_nac': 'Argentina',
        'p4_s2_pct': '50%',

        # PEP y Sujeto Obligado
        'p4_pep_no': True,
        'p4_so_no': True,

        # Firmas
        'p4_aclaracion': h.get('nombre', ''),
        'p4_dni': f"DNI {h.get('dni', '')}",
        'p7_aclaracion': h.get('nombre', ''),
    }


def fill_woranz(output_path=None, fecha=None):
    """
    Completa el formulario Woranz con datos de SBD.

    Args:
        output_path: Path de salida (default: v3 en misma carpeta).
        fecha: date para el documento (default: hoy).

    Returns:
        Path del PDF generado.
    """
    from datetime import date
    meses = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
             'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    input_path = _get_woranz_source()
    if output_path is None:
        folder = str(Path(input_path).parent)
        output_path = os.path.join(folder, 'Woranz - Carta Vinculacion PEP SO - COMPLETADA SBD v3.pdf')

    filler = FormFiller(input_path)
    _define_woranz_fields(filler)

    data = _load_woranz_data()

    # Fecha del documento
    if fecha:
        data['p3_fecha_dia'] = str(fecha.day)
        data['p3_fecha_mes'] = meses[fecha.month]
        data['p3_fecha_anio'] = str(fecha.year)
    else:
        data['p3_fecha_dia'] = ''
        data['p3_fecha_mes'] = ''
        data['p3_fecha_anio'] = ''

    filler.set_values(data)
    result, problems = filler.fill_and_verify(output_path, max_iterations=3)
    filler.close()
    if problems:
        print(f"PDF generado con {len(problems)} advertencia(s):")
        for p in problems:
            print(f"  ⚠ pág {p['page']} campo '{p['field']}': {p['issue']}")
    else:
        print(f"PDF generado: {result} — verificación OK")
    return result


if __name__ == '__main__':
    from datetime import date
    result = fill_woranz(fecha=date(2026, 2, 24))

    for p in [2, 3, 4]:
        png = render_page(result, p)
        print(f"Página {p}: {png}")
