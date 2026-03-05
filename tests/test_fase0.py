"""
Tests Fase 0: Cimientos de ARGOS
Valida que el orquestador, parser, alertas y aprendizaje funcionan.
Correr: python -m pytest tests/test_fase0.py -v
O sin pytest: python tests/test_fase0.py
"""

import os
import sys
import json

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestResults:
    """Simple test runner sin dependencias externas."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  [OK] {name}")
        else:
            self.failed += 1
            self.errors.append(f"{name}: {detail}")
            print(f"  [FAIL] {name} — {detail}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"  {self.passed}/{total} tests passed")
        if self.errors:
            print(f"  {self.failed} FAILED:")
            for e in self.errors:
                print(f"    - {e}")
        else:
            print("  All tests passed!")
        print(f"{'='*50}")
        return self.failed == 0


def test_parser():
    """Test 0.2: Parser de respuestas naturales."""
    print("\n--- Test Parser de Respuestas ---")
    from tools.parsear_respuesta import parsear_bienestar, campos_faltantes, formato_resumen
    t = TestResults()

    # Test números directos
    r = parsear_bienestar("humor 7, energia 8, estres 3")
    t.check("Número directo humor", r['humor'] == 7, f"esperado 7, got {r['humor']}")
    t.check("Número directo energia", r['energia'] == 8, f"esperado 8, got {r['energia']}")
    t.check("Número directo estres", r['estres'] == 3, f"esperado 3, got {r['estres']}")

    # Test horas de sueño
    r = parsear_bienestar("dormí 7 horas")
    t.check("Horas sueño 7", r['horas_sueno'] == 7.0, f"esperado 7.0, got {r['horas_sueno']}")

    r = parsear_bienestar("dormí 6.5 horas")
    t.check("Horas sueño 6.5", r['horas_sueno'] == 6.5, f"esperado 6.5, got {r['horas_sueno']}")

    r = parsear_bienestar("dormi 8hs")
    t.check("Horas sueño 8hs", r['horas_sueno'] == 8.0, f"esperado 8.0, got {r['horas_sueno']}")

    # Test expresiones argentinas
    r = parsear_bienestar("como el orto")
    t.check("Como el orto → humor bajo", r['humor'] is not None and r['humor'] <= 3,
            f"esperado <=3, got {r['humor']}")

    r = parsear_bienestar("bárbaro")
    t.check("Bárbaro → humor alto", r['humor'] is not None and r['humor'] >= 8,
            f"esperado >=8, got {r['humor']}")

    r = parsear_bienestar("bien")
    t.check("Bien → humor 7", r['humor'] == 7, f"esperado 7, got {r['humor']}")

    r = parsear_bienestar("estresado")
    t.check("Estresado → estres alto", r['estres'] is not None and r['estres'] >= 6,
            f"esperado >=6, got {r['estres']}")

    r = parsear_bienestar("sin estrés")
    t.check("Sin estrés → estres bajo", r['estres'] is not None and r['estres'] <= 2,
            f"esperado <=2, got {r['estres']}")

    # Test ejercicio
    r = parsear_bienestar("nadé 45 minutos")
    t.check("Ejercicio 45 min", r['ejercicio_min'] == 45, f"esperado 45, got {r['ejercicio_min']}")

    # Test campos faltantes
    r = parsear_bienestar("dormí 7 horas")
    f = campos_faltantes(r)
    t.check("Campos faltantes sin humor/energia/estres", 'humor' in f and 'energia' in f,
            f"faltantes: {f}")

    # Test formato resumen
    r = parsear_bienestar("humor 7, energia 8, estres 3, dormí 7 horas")
    resumen = formato_resumen(r)
    t.check("Formato resumen no vacío", len(resumen) > 10, f"resumen: {resumen}")

    # Test texto vacío
    r = parsear_bienestar("")
    t.check("Texto vacío → todo None", all(v is None for v in r.values()))

    # Test combinación
    r = parsear_bienestar("todo bien, tranqui, sin estrés, dormí 8hs")
    t.check("Combinación: humor", r['humor'] is not None and r['humor'] >= 6,
            f"humor={r['humor']}")
    t.check("Combinación: estres bajo", r['estres'] is not None and r['estres'] <= 3,
            f"estres={r['estres']}")
    t.check("Combinación: sueño", r['horas_sueno'] == 8.0,
            f"sueno={r['horas_sueno']}")

    return t


def test_orquestador():
    """Test 0.1: Orquestador de sesión."""
    print("\n--- Test Orquestador de Sesión ---")
    from tools.orquestador_sesion import (
        apertura, cierre, estado_sesion, registrar_checkpoint_apertura
    )
    t = TestResults()

    # Test apertura
    data = apertura()
    t.check("Apertura retorna sesion_id", data['sesion_id'] is not None and data['sesion_id'] > 0,
            f"sesion_id={data['sesion_id']}")
    t.check("Apertura retorna fecha", data['fecha'] is not None)
    t.check("Apertura retorna dia_semana", data['dia_semana'] is not None)
    t.check("Apertura retorna checkpoints", isinstance(data['checkpoints'], list))
    t.check("Apertura retorna nudges", isinstance(data['nudges'], list))
    t.check("Apertura retorna coherencia", isinstance(data['coherencia'], list))
    t.check("Apertura retorna alertas", 'alertas' in data)
    t.check("Apertura retorna vencidos_count", isinstance(data['vencidos_count'], int))

    # Test estado sesión
    estado = estado_sesion()
    t.check("Estado: sesión abierta", estado['sesion_abierta'] == True)
    t.check("Estado: fecha correcta", estado['fecha'] is not None)

    # Test registrar checkpoint
    resultado_cp = registrar_checkpoint_apertura(
        "dormí 7 horas, estoy bien, algo estresado",
        sesion_id=data['sesion_id']
    )
    t.check("Checkpoint: valores parseados", resultado_cp['valores'] is not None)
    t.check("Checkpoint: humor parseado", resultado_cp['valores']['humor'] is not None,
            f"humor={resultado_cp['valores']['humor']}")
    t.check("Checkpoint: sueño parseado", resultado_cp['valores']['horas_sueno'] == 7.0,
            f"sueno={resultado_cp['valores']['horas_sueno']}")
    t.check("Checkpoint: bienestar_id", resultado_cp['bienestar_id'] is not None)
    t.check("Checkpoint: resumen", len(resultado_cp['resumen']) > 5)

    # Test cierre
    data_cierre = cierre(
        sesion_id=data['sesion_id'],
        respuestas_cierre="Estuvo bien, algo cansado pero productivo"
    )
    t.check("Cierre: estado completado", data_cierre['estado'] == 'completado')
    t.check("Cierre: bienestar_cierre", data_cierre['bienestar_cierre'] is not None)
    t.check("Cierre: cierre_sesion", data_cierre['cierre_sesion'] is not None)

    # Verificar que la sesión quedó cerrada
    estado2 = estado_sesion()
    t.check("Post-cierre: sesión cerrada", estado2['sesion_abierta'] == False)

    return t


def test_alertas():
    """Test 0.5: Alertas de seguimiento vencido."""
    print("\n--- Test Alertas Automáticas ---")
    from tools.alertas import generar_alertas, alertas_criticas, formato_alertas
    t = TestResults()

    # Test generar alertas
    alertas = generar_alertas()
    t.check("Alertas: retorna dict", isinstance(alertas, dict))
    t.check("Alertas: tiene rojas", 'rojas' in alertas)
    t.check("Alertas: tiene amarillas", 'amarillas' in alertas)
    t.check("Alertas: tiene info", 'info' in alertas)
    t.check("Alertas: tiene resumen", isinstance(alertas['resumen'], str))
    t.check("Alertas: tiene total", isinstance(alertas['total'], int))
    t.check("Alertas: hay_criticas es bool", isinstance(alertas['hay_criticas'], bool))

    # Test formato
    texto = formato_alertas(alertas)
    t.check("Formato alertas: no vacío", len(texto) > 0)

    # Test alertas críticas shortcut
    criticas = alertas_criticas()
    t.check("Alertas críticas: retorna lista", isinstance(criticas, list))

    # Si hay vencidos, verificar estructura
    if alertas['rojas']:
        r = alertas['rojas'][0]
        t.check("Estructura alerta roja: tipo", 'tipo' in r)
        t.check("Estructura alerta roja: accion", 'accion' in r)
        t.check("Estructura alerta roja: dias", 'dias' in r)

    return t


def test_aprendizaje():
    """Test 0.4: Aprendizaje real."""
    print("\n--- Test Aprendizaje ---")
    from tools.aprendizaje import (
        registrar_error, buscar_solucion, estadisticas_aprendizaje, registrar_exito
    )
    t = TestResults()

    # Test registrar error
    r = registrar_error(
        'Test error para fase 0',
        herramienta='test_fase0.py',
        solucion='Es un test, no hacer nada',
        tipo_error='sistema',
        severidad='baja'
    )
    t.check("Registrar error: accion", r['accion'] in ('creado', 'reforzado'))
    t.check("Registrar error: patron_id", r['patron_id'] is not None)

    # Test buscar solución
    sol = buscar_solucion('Test error para fase')
    t.check("Buscar solución: encontrado", sol['encontrado'] == True)
    t.check("Buscar solución: tiene solución", sol.get('solucion') is not None)

    # Test buscar solución inexistente
    sol2 = buscar_solucion('zxcvbnm1234567890')
    t.check("Buscar solución inexistente: no encontrado", sol2['encontrado'] == False)

    # Test estadísticas
    stats = estadisticas_aprendizaje()
    t.check("Estadísticas: patrones", isinstance(stats['patrones'], list))
    t.check("Estadísticas: errores_con_solucion", isinstance(stats['errores_con_solucion'], int))

    # Test registrar éxito
    r2 = registrar_exito("Test exitoso de parser", herramienta="parsear_respuesta.py")
    t.check("Registrar éxito: retorna dict", isinstance(r2, dict))

    # Limpiar test data
    from tools.tracker import get_connection
    conn = get_connection()
    conn.execute("DELETE FROM patrones WHERE descripcion LIKE '%Test error para fase%'")
    conn.execute("DELETE FROM patrones WHERE descripcion LIKE '%Test exitoso de parser%'")
    conn.commit()
    conn.close()
    t.check("Cleanup: test data eliminada", True)

    return t


def test_nudges():
    """Test 0.3: Nudges conectados."""
    print("\n--- Test Nudges ---")
    from tools.proactivo import generar_nudges
    t = TestResults()

    nudges = generar_nudges(max_nudges=5)
    t.check("Nudges: retorna lista", isinstance(nudges, list))
    t.check("Nudges: máximo 5", len(nudges) <= 5)

    if nudges:
        n = nudges[0]
        t.check("Nudge: tiene tipo", 'tipo' in n)
        t.check("Nudge: tiene prioridad", 'prioridad' in n)
        t.check("Nudge: tiene mensaje", 'mensaje' in n)
        t.check("Nudge: prioridad es número", isinstance(n['prioridad'], (int, float)))

    return t


def test_coherencia():
    """Test 0.3: Coherencia conectada."""
    print("\n--- Test Coherencia ---")
    from tools.coherencia import reporte_coherencia
    t = TestResults()

    resultados = reporte_coherencia(dias=30, imprimir=False)
    t.check("Coherencia: retorna lista", isinstance(resultados, list))

    if resultados:
        r = resultados[0]
        t.check("Coherencia: tiene meta", 'meta' in r)
        t.check("Coherencia: tiene coherencia", 'coherencia' in r)
        t.check("Coherencia: tiene señal", 'senal' in r)
        t.check("Coherencia: tiene espejo", 'espejo' in r)
        t.check("Coherencia: señal válida",
                r['senal'] in ('on_track', 'en_riesgo', 'desalineada', 'abandonada'),
                f"senal={r['senal']}")
        t.check("Coherencia: score 0-1", 0 <= r['coherencia'] <= 1,
                f"coherencia={r['coherencia']}")

    return t


def test_flujo_completo():
    """Test integración: flujo apertura → checkpoint → cierre."""
    print("\n--- Test Flujo Completo ---")
    from tools.orquestador_sesion import apertura, registrar_checkpoint_apertura, cierre, estado_sesion
    t = TestResults()

    # 1. Apertura
    data = apertura()
    sesion_id = data['sesion_id']
    t.check("Flujo: sesión abierta", sesion_id > 0)

    # 2. Checkpoint apertura
    cp = registrar_checkpoint_apertura("dormí 6 horas, bien de humor, sin estrés, no hice ejercicio")
    t.check("Flujo: checkpoint registrado", cp['bienestar_id'] is not None)
    t.check("Flujo: sueño=6", cp['valores']['horas_sueno'] == 6.0,
            f"sueno={cp['valores']['horas_sueno']}")
    t.check("Flujo: humor=7", cp['valores']['humor'] == 7,
            f"humor={cp['valores']['humor']}")

    # 3. Verificar estado intermedio
    estado = estado_sesion()
    t.check("Flujo: sesión sigue abierta", estado['sesion_abierta'] == True)
    t.check("Flujo: bienestar registrado", estado['bienestar_registrado'] == True)

    # 4. Cierre
    data_cierre = cierre(sesion_id=sesion_id, respuestas_cierre="bien, productivo, algo cansado al final")
    t.check("Flujo: cierre completado", data_cierre['estado'] == 'completado')
    t.check("Flujo: aprendizajes ejecutados", data_cierre.get('aprendizajes') is not None)

    # 5. Verificar post-cierre
    estado2 = estado_sesion()
    t.check("Flujo: sesión cerrada", estado2['sesion_abierta'] == False)

    return t


def run_all():
    """Ejecutar todos los tests."""
    print("="*50)
    print("  ARGOS FASE 0 — Test Suite")
    print(f"  {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)

    all_results = []
    all_results.append(test_parser())
    all_results.append(test_nudges())
    all_results.append(test_coherencia())
    all_results.append(test_alertas())
    all_results.append(test_aprendizaje())
    all_results.append(test_orquestador())
    all_results.append(test_flujo_completo())

    # Resumen global
    total_passed = sum(t.passed for t in all_results)
    total_failed = sum(t.failed for t in all_results)
    total = total_passed + total_failed

    print(f"\n{'='*50}")
    print(f"  RESULTADO GLOBAL: {total_passed}/{total} tests passed")
    if total_failed > 0:
        print(f"  {total_failed} FAILED")
        for t in all_results:
            for e in t.errors:
                print(f"    - {e}")
    else:
        print("  TODOS LOS TESTS PASARON")
    print(f"{'='*50}")

    return total_failed == 0


if __name__ == '__main__':
    success = run_all()
    sys.exit(0 if success else 1)
