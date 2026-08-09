"""Pruebas de la Etapa 5: saldo potencial, scoring y escenarios (funciones puras)."""
import numpy as np
import pandas as pd

from src.models.scoring import (
    asignar_decil,
    asignar_nivel_confianza,
    asignar_segmento_oportunidad,
    calcular_saldo_ventana,
    comparar_baselines_saldo,
    tabla_saldo_por_segmento,
)


def _fila_fact(numero_id: int, mes: str, producto: str, saldo: float, dia: str = "01") -> dict:
    fecha = f"{mes}-{dia}"
    return {
        "numero_id": numero_id,
        "producto_original": producto,
        "primera_fecha_mes": fecha,
        "ultima_fecha_mes": fecha,
        "saldo_ultimo": saldo,
    }


def test_calcular_saldo_ventana_usa_solo_fechas_dentro_de_30_90_dias() -> None:
    fact = pd.DataFrame([
        _fila_fact(1, "2025-07", "INVESBOT", 999.0),   # 5 días después: fuera de ventana (< 30 días)
        _fila_fact(1, "2025-08", "INVESBOT", 100.0, dia="01"),  # ~35 días después: dentro
        _fila_fact(1, "2025-09", "INVESBOT", 200.0, dia="15"),  # ~80 días después: dentro
        _fila_fact(1, "2025-12", "INVESBOT", 999.0),   # muy posterior: fuera de ventana
    ])
    adopciones = pd.DataFrame({
        "numero_id": [1],
        "fecha_adopcion": [pd.Timestamp("2025-06-27")],
        "producto_adopcion": ["INVESBOT"],
    })
    resultado = calcular_saldo_ventana(fact, adopciones).set_index("numero_id")
    assert resultado.loc[1, "saldo_ventana"] == 150.0  # mediana de 100 y 200


def test_calcular_saldo_ventana_marca_seguimiento_incompleto() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2026-05", "INVESBOT", 100.0)])
    adopciones = pd.DataFrame({
        "numero_id": [1],
        "fecha_adopcion": [pd.Timestamp("2026-05-01")],  # +90 días excede la última fecha disponible
        "producto_adopcion": ["INVESBOT"],
    })
    resultado = calcular_saldo_ventana(fact, adopciones).set_index("numero_id")
    assert not resultado.loc[1, "seguimiento_completo"]


def _historico_sintetico() -> pd.DataFrame:
    filas = []
    rng = np.random.default_rng(42)
    for i in range(200):
        segmento = "preferencial" if i % 2 == 0 else "personal"
        producto = "INVESBOT" if i % 3 == 0 else "FIDUCUENTA"
        fecha = pd.Timestamp("2025-10-01") if i < 100 else pd.Timestamp("2026-02-15")
        saldo = 1000.0 if segmento == "preferencial" else 200.0
        filas.append({
            "numero_id": i,
            "fecha_adopcion": fecha,
            "producto_adopcion": producto,
            "desc_segmento": segmento,
            "saldo_ventana": saldo + rng.normal(0, 1),
        })
    return pd.DataFrame(filas)


def test_comparar_baselines_saldo_selecciona_metodo_con_menor_error() -> None:
    historico = _historico_sintetico()
    tabla, metodo = comparar_baselines_saldo(historico)
    assert set(tabla["metodo"]) == {"mediana_global", "mediana_por_producto", "mediana_por_segmento_producto"}
    # el saldo depende fuertemente del segmento, no del producto: el mejor método debe considerar el segmento.
    assert metodo == "mediana_por_segmento_producto"


def test_tabla_saldo_por_segmento_diferencia_segmentos() -> None:
    historico = _historico_sintetico()
    tabla, mediana_global = tabla_saldo_por_segmento(historico)
    assert tabla["preferencial"] > tabla["personal"]
    assert mediana_global > 0


def test_asignar_decil_diez_es_el_valor_mas_alto() -> None:
    valores = np.arange(100)
    deciles = asignar_decil(valores)
    assert deciles[-1] == 10
    assert deciles[0] == 1


def test_asignar_segmento_oportunidad_cuatro_categorias() -> None:
    probabilidad = np.array([0.9, 0.9, 0.1, 0.1])
    valor = np.array([100.0, 1.0, 100.0, 1.0])
    segmentos = asignar_segmento_oportunidad(probabilidad, valor)
    assert segmentos[0] == "Alta probabilidad y alto valor"
    assert segmentos[1] == "Alta probabilidad y valor moderado"
    assert segmentos[2] == "Probabilidad moderada y alto valor"
    assert segmentos[3] == "Baja prioridad"


def test_asignar_segmento_oportunidad_no_colapsa_con_categoria_mayoritaria() -> None:
    # Simula saldo_potencial asignado por segmento comercial: una categoría (2.0)
    # concentra el 80 % de los clientes, como ocurre con "personal" en los datos reales.
    valor = np.array([2.0] * 80 + [5.0] * 15 + [20.0] * 5)
    probabilidad = np.linspace(0.01, 0.99, num=100)
    segmentos = asignar_segmento_oportunidad(probabilidad, valor)
    conteos = pd.Series(segmentos).value_counts()
    # Con un umbral ponderado por frecuencia, todo caería en "alto valor"; con el
    # umbral sobre valores únicos, las categorías de valor moderado/bajo persisten.
    assert conteos.get("Alta probabilidad y valor moderado", 0) > 0
    assert conteos.get("Baja prioridad", 0) > 0


def test_asignar_nivel_confianza() -> None:
    meses = pd.Series([6, 0, 3])
    faltantes = pd.Series([0, 5, 1])
    resultado = asignar_nivel_confianza(meses, faltantes)
    assert list(resultado) == ["ALTA", "BAJA", "MEDIA"]
