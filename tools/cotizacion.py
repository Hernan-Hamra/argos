"""
ARGOS - Herramientas de Cotización y Análisis de Precios
Cálculo de estructura de costos, IVA mix, álgebra inversa para Anexo VII.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')


def calcular_iva_mix(items):
    """
    Calcula el IVA ponderado de una lista de items con distintas alícuotas.

    Args:
        items: lista de dicts con keys 'neto' (monto sin IVA) y 'iva_pct' (21 o 10.5)

    Returns:
        dict con iva_21, iva_105, iva_total, pct_efectivo
    """
    iva_21 = sum(item['neto'] * 0.21 for item in items if item['iva_pct'] == 21)
    iva_105 = sum(item['neto'] * 0.105 for item in items if item['iva_pct'] == 10.5)
    neto_total = sum(item['neto'] for item in items)
    iva_total = iva_21 + iva_105

    return {
        'iva_21': iva_21,
        'iva_105': iva_105,
        'iva_total': iva_total,
        'neto_total': neto_total,
        'pct_efectivo': (iva_total / neto_total * 100) if neto_total else 0,
    }


def calcular_anexo_vii(target_total, costo_directo, cf_pct, beneficio_pct, iva_monto):
    """
    Calcula la estructura de costos del Anexo VII trabajando hacia atrás
    desde el total conocido.

    La variable libre es Gastos Generales (se despeja para cerrar exacto).

    Args:
        target_total: precio final con IVA (ej: 288898500.75)
        costo_directo: suma de MO + materiales + equipos (línea 6)
        cf_pct: costo financiero como decimal (ej: 0.07 para 7%)
        beneficio_pct: beneficio como decimal (ej: 0.1723 para 17.23%)
        iva_monto: monto fijo de IVA (calculado con calcular_iva_mix)

    Returns:
        dict con todas las líneas del Anexo VII
    """
    linea12 = target_total - iva_monto  # Costo Total del Trabajo
    linea10 = linea12 / (1 + beneficio_pct)  # Subtotal antes de Beneficio
    linea8 = linea10 / (1 + cf_pct)  # Subtotal antes de CF
    linea7 = linea8 - costo_directo  # Gastos Generales (variable libre)
    gg_pct = linea7 / costo_directo  # % Gastos Generales

    linea9 = linea8 * cf_pct
    linea11 = linea10 * beneficio_pct
    iva_pct = iva_monto / linea12

    return {
        'linea6': costo_directo,
        'linea7': linea7,
        'gg_pct': gg_pct,
        'linea8': linea8,
        'linea9': linea9,
        'cf_pct': cf_pct,
        'linea10': linea10,
        'linea11': linea11,
        'beneficio_pct': beneficio_pct,
        'linea12': linea12,
        'iva_monto': iva_monto,
        'iva_pct': iva_pct,
        'linea14': target_total,
    }


def print_anexo_vii(result):
    """Imprime la tabla del Anexo VII en formato argentino."""
    def fmt(v):
        s = f'{v:,.2f}'
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'$ {s}'

    print(f"  6  Costo Directo          (3+4+5)           {fmt(result['linea6'])}")
    print(f"  7  Gastos Generales       {result['gg_pct']*100:.2f} % x (6)       {fmt(result['linea7'])}")
    print(f"  8  Subtotal               (6+7)             {fmt(result['linea8'])}")
    print(f"  9  Costo Financiero       {result['cf_pct']*100:.0f} % x (8)         {fmt(result['linea9'])}")
    print(f" 10  Subtotal               (8+9)             {fmt(result['linea10'])}")
    print(f" 11  Beneficio              {result['beneficio_pct']*100:.2f} % x (10)    {fmt(result['linea11'])}")
    print(f" 12  Costo Total            (10+11)           {fmt(result['linea12'])}")
    print(f" 13  IVA (*)                {result['iva_pct']*100:.2f} % x (12)      {fmt(result['iva_monto'])}")
    print(f" 14  TOTAL                  (12+13)           {fmt(result['linea14'])}")
