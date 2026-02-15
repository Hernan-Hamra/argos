# ARGOS - Sistema de Gestión de Licitaciones

## Qué es ARGOS
Herramienta de automatización para preparar licitaciones públicas y privadas en Argentina.
Desarrollado por y para **Software By Design S.A.**

## Empresa
- **Razón social:** SOFTWARE BY DESIGN S.A.
- **CUIT:** 30-70894532-0
- **Domicilio legal:** Uspallata 2977 1°G, CP 1435, CABA
- **Presidente:** Ing. Marcelo Ariel Hamra (Ingeniero en Sistemas - UTN, DNI 20.665.853)
- **Apoderado:** Hernán Hamra (DNI 23.505.172)

## Reglas de trabajo (OBLIGATORIAS)
1. **NUNCA modificar archivos sin mostrar resultado y pedir confirmación**
2. **Solo trabajar sobre lo explícitamente indicado**
3. **No agregar más de lo que dice el pliego** - no inventar requisitos
4. **No fabricar datasheets** - solo datos reales de fabricante
5. **No tocar Excel con hojas helper** de otros proyectos
6. **PPTx en "varios"** son docs intermedios de trabajo - no tocar
7. **Proponer estructuras antes de crear**
8. **Formato argentino:** montos con $ X.XXX.XXX,XX (puntos miles, coma decimal)

## Estructura del proyecto
```
C:\Users\HERNAN\argos\
├── CLAUDE.md                 ← este archivo (reglas del proyecto)
├── tools/                    ← módulos reutilizables
│   ├── doc_generator.py     ← crear docs Word desde template
│   ├── pdf_converter.py     ← docx→PDF via Word COM
│   ├── foliador.py          ← merge PDFs + numeración de folios
│   ├── cotizacion.py        ← análisis de precios, IVA mix, álgebra inversa
│   └── excel_tools.py       ← lectura/escritura Excel
├── projects/                 ← scripts específicos por licitación
│   └── sbase_410_26/        ← LP 410/26 SBASE (feb 2026)
├── templates/                ← templates .docx reutilizables
└── output/                   ← archivos temporales generados
```

## Stack técnico
- **Python 3.12.1** en C:\Python312 (usar `python`, NO `python3`)
- **python-docx + lxml**: manipulación .docx a nivel XML
- **win32com.client**: Word COM automation para docx→PDF
  - SIEMPRE hacer `taskkill /f /im WINWORD.EXE` antes de usar
- **PyMuPDF (fitz)**: merge PDF, foliación, extracción texto
- **openpyxl**: Excel (data_only=True para valores, False para fórmulas)
- **requests**: descarga de datasheets

## Patrones técnicos clave

### Paths de OneDrive
- Siempre usar raw strings `r''` en Python
- NUNCA usar heredoc en bash para paths con caracteres españoles (ó, é, í)
- Los .docx originales suelen estar en subcarpeta `varios/`, los .pdf en la carpeta principal

### Documentos Word
- Template: usar una DDJJ existente como base (preserva header/footer con membrete)
- `tools/doc_generator.py` tiene `load_template()`, `add_para()`, `add_separator()`
- Para modificar .docx existente: buscar en `doc.paragraphs` Y `doc.tables` por separado
- Reemplazar en `run.text` (no en `p.text`) para preservar formato

### Análisis de Precios (Anexo VII)
- Cadena: Costo Directo → Gastos Generales → CF → Beneficio → IVA → Total
- IVA es MIX de 21% (servicios/materiales) y 10.5% (equipamiento informático)
- Trabajar hacia atrás desde el total para despejar Gastos Generales
- Usar fórmula de cierre `=TARGET_CELL-D68` para IVA (absorbe redondeo floating point)
- `tools/cotizacion.py` tiene `calcular_anexo_vii()` y `calcular_iva_mix()`

### Foliación
- `tools/foliador.py` tiene `merge_and_foliate()`
- Agregar "Folio: X" en bottom-right, fontsize 9, color gris
- Skip archivos vacíos (0 bytes)
- Foliación continua entre carpetas (A1→A2→B→C)

## Estructura estándar de licitación
- **Carpeta A1** - Documentación Legal
- **Carpeta A2** - Información Económico-Financiera
- **Carpeta B** - Documentación Técnica
- **Carpeta C** - Oferta Económica

## Marcas con datasheets descargables
- **Furukawa** (lightera.com): Cat6A, FO OM3, ODF, faceplates, patch panels
- **Panduit**: Racks 42U
- **Ubiquiti** (ui.com): Switches, APs, Gateways
- **Grandstream**: Centrales IP, teléfonos, gateways FXO
- **Kaise**: UPS rack

## Problemas conocidos
| Problema | Solución |
|----------|----------|
| Encoding español en paths OneDrive | Python scripts con r'', nunca heredoc |
| OneDrive bloquea archivos | Reintentar con sleep, o pedir cerrar |
| .docx desaparece | Buscar en subcarpeta `varios/` |
| PDFs vacíos (0 bytes) | Skip con getsize() > 0 |
| Excel PermissionError | Cerrar Excel, esperar sync, reintentar |
| Floating point en cadena Excel | Celda de cierre referenciando target |
