"""Pruebas de la Etapa 3: dataset de modelado y controles contra fuga temporal."""
from typing import List

import pandas as pd
import pytest

from src.features.dataset_modelado import (
    calcular_fecha_adopcion,
    construir_dataset_modelado,
    construir_variables_corte,
)

COLUMNAS_FACT = (
    "numero_id", "mes", "producto_original", "familia_producto", "canal_producto",
    "saldo_ultimo", "saldo_promedio", "saldo_minimo", "saldo_maximo",
    "numero_observaciones", "primera_fecha_mes", "ultima_fecha_mes", "estado_observacion",
)


def _fila_fact(numero_id: int, mes: str, producto: str, saldo: float, dia: str = "01") -> dict:
    fecha = f"{mes}-{dia}"
    return {
        "numero_id": numero_id,
        "mes": mes,
        "producto_original": producto,
        "familia_producto": "X",
        "canal_producto": "X",
        "saldo_ultimo": saldo,
        "saldo_promedio": saldo,
        "saldo_minimo": saldo,
        "saldo_maximo": saldo,
        "numero_observaciones": 1,
        "primera_fecha_mes": fecha,
        "ultima_fecha_mes": fecha,
        "estado_observacion": "OBSERVADO_CON_SALDO" if saldo != 0 else "OBSERVADO_CON_CERO",
    }


def _dim_cliente(ids: List[int]) -> pd.DataFrame:
    return pd.DataFrame({
        "numero_id": ids,
        "grupo_edad": ["26-35"] * len(ids),
        "desc_genero": ["femenino"] * len(ids),
        "desc_segmento": ["personal"] * len(ids),
        "desc_tipo_de_vivienda": ["PROPIA"] * len(ids),
        "ingresos_mensuales": [1000.0] * len(ids),
        "total_egresos_mensuales": [400.0] * len(ids),
        "total_activos": [5000.0] * len(ids),
        "total_pasivos": [1000.0] * len(ids),
        "total_patrimonio": [4000.0] * len(ids),
    })


def test_calcular_fecha_adopcion_excluye_carga_inicial() -> None:
    fact = pd.DataFrame([
        _fila_fact(1, "2025-06", "INVESBOT", 100.0),  # carga inicial: no cuenta como adopción
        _fila_fact(2, "2025-08", "INVESBOT", 100.0),  # adopción real
        _fila_fact(3, "2025-07", "FIDUCUENTA", 0.0),  # dentro de ventana excluida de Fiducuenta
    ])
    adopciones = calcular_fecha_adopcion(fact)
    ids_con_adopcion = set(adopciones["numero_id"])
    assert ids_con_adopcion == {2}


def test_calcular_fecha_adopcion_usa_producto_valido_mas_temprano() -> None:
    fact = pd.DataFrame([
        _fila_fact(1, "2025-06", "FIDUCUENTA", 0.0),  # excluido (carga inicial Fiducuenta)
        _fila_fact(1, "2025-09", "INVESBOT", 50.0),   # adopción válida
    ])
    adopciones = calcular_fecha_adopcion(fact).set_index("numero_id")
    assert adopciones.loc[1, "producto_adopcion"] == "INVESBOT"


def test_construir_variables_corte_no_usa_mes_del_corte() -> None:
    fact = pd.DataFrame([
        _fila_fact(1, "2025-10", "CUENTA DE AHORRO", 100.0),
        _fila_fact(1, "2025-11", "CUENTA DE AHORRO", 999999.0),  # mismo mes que el corte: debe ignorarse
    ])
    variables = construir_variables_corte(fact, pd.Timestamp("2025-11-01")).set_index("numero_id")
    assert variables.loc[1, "saldo_total_ultimo"] == 100.0
    assert variables.loc[1, "fecha_maxima_variable_usada"] < "2025-11-01"


def test_dataset_modelado_unicidad_numero_id_fecha_corte() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2025-09", "INVESBOT", 10.0)])  # adopta antes de ambos cortes
    dim_cliente = _dim_cliente([1, 2])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01", "2026-01-01"], 90)
    assert not dataset[["numero_id", "fecha_corte"]].duplicated().any()
    # cliente 1 ya adoptó antes de ambos cortes (sale del universo); cliente 2 permanece en los dos.
    assert len(dataset) == 2
    assert set(dataset["numero_id"]) == {2}


def test_dataset_modelado_target_dentro_de_horizonte() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2026-02", "INVESBOT", 10.0, dia="15")])
    dim_cliente = _dim_cliente([1])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01"], 90)
    fila = dataset.set_index("numero_id").loc[1]
    assert fila["target_adopcion_digital"] == 1  # 2026-02-15 está dentro de 90 días desde 2025-12-01


def test_dataset_modelado_target_fuera_de_horizonte() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2026-04", "INVESBOT", 10.0)])
    dim_cliente = _dim_cliente([1])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01"], 90)
    fila = dataset.set_index("numero_id").loc[1]
    assert fila["target_adopcion_digital"] == 0  # 2026-04 excede el horizonte de 90 días


def test_dataset_modelado_excluye_cliente_ya_adoptado_antes_del_corte() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2025-08", "INVESBOT", 10.0)])
    dim_cliente = _dim_cliente([1])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01"], 90)
    assert dataset.empty  # el cliente ya adoptó antes del corte: sale del universo de adquisición


def test_dataset_modelado_carga_inicial_nunca_cuenta_como_adopcion() -> None:
    fact = pd.DataFrame([_fila_fact(1, "2025-06", "INVESBOT", 10.0)])  # solo aparece en carga inicial
    dim_cliente = _dim_cliente([1])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01", "2026-01-01"], 90)
    assert (dataset["target_adopcion_digital"] == 0).all()
    assert len(dataset) == 2  # el cliente permanece elegible en ambos cortes


def test_dataset_modelado_sin_fuga_temporal_en_muestra() -> None:
    fact = pd.DataFrame([
        _fila_fact(1, "2025-09", "CUENTA DE AHORRO", 500.0),
        _fila_fact(1, "2025-10", "CUENTA DE AHORRO", 600.0),
        _fila_fact(1, "2025-12", "CUENTA DE AHORRO", 700.0),  # posterior al corte de diciembre
    ])
    dim_cliente = _dim_cliente([1])
    dataset = construir_dataset_modelado(fact, dim_cliente, ["2025-12-01"], 90)
    fila = dataset.set_index("numero_id").loc[1]
    assert fila["fecha_maxima_variable_usada"] < "2025-12-01"
    assert fila["saldo_total_ultimo"] == 600.0
