"""Modelo de adopción digital (Etapa 4): baseline interpretable vs. CatBoost.

Compara una regresión logística regularizada con `CatBoostClassifier` sobre
`data/processed/dataset_modelado.parquet`, usando separación temporal por
`fecha_corte` (no aleatoria). Selecciona un único modelo y persiste solo el
modelo elegido y metadatos compactos. No entrena el modelo de saldo (Etapa 5).
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

SEMILLA = 42
CORTES_TRAIN = ["2025-12-01", "2026-01-01"]
CORTES_TEST = ["2026-02-01", "2026-03-01"]

COLUMNAS_CATEGORICAS = ("grupo_edad", "desc_genero", "desc_segmento", "desc_tipo_de_vivienda")
COLUMNAS_EXCLUIDAS = ("numero_id", "fecha_corte", "fecha_maxima_variable_usada", "target_adopcion_digital")
VALOR_FALTANTE_CATEGORICO = "SIN_INFORMACION"


def _columnas_numericas(dataset: pd.DataFrame) -> List[str]:
    return [
        columna for columna in dataset.columns
        if columna not in COLUMNAS_EXCLUIDAS and columna not in COLUMNAS_CATEGORICAS
    ]


def preparar_particiones(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Separa train/test de forma temporal por `fecha_corte` (no aleatoria).

    `numero_id` nunca se incluye como predictor.
    """
    columnas_numericas = _columnas_numericas(dataset)
    columnas_features = list(COLUMNAS_CATEGORICAS) + columnas_numericas

    train = dataset[dataset["fecha_corte"].isin(CORTES_TRAIN)]
    test = dataset[dataset["fecha_corte"].isin(CORTES_TEST)]

    x_train = train[columnas_features].copy()
    x_test = test[columnas_features].copy()
    for columna in COLUMNAS_CATEGORICAS:
        x_train[columna] = x_train[columna].fillna(VALOR_FALTANTE_CATEGORICO)
        x_test[columna] = x_test[columna].fillna(VALOR_FALTANTE_CATEGORICO)

    y_train = train["target_adopcion_digital"]
    y_test = test["target_adopcion_digital"]
    return x_train, y_train, x_test, y_test


def _metricas_clasificacion(y_true: pd.Series, y_score: np.ndarray) -> Dict[str, float]:
    """Calcula PR-AUC, ROC-AUC, Brier, y precisión/recall/lift en el top 10 %."""
    orden = np.argsort(-y_score)
    n_top = max(int(len(y_score) * 0.10), 1)
    top = orden[:n_top]

    prevalencia = float(y_true.mean())
    precision_top10 = float(y_true.to_numpy()[top].mean())
    recall_top10 = float(y_true.to_numpy()[top].sum() / max(y_true.sum(), 1))
    lift_top10 = precision_top10 / prevalencia if prevalencia > 0 else float("nan")

    return {
        "pr_auc": float(average_precision_score(y_true, y_score)),
        "roc_auc": float(roc_auc_score(y_true, y_score)),
        "brier": float(brier_score_loss(y_true, y_score)),
        "precision_top10": precision_top10,
        "recall_top10": recall_top10,
        "lift_top10": lift_top10,
        "prevalencia": prevalencia,
    }


def _tasa_por_decil(y_true: pd.Series, y_score: np.ndarray) -> pd.DataFrame:
    """Tasa observada de adopción por decil de score (decil 10 = score más alto)."""
    rango = pd.Series(y_score).rank(method="first")
    decil = pd.qcut(rango, 10, labels=False) + 1
    tabla = pd.DataFrame({"decil": decil, "target": y_true.to_numpy()})
    resumen = tabla.groupby("decil", as_index=False)["target"].agg(clientes="count", tasa_adopcion="mean")
    return resumen.sort_values("decil", ascending=False).reset_index(drop=True)


def entrenar_baseline(x_train: pd.DataFrame, y_train: pd.Series, columnas_numericas: List[str]) -> Pipeline:
    """Regresión logística regularizada con imputación/escalado ajustados solo en entrenamiento."""
    transformador = ColumnTransformer([
        ("categoricas", Pipeline([
            ("imputar", SimpleImputer(strategy="constant", fill_value=VALOR_FALTANTE_CATEGORICO)),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), list(COLUMNAS_CATEGORICAS)),
        ("numericas", Pipeline([
            ("imputar", SimpleImputer(strategy="median")),
            ("escalar", StandardScaler()),
        ]), columnas_numericas),
    ])
    pipeline = Pipeline([
        ("transformar", transformador),
        ("clasificador", LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=SEMILLA, solver="lbfgs",
        )),
    ])
    pipeline.fit(x_train, y_train)
    return pipeline


def entrenar_catboost(
    x_train: pd.DataFrame, y_train: pd.Series, fechas_train: pd.Series = None,
) -> Tuple[CatBoostClassifier, Dict[str, Any]]:
    """Entrena CatBoost con una búsqueda pequeña (2 combinaciones) y early stopping.

    Si se pasa `fechas_train`, la validación usa el corte más reciente de
    `CORTES_TRAIN` (no un split aleatorio): un split aleatorio mezcla filas del
    mismo período que el resto del entrenamiento y sobreestima la generalización
    a los cortes de prueba futuros (early stopping/selección de iteración
    quedaban ajustados a un problema "en el tiempo", no fuera de tiempo).
    """
    if fechas_train is not None:
        ultimo_corte_train = CORTES_TRAIN[-1]
        es_validacion = (fechas_train == ultimo_corte_train).to_numpy()
        x_fit, y_fit = x_train.loc[~es_validacion], y_train.loc[~es_validacion]
        x_val, y_val = x_train.loc[es_validacion], y_train.loc[es_validacion]
    else:
        x_fit, x_val, y_fit, y_val = train_test_split(
            x_train, y_train, test_size=0.1, random_state=SEMILLA, stratify=y_train,
        )
    indices_categoricas = [x_train.columns.get_loc(c) for c in COLUMNAS_CATEGORICAS]
    pool_fit = Pool(x_fit, y_fit, cat_features=indices_categoricas)
    pool_val = Pool(x_val, y_val, cat_features=indices_categoricas)

    combinaciones = [
        {"depth": 7, "learning_rate": 0.05, "l2_leaf_reg": 5},
    ]
    mejor_modelo = None
    mejor_pr_auc = -1.0
    mejor_parametros: Dict[str, Any] = {}

    for posicion, combinacion in enumerate(combinaciones, start=1):
        logger.info(
            "CatBoost: entrenando combinación %s/%s (%s)...",
            posicion, len(combinaciones), combinacion,
        )
        # early stopping por PR-AUC (no Logloss): la métrica que importa para
        # priorización es PR-AUC/lift, no Logloss.
        modelo = CatBoostClassifier(
            iterations=1000,
            early_stopping_rounds=75,
            eval_metric="PRAUC",
            random_seed=SEMILLA,
            loss_function="Logloss",
            verbose=50,
            **combinacion,
        )
        modelo.fit(pool_fit, eval_set=pool_val)
        pr_auc = average_precision_score(y_val, modelo.predict_proba(pool_val)[:, 1])
        logger.info("CatBoost: combinación %s/%s terminada, PR-AUC validación = %.4f", posicion, len(combinaciones), pr_auc)
        if pr_auc > mejor_pr_auc:
            mejor_pr_auc = pr_auc
            mejor_modelo = modelo
            mejor_parametros = {**combinacion, "iterations": max(modelo.get_best_iteration() + 1, 1)}

    mejor_modelo = CatBoostClassifier(**mejor_parametros, random_seed=SEMILLA, loss_function="Logloss", verbose=100)
    mejor_modelo.fit(Pool(x_train, y_train, weight=np.where(fechas_train == CORTES_TRAIN[-1], 2.0, 1.0), cat_features=indices_categoricas))
    #mejor_modelo.fit(Pool(x_train, y_train, cat_features=indices_categoricas))
    return mejor_modelo, mejor_parametros


def _importancia_baseline(pipeline: Pipeline, columnas_numericas: List[str]) -> List[Dict[str, Any]]:
    onehot: OneHotEncoder = pipeline.named_steps["transformar"].named_transformers_["categoricas"].named_steps["onehot"]
    nombres = list(onehot.get_feature_names_out(list(COLUMNAS_CATEGORICAS))) + columnas_numericas
    coeficientes = pipeline.named_steps["clasificador"].coef_[0]
    orden = np.argsort(-np.abs(coeficientes))[:10]
    return [{"variable": nombres[i], "coeficiente": round(float(coeficientes[i]), 4)} for i in orden]


def _importancia_catboost(modelo: CatBoostClassifier, columnas: List[str]) -> List[Dict[str, Any]]:
    importancias = modelo.get_feature_importance()
    orden = np.argsort(-importancias)[:10]
    return [{"variable": columnas[i], "importancia": round(float(importancias[i]), 2)} for i in orden]


def _shap_catboost(modelo: CatBoostClassifier, x_test: pd.DataFrame, indices_categoricas: List[int]) -> List[Dict[str, Any]]:
    muestra = x_test.sample(n=min(2000, len(x_test)), random_state=SEMILLA)
    pool_muestra = Pool(muestra, cat_features=indices_categoricas)
    shap_values = modelo.get_feature_importance(pool_muestra, type="ShapValues")
    importancia_media = np.abs(shap_values[:, :-1]).mean(axis=0)
    orden = np.argsort(-importancia_media)[:5]
    columnas = list(x_test.columns)
    return [{"variable": columnas[i], "shap_medio_abs": round(float(importancia_media[i]), 2)} for i in orden]


def _composicion_target_por_producto(fact: pd.DataFrame, dataset_test: pd.DataFrame) -> pd.DataFrame:
    from src.features.dataset_modelado import calcular_fecha_adopcion

    adopciones = calcular_fecha_adopcion(fact)
    adoptantes_test = dataset_test.loc[dataset_test["target_adopcion_digital"] == 1, ["numero_id"]]
    composicion = adoptantes_test.merge(adopciones, on="numero_id", how="left")
    resumen = (
        composicion.groupby("producto_adopcion", as_index=False)
        .size()
        .rename(columns={"size": "adoptantes"})
        .sort_values("adoptantes", ascending=False)
    )
    return resumen


def _generar_reporte(
    ruta_reporte: Path,
    comparacion: pd.DataFrame,
    estabilidad: pd.DataFrame,
    decil_seleccionado: pd.DataFrame,
    composicion_producto: pd.DataFrame,
    importancia_baseline: List[Dict[str, Any]],
    importancia_catboost: List[Dict[str, Any]],
    shap_top: List[Dict[str, Any]],
    modelo_seleccionado: str,
) -> None:
    contenido = [
        f"Separación temporal: entrenamiento en cortes {CORTES_TRAIN}, prueba en cortes {CORTES_TEST}.",
        f"**Modelo seleccionado: {modelo_seleccionado}** (mejor PR-AUC en prueba temporal, ver tabla).",
        "",
        "### Comparación de modelos y baselines (conjunto de prueba temporal)",
        "",
        tabla_markdown(
            comparacion.to_dict("records"),
            ("modelo", "pr_auc", "roc_auc", "brier", "precision_top10", "recall_top10", "lift_top10"),
        ),
        "",
        "### Estabilidad temporal básica (PR-AUC del modelo seleccionado por corte de prueba)",
        "",
        tabla_markdown(estabilidad.to_dict("records"), ("fecha_corte", "pr_auc", "tasa_adopcion")),
        "",
        f"### Tasa observada por decil ({modelo_seleccionado}, prueba)",
        "",
        tabla_markdown(decil_seleccionado.to_dict("records"), ("decil", "clientes", "tasa_adopcion")),
        "",
        "### Composición del target de prueba por producto de adopción",
        "",
        tabla_markdown(composicion_producto.to_dict("records"), ("producto_adopcion", "adoptantes")),
        "",
        "### Explicabilidad",
        "",
        "Top 10 coeficientes del baseline (regresión logística, variables estandarizadas):",
        "",
        tabla_markdown(importancia_baseline, ("variable", "coeficiente")),
        "",
        "Top 10 importancia global de CatBoost:",
        "",
        tabla_markdown(importancia_catboost, ("variable", "importancia")),
        "",
        "Top 5 variables por SHAP medio absoluto (muestra reproducible de 2000 filas de prueba):",
        "",
        tabla_markdown(shap_top, ("variable", "shap_medio_abs")),
        "",
        "Limitaciones: el desbalance es fuerte (prevalencia ~1-1.4 %); las métricas de precisión/recall "
        "en el top 10 % son más informativas que el ROC-AUC. El modelo debe recalibrarse con adopción "
        "real de la App una vez esté disponible.",
    ]
    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="MODELO_ADOPCION",
        titulo="Modelo de adopción digital (Etapa 4)",
        contenido="\n".join(contenido),
    )


def ejecutar_modelo_adopcion(configuracion: Dict[str, Any]) -> Dict[str, Any]:
    """Orquesta el entrenamiento, evaluación, selección y persistencia del modelo de adopción."""
    processed_path = Path(configuracion["data"]["processed_path"])
    logger.info("Cargando dataset_modelado.parquet y fact_saldos_mensuales.parquet...")
    dataset = pd.read_parquet(processed_path / "dataset_modelado.parquet")
    fact = pd.read_parquet(processed_path / "fact_saldos_mensuales.parquet")

    assert "numero_id" not in _columnas_numericas(dataset)
    columnas_numericas = _columnas_numericas(dataset)

    logger.info("Preparando particiones temporales train/test...")
    x_train, y_train, x_test, y_test = preparar_particiones(dataset)
    logger.info("Train: %s filas. Test: %s filas.", len(x_train), len(x_test))

    logger.info("Entrenando baseline (regresión logística)...")
    baseline = entrenar_baseline(x_train, y_train, columnas_numericas)
    logger.info("Baseline entrenado. Entrenando CatBoost (2 combinaciones con early stopping)...")
    fechas_train = dataset.loc[x_train.index, "fecha_corte"]
    catboost_modelo, catboost_parametros = entrenar_catboost(x_train, y_train, fechas_train)

    logger.info("Calculando métricas de prueba temporal...")
    indices_categoricas = [x_train.columns.get_loc(c) for c in COLUMNAS_CATEGORICAS]
    pool_test = Pool(x_test, cat_features=indices_categoricas)

    score_baseline = baseline.predict_proba(x_test)[:, 1]
    score_catboost = catboost_modelo.predict_proba(pool_test)[:, 1]
    score_prevalencia = np.full(len(y_test), y_train.mean())
    score_regla_simple = x_test["experiencia_previa_inversion"].to_numpy().astype(float)

    metricas = {
        "regresion_logistica": _metricas_clasificacion(y_test, score_baseline),
        "catboost": _metricas_clasificacion(y_test, score_catboost),
        "baseline_prevalencia": _metricas_clasificacion(y_test, score_prevalencia),
        "regla_simple_experiencia_previa": _metricas_clasificacion(y_test, score_regla_simple),
    }
    comparacion = pd.DataFrame([{"modelo": nombre, **valores} for nombre, valores in metricas.items()])
    for columna in ("pr_auc", "roc_auc", "brier", "precision_top10", "recall_top10", "lift_top10"):
        comparacion[columna] = comparacion[columna].round(4)

    modelo_seleccionado = (
        "catboost" if metricas["catboost"]["pr_auc"] >= metricas["regresion_logistica"]["pr_auc"] else "regresion_logistica"
    )
    score_seleccionado = score_catboost if modelo_seleccionado == "catboost" else score_baseline

    dataset_test = dataset.loc[dataset["fecha_corte"].isin(CORTES_TEST)].reset_index(drop=True)
    dataset_test["_score"] = score_seleccionado
    estabilidad = (
        dataset_test.groupby("fecha_corte")
        .apply(lambda grupo: pd.Series({
            "pr_auc": average_precision_score(grupo["target_adopcion_digital"], grupo["_score"]),
            "tasa_adopcion": grupo["target_adopcion_digital"].mean(),
        }))
        .reset_index()
    )
    estabilidad["pr_auc"] = estabilidad["pr_auc"].round(4)
    estabilidad["tasa_adopcion"] = estabilidad["tasa_adopcion"].round(4)

    decil_seleccionado = _tasa_por_decil(y_test, score_seleccionado)
    decil_seleccionado["tasa_adopcion"] = decil_seleccionado["tasa_adopcion"].round(4)

    logger.info("Calculando explicabilidad (importancias y SHAP sobre muestra)...")
    composicion_producto = _composicion_target_por_producto(fact, dataset_test)
    importancia_baseline = _importancia_baseline(baseline, columnas_numericas)
    importancia_catboost = _importancia_catboost(catboost_modelo, list(x_train.columns))
    shap_top = _shap_catboost(catboost_modelo, x_test, indices_categoricas)

    logger.info("Guardando modelo seleccionado (%s) y metadatos...", modelo_seleccionado)
    artifacts_path = Path(configuracion["outputs"]["artifacts_path"])
    ruta_modelos = artifacts_path / "models"
    ruta_metadata = artifacts_path / "metadata"
    ruta_modelos.mkdir(parents=True, exist_ok=True)
    ruta_metadata.mkdir(parents=True, exist_ok=True)

    if modelo_seleccionado == "catboost":
        ruta_modelo = ruta_modelos / "modelo_adopcion.cbm"
        catboost_modelo.save_model(str(ruta_modelo))
    else:
        import joblib

        ruta_modelo = ruta_modelos / "modelo_adopcion.joblib"
        joblib.dump(baseline, ruta_modelo)

    metadata = {
        "fecha_generacion": datetime.now(timezone.utc).isoformat(),
        "semilla": SEMILLA,
        "cortes_train": CORTES_TRAIN,
        "cortes_test": CORTES_TEST,
        "modelo_seleccionado": modelo_seleccionado,
        "ruta_modelo": str(ruta_modelo),
        "metricas_test": metricas,
        "hiperparametros_catboost": catboost_parametros,
        "estabilidad_por_corte": estabilidad.to_dict("records"),
    }
    (ruta_metadata / "modelos.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    logger.info("Generando reporte en docs/reporte_analitico.md...")
    ruta_reporte = Path(configuracion.get("reporting", {}).get("analytic_report", "docs/reporte_analitico.md"))
    _generar_reporte(
        ruta_reporte, comparacion, estabilidad, decil_seleccionado, composicion_producto,
        importancia_baseline, importancia_catboost, shap_top, modelo_seleccionado,
    )

    logger.info("Modelo seleccionado: %s. PR-AUC test: %.4f", modelo_seleccionado, metricas[
        "catboost" if modelo_seleccionado == "catboost" else "regresion_logistica"
    ]["pr_auc"])
    return {
        "modelo_seleccionado": modelo_seleccionado,
        "ruta_modelo": str(ruta_modelo),
        "ruta_metadata": str(ruta_metadata / "modelos.json"),
        "ruta_reporte": str(ruta_reporte),
        "metricas_test": metricas,
    }
