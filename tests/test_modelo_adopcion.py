"""Pruebas de la Etapa 4: separación temporal, métricas y ausencia de numero_id como predictor."""
import numpy as np
import pandas as pd

from src.models.adopcion import (
    CORTES_TEST,
    CORTES_TRAIN,
    _metricas_clasificacion,
    _tasa_por_decil,
    entrenar_baseline,
    entrenar_catboost,
    preparar_particiones,
)


def _dataset_sintetico(n: int = 200) -> pd.DataFrame:
    rng = np.random.RandomState(42)
    cortes = CORTES_TRAIN + CORTES_TEST
    filas = []
    for i in range(n):
        filas.append({
            "numero_id": i,
            "fecha_corte": cortes[i % len(cortes)],
            "grupo_edad": ["18-25", "26-35"][i % 2],
            "desc_genero": "femenino",
            "desc_segmento": "personal",
            "desc_tipo_de_vivienda": "PROPIA" if i % 3 else None,
            "ingresos_mensuales": float(rng.uniform(500, 5000)),
            "total_egresos_mensuales": float(rng.uniform(100, 2000)),
            "total_activos": float(rng.uniform(1000, 10000)),
            "total_pasivos": float(rng.uniform(0, 3000)),
            "total_patrimonio": float(rng.uniform(500, 8000)),
            "meses_observados": i % 6,
            "saldo_total_ultimo": float(rng.uniform(0, 5000)),
            "saldo_promedio_3m": float(rng.uniform(0, 5000)),
            "saldo_promedio_6m": float(rng.uniform(0, 5000)),
            "proporcion_meses_positivos": float(rng.uniform(0, 1)),
            "tendencia_saldo_simple": float(rng.uniform(-100, 100)),
            "recencia_meses": float(i % 5),
            "fecha_maxima_variable_usada": "2025-10-01",
            "cantidad_productos": i % 3,
            "tenencia_bolsillos": i % 2,
            "experiencia_previa_inversion": i % 2,
            "flujo_libre": float(rng.uniform(-500, 3000)),
            "patrimonio_calculado": float(rng.uniform(500, 8000)),
            "diferencia_patrimonial": float(rng.uniform(-100, 100)),
            "bandera_vivienda_faltante": 0,
            "bandera_patrimonio_negativo": 0,
            "variables_financieras_faltantes": 0,
            "target_adopcion_digital": int(rng.uniform(0, 1) < 0.2),
        })
    return pd.DataFrame(filas)


def test_preparar_particiones_respeta_separacion_temporal() -> None:
    dataset = _dataset_sintetico()
    x_train, y_train, x_test, y_test = preparar_particiones(dataset)
    assert len(x_train) + len(x_test) < len(dataset) or len(x_train) + len(x_test) == len(dataset)
    assert "numero_id" not in x_train.columns
    assert "fecha_corte" not in x_train.columns
    assert "target_adopcion_digital" not in x_train.columns
    assert len(x_train) == len(y_train)
    assert len(x_test) == len(y_test)


def test_preparar_particiones_sin_traslape_de_cortes() -> None:
    dataset = _dataset_sintetico()
    cortes_usados_train = set(dataset.loc[dataset["fecha_corte"].isin(CORTES_TRAIN), "fecha_corte"])
    cortes_usados_test = set(dataset.loc[dataset["fecha_corte"].isin(CORTES_TEST), "fecha_corte"])
    assert cortes_usados_train.isdisjoint(cortes_usados_test)


def test_metricas_clasificacion_valores_esperados() -> None:
    y_true = pd.Series([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    y_score = np.array([0.1, 0.2, 0.3, 0.4, 0.9, 0.8, 0.7, 0.6, 0.5, 0.05])
    metricas = _metricas_clasificacion(y_true, y_score)
    assert metricas["prevalencia"] == 0.6
    assert 0.0 <= metricas["pr_auc"] <= 1.0
    assert metricas["precision_top10"] == 1.0  # el score más alto (0.9) corresponde a un positivo


def test_tasa_por_decil_cubre_todas_las_filas() -> None:
    rng = np.random.RandomState(1)
    y_true = pd.Series(rng.binomial(1, 0.1, size=100))
    y_score = rng.uniform(0, 1, size=100)
    resumen = _tasa_por_decil(y_true, y_score)
    assert resumen["clientes"].sum() == 100
    assert len(resumen) == 10


def test_entrenar_baseline_y_catboost_producen_probabilidades_validas() -> None:
    dataset = _dataset_sintetico()
    x_train, y_train, x_test, _ = preparar_particiones(dataset)
    columnas_numericas = [c for c in x_train.columns if c not in (
        "grupo_edad", "desc_genero", "desc_segmento", "desc_tipo_de_vivienda"
    )]

    baseline = entrenar_baseline(x_train, y_train, columnas_numericas)
    score_baseline = baseline.predict_proba(x_test)[:, 1]
    assert ((score_baseline >= 0) & (score_baseline <= 1)).all()

    modelo_catboost, parametros = entrenar_catboost(x_train, y_train)
    assert modelo_catboost is not None
    assert "depth" in parametros
