# ARGOS Tools

Módulos reutilizables para la preparación de licitaciones.

---

## doc_generator.py — Generador de documentos Word

Crea documentos `.docx` desde un template existente, preservando header/footer con membrete corporativo.

**Funciones:**

- **`load_template(path)`**
  Carga un `.docx` como template. Limpia el body pero conserva `sectPr` (encabezado/pie con membrete). Devuelve un objeto `Document`.

- **`add_para(doc, text, ...)`**
  Agrega un párrafo con formato completo (font, size, bold, color, alignment). Usa lxml para forzar `rFonts` (sin esto Word ignora el font).

- **`add_separator(doc)`**
  Inserta línea separadora centrada en azul corporativo.

- **`add_firma(doc, nombre, cargo, empresa)`**
  Agrega bloque de firma estándar (línea + nombre + cargo + empresa).

**Uso típico:**
```python
from tools.doc_generator import load_template, add_para, add_firma

doc = load_template(r'C:\ruta\template_con_membrete.docx')
add_para(doc, 'TÍTULO', bold=True, size=14)
add_para(doc, 'Texto del documento...')
add_firma(doc, 'Hernán Hamra', 'Apoderado', 'SOFTWARE BY DESIGN S.A.')
doc.save(r'C:\ruta\salida.docx')
```

**Dependencias:** `python-docx`, `lxml`

---

## pdf_converter.py — Conversor DOCX a PDF

Convierte archivos `.docx` a `.pdf` usando Word COM automation (Microsoft Word debe estar instalado).

**Funciones:**

- **`kill_word()`**
  Cierra cualquier instancia de Word abierta (evita conflictos COM).

- **`docx_to_pdf(docx_path, pdf_path=None)`**
  Convierte un `.docx` a PDF. Si no se indica `pdf_path`, genera el PDF en el mismo directorio. Devuelve el path del PDF.

- **`batch_docx_to_pdf(docx_dir, pdf_dir=None)`**
  Convierte todos los `.docx` de un directorio. Abre Word una sola vez para mejor rendimiento.

**Uso típico:**
```python
from tools.pdf_converter import docx_to_pdf, batch_docx_to_pdf

# Un archivo
docx_to_pdf(r'C:\docs\documento.docx')

# Todos los .docx de una carpeta
batch_docx_to_pdf(r'C:\docs\carpeta_b', pdf_dir=r'C:\docs\pdfs')
```

**Importante:** Siempre cierra Word antes de ejecutar (`kill_word()` se llama automáticamente).

**Dependencias:** `pywin32` (solo Windows)

---

## foliador.py — Merge y foliación de PDFs

Combina múltiples PDFs en uno solo y agrega número de folio a cada página.

**Funciones:**

- **`merge_and_foliate(pdf_list, output_path, ...)`**
  Recibe lista ordenada de PDFs, los une en uno solo y agrega "Folio: N" en cada página.
  Devuelve dict con `total_pages`, `folio_start`, `folio_end`.

- **`print_folio_summary(result)`**
  Imprime tabla resumen con rango de folios por archivo.

**Parámetros de `merge_and_foliate`:**

- `folio_start` (default: 1) — Número del primer folio
- `fontsize` (default: 9) — Tamaño de fuente
- `color` (default: gris 0.3) — Color RGB (0-1)
- `prefix` (default: "Folio: ") — Texto antes del número
- `position` (default: "bottom_right") — Ubicación en la página

**Uso típico:**
```python
from tools.foliador import merge_and_foliate, print_folio_summary

pdfs = [r'C:\docs\01.pdf', r'C:\docs\02.pdf', r'C:\docs\03.pdf']
result = merge_and_foliate(pdfs, r'C:\output\carpeta_a1.pdf', folio_start=1)
print_folio_summary(result)
# Total: 75 folios (del 1 al 75)
```

**Notas:** Salta automáticamente archivos inexistentes o vacíos (0 bytes).

**Dependencias:** `PyMuPDF (fitz)`

---

## cotizacion.py — Análisis de Precios (Anexo VII)

Cálculo de estructura de costos para licitaciones: IVA mix, álgebra inversa, cadena Costo → GG → CF → Beneficio → IVA → Total.

**Funciones:**

- **`calcular_iva_mix(items)`**
  Calcula IVA ponderado entre items al 21% y al 10.5%.
  Devuelve: `iva_21`, `iva_105`, `iva_total`, `pct_efectivo`.

- **`calcular_anexo_vii(target_total, costo_directo, cf_pct, beneficio_pct, iva_monto)`**
  Trabaja hacia atrás desde el total conocido para despejar Gastos Generales (variable libre).
  Devuelve todas las líneas del Anexo VII.

- **`print_anexo_vii(result)`**
  Imprime la tabla del Anexo VII en formato argentino ($ X.XXX.XXX,XX).

**Lógica del álgebra inversa:**
```
Total conocido (ej: $288.898.500,75)
  → restar IVA mix       → Costo Total (línea 12)
  → dividir (1+Beneficio) → Subtotal (línea 10)
  → dividir (1+CF)        → Subtotal (línea 8)
  → restar Costo Directo  → Gastos Generales (línea 7) ← variable libre
```

**Uso típico:**
```python
from tools.cotizacion import calcular_iva_mix, calcular_anexo_vii, print_anexo_vii

# 1. Calcular IVA mix
items = [
    {'neto': 100000, 'iva_pct': 21},    # servicios
    {'neto': 200000, 'iva_pct': 10.5},   # equipamiento informático
]
iva = calcular_iva_mix(items)

# 2. Calcular estructura completa
result = calcular_anexo_vii(
    target_total=288898500.75,
    costo_directo=143255454.92,
    cf_pct=0.07,
    beneficio_pct=0.1723,
    iva_monto=iva['iva_total']
)
print_anexo_vii(result)
```

---

## excel_tools.py — Lectura y escritura Excel

Utilidades para leer y modificar archivos `.xlsx` con openpyxl.

**Funciones:**

- **`read_excel_summary(path)`**
  Lee un Excel y devuelve dict con nombres de hojas y dimensiones (filas x columnas).

- **`read_sheet_data(path, sheet_name, ...)`**
  Lee datos de una hoja específica. Soporta rango (`row_start`, `row_end`, `col_start`, `col_end`).
  `data_only=True` para valores, `False` para fórmulas.

- **`update_cells(path, sheet_name, changes)`**
  Actualiza celdas puntuales. `changes` es lista de `{'row': R, 'col': C, 'value': V}`.

**Uso típico:**
```python
from tools.excel_tools import read_excel_summary, read_sheet_data, update_cells

# Ver estructura del Excel
summary = read_excel_summary(r'C:\docs\presupuesto.xlsx')
# {'Hoja1': {'rows': 50, 'cols': 8}, 'AnexoVII': {'rows': 70, 'cols': 10}}

# Leer datos
data = read_sheet_data(r'C:\docs\presupuesto.xlsx', 'AnexoVII', row_start=60, row_end=70)

# Modificar celdas
update_cells(r'C:\docs\presupuesto.xlsx', 'AnexoVII', [
    {'row': 63, 'col': 4, 'value': '=D62*35.53%'},
    {'row': 65, 'col': 4, 'value': '=D64*7%'},
])
```

**Importante:** Cerrar Excel antes de escribir (OneDrive bloquea archivos abiertos).

**Dependencias:** `openpyxl`
