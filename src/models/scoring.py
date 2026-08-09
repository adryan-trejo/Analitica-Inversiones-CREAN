"""Saldo potencial, scoring y escenarios (Etapa 5).

Estima el saldo potencial administrado condicionado a la adopción digital con
el método de mediana más simple que resulte defendible (no se entrena un
regresor adicional: los baselines de mediana ya son suficientes, ver
`docs/reporte_analitico.md`). Combina la probabilidad del modelo de Etapa 4
con el saldo potencial para priorizar clientes, y construye segmentos y
escenarios de oportunidad..
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import mean_absolute_error

from src.features.dataset_modelado import PRODUCTOS_PROXY, calcular_fecha_adopcion
from src.models.adopcion import COLUMNAS_CATEGORICAS, VALOR_FALTANTE_CATEGORICO, _columnas_numericas
from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

VENTANA_INF_DIAS = 30
VENTANA_SUP_DIAS = 90
CORTE_SPLIT_BASELINE = pd.Timestamp("2026-02-01")
FACTORES_ESCENARIO = (("conservadora", 0.7), ("base", 1.0), ("expansiva", 1.3))
SEGMENTOS_OPORTUNIDAD = (
    "Alta probabilidad y alto valor",
    "Alta probabilidad y valor moderado",
    "Probabilidad moderada y alto valor",
    "Baja prioridad",
)


def calcular_saldo_ventana(fact: pd.DataFrame, adopciones: pd.DataFrame) -> pd.DataFrame:
    """Calcula el saldo observado entre 30 y 90 días después de la adopción real.

    `adopciones` debe incluir `numero_id`, `fecha_adopcion`, `producto_adopcion`
    (y opcionalmente otras columnas de perfil, que se conservan). Marca
    `seguimiento_completo` en False cuando el horizonte de 90 días excede la
    última fecha disponible en los datos (no se puede evaluar todavía).
    """
    max_fecha_datos = pd.to_datetime(fact["ultima_fecha_mes"]).max()
    proxy = fact.loc[
        fact["producto_original"].isin(PRODUCTOS_PROXY),
        ["numero_id", "producto_original", "primera_fecha_mes", "saldo_ultimo"],
    ].copy()
    proxy["fecha_hist"] = pd.to_datetime(proxy["primera_fecha_mes"])

    combinado = adopciones.rename(columns={"producto_adopcion": "producto_original"}).merge(
        proxy, on=["numero_id", "producto_original"], how="left"
    )
    ventana_inf = combinado["fecha_adopcion"] + pd.Timedelta(days=VENTANA_INF_DIAS)
    ventana_sup = combinado["fecha_adopcion"] + pd.Timedelta(days=VENTANA_SUP_DIAS)
    dentro_ventana = combinado["fecha_hist"].between(ventana_inf, ventana_sup)

    saldo_ventana = (
        combinado.loc[dentro_ventana]
        .groupby("numero_id")["saldo_ultimo"]
        .median()
        .rename("saldo_ventana")
    )

    resultado = adopciones.merge(saldo_ventana, on="numero_id", how="left")
    resultado["seguimiento_completo"] = (
        resultado["fecha_adopcion"] + pd.Timedelta(days=VENTANA_SUP_DIAS)
    ) <= max_fecha_datos
    return resultado


def _mae_baseline(train: pd.DataFrame, test: pd.DataFrame, columnas: Tuple[str, ...]) -> float:
    mediana_global_train = train["saldo_ventana"].median()
    if not columnas:
        prediccion = np.full(len(test), mediana_global_train)
    else:
        tabla = train.groupby(list(columnas))["saldo_ventana"].median()
        prediccion = test.set_index(list(columnas)).index.map(tabla).to_numpy(dtype=float)
        prediccion = np.where(pd.isna(prediccion), mediana_global_train, prediccion)
    return float(mean_absolute_error(test["saldo_ventana"], prediccion))


def comparar_baselines_saldo(historico_evaluable: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    """Compara mediana global, por producto y por segmento-producto con separación temporal."""
    train = historico_evaluable[historico_evaluable["fecha_adopcion"] < CORTE_SPLIT_BASELINE]
    test = historico_evaluable[historico_evaluable["fecha_adopcion"] >= CORTE_SPLIT_BASELINE]

    candidatos: Dict[str, Tuple[str, ...]] = {
        "mediana_global": (),
        "mediana_por_producto": ("producto_adopcion",),
        "mediana_por_segmento_producto": ("desc_segmento", "producto_adopcion"),
    }
    filas = [
        {"metodo": nombre, "mae": round(_mae_baseline(train, test, columnas), 2), "clientes_evaluados": len(test)}
        for nombre, columnas in candidatos.items()
    ]
    tabla = pd.DataFrame(filas).sort_values("mae").reset_index(drop=True)
    return tabla, tabla.iloc[0]["metodo"]


def tabla_saldo_por_segmento(historico_evaluable: pd.DataFrame) -> Tuple[pd.Series, float]:
    """Mediana histórica de saldo por segmento (marginal sobre producto), para el scoring.

    Se usa esta granularidad al calificar clientes porque el producto que un
    cliente aún no adoptante elegiría es desconocido; la comparación con
    `producto_adopcion` en `comparar_baselines_saldo` solo aplica a clientes
    que ya adoptaron (donde el producto real sí se conoce).
    """
    tabla = historico_evaluable.groupby("desc_segmento")["saldo_ventana"].median()
    mediana_global = float(historico_evaluable["saldo_ventana"].median())
    return tabla, mediana_global


def asignar_decil(valores: np.ndarray) -> np.ndarray:
    """Asigna decil 1-10 (10 = valor más alto)."""
    rango = pd.Series(valores).rank(method="first")
    return (pd.qcut(rango, 10, labels=False) + 1).to_numpy()


def asignar_segmento_oportunidad(probabilidad: np.ndarray, valor: np.ndarray) -> np.ndarray:
    """Combina probabilidad y valor condicionado en los 4 segmentos de oportunidad.

    El umbral de "valor" se calcula sobre sus valores únicos (no ponderado por
    frecuencia): si `valor` toma pocos valores distintos y uno de ellos
    concentra la mayoría de los clientes (p. ej. el saldo potencial por
    segmento comercial, donde "personal" es ~76 % de la población), un
    umbral ponderado por frecuencia colapsaría casi todo el universo en un
    solo lado del corte.
    """
    umbral_prob = np.median(probabilidad)
    umbral_valor = np.median(np.unique(valor))
    alta_prob = probabilidad >= umbral_prob
    alto_valor = valor >= umbral_valor
    return np.select(
        [alta_prob & alto_valor, alta_prob & ~alto_valor, (~alta_prob) & alto_valor],
        list(SEGMENTOS_OPORTUNIDAD[:3]),
        default=SEGMENTOS_OPORTUNIDAD[3],
    )


def asignar_nivel_confianza(meses_observados: pd.Series, variables_faltantes: pd.Series) -> np.ndarray:
    """Heurística simple de confianza según historia observada y completitud de datos."""
    alta = (meses_observados >= 6) & (variables_faltantes == 0)
    baja = (variables_faltantes >= 2) | (meses_observados == 0)
    return np.select([alta, baja], ["ALTA", "BAJA"], default="MEDIA")


def _generar_reporte(
    ruta_reporte: Path,
    comparacion_baselines: pd.DataFrame,
    metodo_seleccionado: str,
    resumen_segmentos: pd.DataFrame,
    resumen_oportunidad: pd.DataFrame,
    razones_principales: str,
    corte_scoring: str,
) -> None:
    contenido = [
        f"Scoring generado para el corte {corte_scoring} (último corte disponible en `dataset_modelado`).",
        "Saldo potencial: mediana del saldo observado entre 30 y 90 días después de la adopción real.",
        "",
        "### Qué mide cada columna de `outputs/scoring_clientes.parquet`",
        "",
        "- `probabilidad_adopcion`: salida del modelo CatBoost de Etapa 4 (probabilidad de adoptar "
        "dentro del horizonte de 90 días desde el corte).",
        "- `saldo_potencial_condicional`: mediana histórica de saldo 30-90 días post-adopción, "
        "asignada por segmento comercial (marginal sobre producto, ver más abajo). No depende de la probabilidad.",
        "- `saldo_esperado_ajustado` = `probabilidad_adopcion` × `saldo_potencial_condicional`: valor "
        "esperado agregable, usado para los escenarios y el ranking de valor (`decil_valor`).",
        "- `decil_adopcion` (1-10, 10 = más alto): ranking por `probabilidad_adopcion`.",
        "- `decil_valor` (1-10, 10 = más alto): ranking por `saldo_esperado_ajustado`.",
        "- `segmento_oportunidad`: cruce de `probabilidad_adopcion` y `saldo_potencial_condicional` "
        "(no `saldo_esperado_ajustado`, para no correlacionar ambos ejes) contra sus medianas; el umbral "
        "de valor se calcula sobre los valores únicos observados, no ponderado por frecuencia, para que "
        "el segmento comercial mayoritario (`personal`, ~76 % de los clientes) no domine el corte.",
        "- `nivel_confianza`: ALTA si hay ≥6 meses observados y ninguna variable financiera faltante; "
        "BAJA si faltan ≥2 variables financieras o no hay historia observada; MEDIA en el resto.",
        "- `razones_principales`: top-3 variables por importancia global del modelo (mismas para todos "
        "los clientes; no se calcula SHAP individual para toda la población).",
        "",
        "### Comparación de métodos de saldo potencial (separación temporal, MAE)",
        "",
        tabla_markdown(comparacion_baselines.to_dict("records"), ("metodo", "mae", "clientes_evaluados")),
        "",
        f"Método con menor error: **{metodo_seleccionado}**. Para el scoring (clientes que aún no "
        "adoptan) se usa la mediana histórica por segmento (marginal sobre producto, con respaldo en "
        "la mediana global), porque el producto que elegirían es desconocido antes de adoptar.",
        "",
        "### Segmentos de oportunidad (scoring)",
        "",
        tabla_markdown(
            resumen_segmentos.to_dict("records"),
            ("segmento_oportunidad", "clientes", "probabilidad_promedio", "saldo_esperado_promedio"),
        ),
        "",
        "### Escenarios de oportunidad total (factores explícitos, no observaciones reales)",
        "",
        tabla_markdown(
            resumen_oportunidad.to_dict("records"),
            ("segmento_oportunidad", "oportunidad_conservadora", "oportunidad_base", "oportunidad_expansiva"),
        ),
        "",
        f"Variables más asociadas con la adopción (modelo seleccionado en Etapa 4): {razones_principales}.",
        "",
        "Limitaciones: el saldo potencial es una mediana histórica, no una predicción individual precisa; "
        "los escenarios aplican factores explícitos (0.7 / 1.0 / 1.3) sobre el saldo esperado ajustado y no "
        "deben interpretarse como observaciones reales ni como captación de dinero nuevo. No se distingue "
        "con certeza adquisición, migración o profundización con los datos disponibles.",
    ]
    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="SALDO_SCORING_ESCENARIOS",
        titulo="Saldo potencial, scoring y escenarios (Etapa 5)",
        contenido="\n".join(contenido),
    )


def ejecutar_scoring(configuracion: Dict[str, Any]) -> Dict[str, Any]:
    """Orquesta el cálculo de saldo potencial, scoring, segmentos y escenarios de la Etapa 5."""
    processed_path = Path(configuracion["data"]["processed_path"])
    artifacts_path = Path(configuracion["outputs"]["artifacts_path"])
    outputs_path = Path(configuracion["outputs"]["path"])
    outputs_path.mkdir(parents=True, exist_ok=True)

    logger.info("Cargando dataset_modelado, fact_saldos_mensuales, dim_cliente y modelo de Etapa 4...")
    dataset = pd.read_parquet(processed_path / "dataset_modelado.parquet")
    fact = pd.read_parquet(processed_path / "fact_saldos_mensuales.parquet")
    dim_cliente = pd.read_parquet(processed_path / "dim_cliente.parquet")

    metadata = json.loads((artifacts_path / "metadata" / "modelos.json").read_text(encoding="utf-8"))
    modelo = CatBoostClassifier()
    modelo.load_model(str(artifacts_path / "models" / "modelo_adopcion.cbm"))

    logger.info("Calculando saldo observado 30-90 días después de la adopción real (histórico)...")
    adopciones = calcular_fecha_adopcion(fact).merge(
        dim_cliente[["numero_id", "desc_segmento"]], on="numero_id", how="left"
    )
    historico = calcular_saldo_ventana(fact, adopciones)
    historico_evaluable = historico[historico["seguimiento_completo"] & historico["saldo_ventana"].notna()]

    comparacion_baselines, metodo_seleccionado = comparar_baselines_saldo(historico_evaluable)
    tabla_segmento, mediana_global = tabla_saldo_por_segmento(historico_evaluable)
    logger.info("Método de saldo potencial con menor MAE: %s", metodo_seleccionado)

    corte_scoring = sorted(dataset["fecha_corte"].unique())[-1]
    universo = dataset.loc[dataset["fecha_corte"] == corte_scoring].reset_index(drop=True)
    logger.info("Calificando %s clientes elegibles del corte %s...", len(universo), corte_scoring)

    columnas_numericas = _columnas_numericas(dataset)
    columnas_features = list(COLUMNAS_CATEGORICAS) + columnas_numericas
    x_universo = universo[columnas_features].copy()
    for columna in COLUMNAS_CATEGORICAS:
        x_universo[columna] = x_universo[columna].fillna(VALOR_FALTANTE_CATEGORICO)
    indices_categoricas = [x_universo.columns.get_loc(c) for c in COLUMNAS_CATEGORICAS]
    pool_universo = Pool(x_universo, cat_features=indices_categoricas)

    probabilidad = modelo.predict_proba(pool_universo)[:, 1]
    saldo_potencial = universo["desc_segmento"].map(tabla_segmento).fillna(mediana_global).to_numpy()
    saldo_esperado = probabilidad * saldo_potencial

    importancias = modelo.get_feature_importance()
    orden_importancia = np.argsort(-importancias)[:3]
    razones_principales = ", ".join(x_universo.columns[i] for i in orden_importancia)

    scoring_clientes = pd.DataFrame({
        "numero_id": universo["numero_id"],
        "fecha_score": corte_scoring,
        "probabilidad_adopcion": probabilidad.round(4),
        "saldo_potencial_condicional": saldo_potencial.round(2),
        "saldo_esperado_ajustado": saldo_esperado.round(2),
        "decil_adopcion": asignar_decil(probabilidad),
        "decil_valor": asignar_decil(saldo_esperado),
        "segmento_oportunidad": asignar_segmento_oportunidad(probabilidad, saldo_potencial),
        "nivel_confianza": asignar_nivel_confianza(universo["meses_observados"], universo["variables_financieras_faltantes"]),
        "razones_principales": razones_principales,
        "version_modelo": f"{metadata['modelo_seleccionado']}@{metadata['fecha_generacion'][:10]}",
    })

    assert scoring_clientes["numero_id"].is_unique, "scoring_clientes debe tener una fila por numero_id."
    assert scoring_clientes["probabilidad_adopcion"].between(0, 1).all(), "Probabilidades fuera de [0, 1]."

    ruta_scoring = outputs_path / "scoring_clientes.parquet"
    scoring_clientes.to_parquet(ruta_scoring, index=False)

    resumen_segmentos = (
        scoring_clientes.groupby("segmento_oportunidad", as_index=False)
        .agg(
            clientes=("numero_id", "count"),
            probabilidad_promedio=("probabilidad_adopcion", "mean"),
            saldo_esperado_promedio=("saldo_esperado_ajustado", "mean"),
            saldo_esperado_total=("saldo_esperado_ajustado", "sum"),
        )
    )
    for columna in ("probabilidad_promedio", "saldo_esperado_promedio", "saldo_esperado_total"):
        resumen_segmentos[columna] = resumen_segmentos[columna].round(2)

    resumen_oportunidad = resumen_segmentos.copy()
    for nombre_escenario, factor in FACTORES_ESCENARIO:
        resumen_oportunidad[f"oportunidad_{nombre_escenario}"] = (
            resumen_oportunidad["saldo_esperado_total"] * factor
        ).round(2)

    ruta_resumen = outputs_path / "resumen_oportunidad.csv"
    resumen_oportunidad.to_csv(ruta_resumen, index=False, encoding="utf-8")

    ruta_reporte = Path(configuracion.get("reporting", {}).get("analytic_report", "docs/reporte_analitico.md"))
    _generar_reporte(
        ruta_reporte, comparacion_baselines, metodo_seleccionado, resumen_segmentos,
        resumen_oportunidad, razones_principales, str(corte_scoring),
    )

    logger.info("Scoring generado: %s clientes, método de saldo: %s.", len(scoring_clientes), metodo_seleccionado)
    return {
        "clientes": len(scoring_clientes),
        "metodo_saldo": metodo_seleccionado,
        "ruta_scoring": str(ruta_scoring),
        "ruta_resumen": str(ruta_resumen),
        "ruta_reporte": str(ruta_reporte),
    }
