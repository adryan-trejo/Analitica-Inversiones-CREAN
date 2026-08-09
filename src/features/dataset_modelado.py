"""Dataset de modelado y EDA dirigido (Etapa 3).

Construye el target de adopción digital y variables predictivas disponibles
únicamente hasta cada fecha de corte, a partir de `dim_cliente` y
`fact_saldos_mensuales` (Etapa 2). Usa el proxy y el horizonte aprobados en
`docs/decisiones_analiticas.md`. No entrena modelos.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import matplotlib
from pyarrow import dataset
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

PRODUCTOS_PROXY = ("INVESBOT", "FIDUCUENTA", "INVERSIÓN VIRTUAL")
PRODUCTOS_EXPERIENCIA_INVERSION = ("INVESBOT", "FIDUCUENTA", "INVERSIÓN VIRTUAL", "CDT")

# Meses de carga inicial excluidos como "adopción" (docs/decisiones_analiticas.md, Etapa 2).
EXCLUSIONES_PROXY: Dict[str, List[str]] = {
    "INVESBOT": ["2025-06"],
    "INVERSIÓN VIRTUAL": ["2025-06"],
    "FIDUCUENTA": ["2025-06", "2025-07", "2025-08", "2025-09"],
}

COLUMNAS_FINANCIERAS = (
    "ingresos_mensuales", "total_egresos_mensuales", "total_activos",
    "total_pasivos", "total_patrimonio",
)


def calcular_fecha_adopcion(fact: pd.DataFrame) -> pd.DataFrame:
    """Calcula la primera fecha de adopción digital válida por cliente.

    Una primera aparición en un producto proxy solo cuenta como adopción si
    su mes no pertenece a la ventana de carga inicial excluida en
    `EXCLUSIONES_PROXY`. Si la única aparición de un cliente en un producto
    ocurre dentro de esa ventana, ese producto no genera evento de adopción
    para ese cliente.
    """
    proxy = fact[fact["producto_original"].isin(PRODUCTOS_PROXY)]
    if proxy.empty:
        return pd.DataFrame(columns=["numero_id", "fecha_adopcion", "producto_adopcion"])

    primer_mes = proxy.groupby(["numero_id", "producto_original"], as_index=False)["mes"].min()
    primeras = primer_mes.merge(
        proxy[["numero_id", "producto_original", "mes", "primera_fecha_mes"]],
        on=["numero_id", "producto_original", "mes"],
        how="left",
    ).drop_duplicates(["numero_id", "producto_original"])

    excluido = pd.Series(False, index=primeras.index)
    for producto, meses_excluidos in EXCLUSIONES_PROXY.items():
        seleccion = primeras["producto_original"] == producto
        excluido |= seleccion & primeras["mes"].isin(meses_excluidos)

    validas = primeras.loc[~excluido].copy()
    validas["fecha_adopcion"] = pd.to_datetime(validas["primera_fecha_mes"])
    adopcion = (
        validas.sort_values("fecha_adopcion")
        .drop_duplicates("numero_id", keep="first")
        .rename(columns={"producto_original": "producto_adopcion"})
    )
    return adopcion[["numero_id", "fecha_adopcion", "producto_adopcion"]].reset_index(drop=True)


def construir_variables_corte(fact: pd.DataFrame, fecha_corte: pd.Timestamp) -> pd.DataFrame:
    """Construye variables de comportamiento por cliente usando solo datos anteriores al corte.

    Se filtra por `mes` estrictamente anterior al mes de la fecha de corte
    (los cortes son siempre el día 1 de un mes), lo que evita cualquier
    filtración de información del mes en curso o posterior.
    """
    mes_corte = fecha_corte.strftime("%Y-%m")
    hist = fact[fact["mes"] < mes_corte]

    por_mes = (
        hist.groupby(["numero_id", "mes"], as_index=False)["saldo_ultimo"]
        .sum()
        .rename(columns={"saldo_ultimo": "saldo_mes_total"})
        .sort_values(["numero_id", "mes"])
        .reset_index(drop=True)
    )

    if por_mes.empty:
        return pd.DataFrame(columns=[
            "numero_id", "saldo_total_ultimo", "saldo_promedio_3m", "saldo_promedio_6m",
            "meses_observados", "proporcion_meses_positivos", "tendencia_saldo_simple",
            "recencia_meses", "fecha_maxima_variable_usada", "tenencia_bolsillos",
            "experiencia_previa_inversion", "cantidad_productos",
        ])

    grupo = por_mes.groupby("numero_id")
    meses_observados = grupo.size().rename("meses_observados")
    ultimo = grupo["saldo_mes_total"].last().rename("saldo_total_ultimo")
    primero = grupo["saldo_mes_total"].first()

    rank_desc = por_mes.groupby("numero_id").cumcount(ascending=False)
    prom3 = por_mes.loc[rank_desc < 3].groupby("numero_id")["saldo_mes_total"].mean().rename("saldo_promedio_3m")
    prom6 = por_mes.loc[rank_desc < 6].groupby("numero_id")["saldo_mes_total"].mean().rename("saldo_promedio_6m")

    positivo = (por_mes["saldo_mes_total"] > 0).astype(int)
    prop_positivos = positivo.groupby(por_mes["numero_id"]).mean().rename("proporcion_meses_positivos")

    tendencia = ((ultimo - primero) / meses_observados.sub(1).clip(lower=1)).rename("tendencia_saldo_simple")

    ultimo_mes = grupo["mes"].last()
    periodo_corte = pd.Period(mes_corte, freq="M")
    recencia = (periodo_corte - ultimo_mes.apply(lambda m: pd.Period(m, freq="M"))).apply(lambda offset: offset.n)
    recencia = recencia.rename("recencia_meses")

    fecha_maxima = hist.groupby("numero_id")["ultima_fecha_mes"].max().rename("fecha_maxima_variable_usada")

    bolsillos_positivo = hist[(hist["producto_original"] == "BOLSILLOS") & (hist["saldo_ultimo"] > 0)]
    clientes_bolsillos = set(bolsillos_positivo["numero_id"].unique())

    experiencia = hist[hist["producto_original"].isin(PRODUCTOS_EXPERIENCIA_INVERSION)]
    clientes_experiencia = set(experiencia["numero_id"].unique())

    cantidad_productos = hist.groupby("numero_id")["producto_original"].nunique().rename("cantidad_productos")

    variables = pd.concat(
        [meses_observados, ultimo, prom3, prom6, prop_positivos, tendencia, recencia, fecha_maxima, cantidad_productos],
        axis=1,
    ).reset_index()
    variables["tenencia_bolsillos"] = variables["numero_id"].isin(clientes_bolsillos).astype(int)
    variables["experiencia_previa_inversion"] = variables["numero_id"].isin(clientes_experiencia).astype(int)
    return variables


def construir_dataset_modelado(
    fact: pd.DataFrame,
    dim_cliente: pd.DataFrame,
    cortes: List[str],
    horizonte_dias: int,
) -> pd.DataFrame:
    """Construye el dataset de modelado para todas las fechas de corte.

    Granularidad: `numero_id + fecha_corte`. El universo elegible en cada
    corte excluye a los clientes que ya adoptaron el proxy digital antes o en
    esa fecha (salen del universo de adquisición tras adoptar). El target es
    1 si la adopción válida ocurre después del corte y dentro del horizonte.
    """
    adopciones = calcular_fecha_adopcion(fact)
    base = dim_cliente.merge(adopciones, on="numero_id", how="left")

    piezas = []
    for corte_str in cortes:
        fecha_corte = pd.Timestamp(corte_str)
        limite = fecha_corte + pd.Timedelta(days=horizonte_dias)

        ya_adoptado = base["fecha_adopcion"].notna() & (base["fecha_adopcion"] <= fecha_corte)
        universo = base.loc[~ya_adoptado].drop(columns=["producto_adopcion"]).copy()

        universo["target_adopcion_digital"] = (
            universo["fecha_adopcion"].notna()
            & (universo["fecha_adopcion"] > fecha_corte)
            & (universo["fecha_adopcion"] <= limite)
        ).astype(int)
        universo = universo.drop(columns=["fecha_adopcion"])

        variables = construir_variables_corte(fact, fecha_corte)
        pieza = universo.merge(variables, on="numero_id", how="left")
        pieza.insert(1, "fecha_corte", corte_str)
        piezas.append(pieza)

    dataset = pd.concat(piezas, ignore_index=True)

    dataset["flujo_libre"] = dataset["ingresos_mensuales"] - dataset["total_egresos_mensuales"]
    dataset["patrimonio_calculado"] = dataset["total_activos"] - dataset["total_pasivos"]
    dataset["diferencia_patrimonial"] = dataset["total_patrimonio"] - dataset["patrimonio_calculado"]
    dataset["bandera_vivienda_faltante"] = dataset["desc_tipo_de_vivienda"].isna().astype(int)
    dataset["bandera_patrimonio_negativo"] = (dataset["total_patrimonio"] < 0).astype(int)
    dataset["variables_financieras_faltantes"] = dataset[list(COLUMNAS_FINANCIERAS)].isna().sum(axis=1)

    for columna in ("meses_observados", "cantidad_productos", "tenencia_bolsillos", "experiencia_previa_inversion"):
        dataset[columna] = dataset[columna].fillna(0).astype(int)

    return dataset.reset_index(drop=True)


def _generar_visualizaciones(dataset: pd.DataFrame, ruta_figura: Path) -> None:
    """Genera un panel único (2x3) con las visualizaciones dirigidas del EDA de la Etapa 3."""
    ruta_figura.parent.mkdir(parents=True, exist_ok=True)
    figura, ejes = plt.subplots(2, 3, figsize=(16, 9))

    conteo_target = dataset["target_adopcion_digital"].value_counts().sort_index()
    ejes[0, 0].bar(["No adopta", "Adopta"], conteo_target.reindex([0, 1], fill_value=0))
    ejes[0, 0].set_title("Composición del target")

    tasa_por_corte = dataset.groupby("fecha_corte")["target_adopcion_digital"].mean()
    ejes[0, 1].bar(tasa_por_corte.index.astype(str), tasa_por_corte.values)
    ejes[0, 1].set_title("Tasa de adopción por cohorte")
    ejes[0, 1].tick_params(axis="x", rotation=45)

    tasa_por_segmento = dataset.groupby("desc_segmento")["target_adopcion_digital"].mean().sort_values(ascending=False)
    ejes[0, 2].bar(tasa_por_segmento.index.astype(str), tasa_por_segmento.values)
    ejes[0, 2].set_title("Adopción por segmento")
    ejes[0, 2].tick_params(axis="x", rotation=45)

    dataset.boxplot(column="saldo_total_ultimo", by="target_adopcion_digital", ax=ejes[1, 0], showfliers=False)
    ejes[1, 0].set_title("Liquidez: adoptantes vs. no adoptantes")
    ejes[1, 0].set_xlabel("target")

    dataset.boxplot(column="flujo_libre", by="target_adopcion_digital", ax=ejes[1, 1], showfliers=False)
    ejes[1, 1].set_title("Flujo libre: adoptantes vs. no adoptantes")
    ejes[1, 1].set_xlabel("target")

    tasa_por_experiencia = dataset.groupby("experiencia_previa_inversion")["target_adopcion_digital"].mean()
    ejes[1, 2].bar(["Sin experiencia", "Con experiencia"], tasa_por_experiencia.reindex([0, 1], fill_value=0))
    ejes[1, 2].set_title("Adopción según experiencia previa")

    figura.suptitle("")
    figura.tight_layout()
    figura.savefig(ruta_figura, dpi=110)
    plt.close(figura)


def _generar_reporte_analitico(ruta_reporte: Path, dataset: pd.DataFrame, ruta_figura: Path) -> None:
    resumen_cortes = (
        dataset.groupby("fecha_corte", as_index=False)
        .agg(
            clientes_elegibles=("numero_id", "count"),
            adoptantes=("target_adopcion_digital", "sum"),
            tasa_adopcion=("target_adopcion_digital", "mean"),
        )
    )
    resumen_cortes["tasa_adopcion"] = resumen_cortes["tasa_adopcion"].round(4)

    muestra_auditoria = dataset[["numero_id", "fecha_corte", "fecha_maxima_variable_usada"]].dropna().sample(
        n=min(10, len(dataset.dropna(subset=["fecha_maxima_variable_usada"]))), random_state=42
    )

    contenido = [
        f"`dataset_modelado`: {len(dataset)} filas; granularidad `numero_id + fecha_corte`.",
        "Target: adopción digital (Invesbot, Fiducuenta, Inversión Virtual) dentro de 90 días "
        "posteriores al corte, excluyendo ventanas de carga inicial (ver `docs/decisiones_analiticas.md`).",
        "",
        "### Clientes elegibles y tasa de adopción por fecha de corte",
        "",
        tabla_markdown(resumen_cortes.to_dict("records"), ("fecha_corte", "clientes_elegibles", "adoptantes", "tasa_adopcion")),
        "",
        "### Auditoría de fecha máxima de variables usada (muestra)",
        "",
        "Todas las filas deben cumplir `fecha_maxima_variable_usada < fecha_corte` (no se usa el mes del corte).",
        "",
        tabla_markdown(muestra_auditoria.to_dict("records"), ("numero_id", "fecha_corte", "fecha_maxima_variable_usada")),
        "",
        "### EDA dirigido (6 visualizaciones)",
        "",
        f"![EDA Etapa 3]({ruta_figura.as_posix()})",
        "",
        "1. Composición del target: proporción de adoptantes frente a no adoptantes, fuertemente desbalanceada.",
        "2. Tasa de adopción por cohorte: estabilidad de la tasa entre las cuatro fechas de corte.",
        "3. Adopción por segmento: diferencias de tasa entre segmentos comerciales (`desc_segmento`).",
        "4. Liquidez (saldo total observado) comparada entre adoptantes y no adoptantes.",
        "5. Flujo libre (ingresos menos egresos) comparado entre adoptantes y no adoptantes.",
        "6. Tasa de adopción según experiencia previa de inversión (Invesbot/Fiducuenta/Inversión Virtual/CDT).",
        "",
        "Limitación: las variables de liquidez y flujo libre pueden tener valores extremos "
        "(ver banderas de calidad en el dataset); las visualizaciones excluyen atípicos solo "
        "para la escala del gráfico, no para el dataset persistido.",
    ]
    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="DATASET_MODELADO_EDA",
        titulo="Dataset de modelado y EDA dirigido (Etapa 3)",
        contenido="\n".join(contenido),
    )


def ejecutar_dataset_modelado(configuracion: Dict[str, Any]) -> Dict[str, Any]:
    """Orquesta la construcción del dataset de modelado, el EDA y el reporte de la Etapa 3."""
    processed_path = Path(configuracion["data"]["processed_path"])
    dim_cliente = pd.read_parquet(processed_path / "dim_cliente.parquet")
    fact = pd.read_parquet(processed_path / "fact_saldos_mensuales.parquet")

    cortes = configuracion["modeling"]["cutoff_dates"]
    horizonte_dias = configuracion["modeling"]["adoption_horizon_days"]
    dataset = construir_dataset_modelado(fact, dim_cliente, cortes, horizonte_dias)

    assert dataset[["numero_id", "fecha_corte"]].duplicated().sum() == 0, (
        "El dataset de modelado no cumple unicidad numero_id + fecha_corte."
    )

    ruta_dataset = processed_path / "dataset_modelado.parquet"
    dataset.to_parquet(ruta_dataset, index=False)

    ruta_figura = Path("docs/eda_etapa3.png")
    _generar_visualizaciones(dataset, ruta_figura)

    ruta_reporte = Path(configuracion.get("reporting", {}).get("analytic_report", "docs/reporte_analitico.md"))
    _generar_reporte_analitico(ruta_reporte, dataset, ruta_figura)

    logger.info("Dataset de modelado generado: %s filas en %s.", len(dataset), ruta_dataset)
    return {
        "filas": len(dataset),
        "ruta_dataset": str(ruta_dataset),
        "ruta_reporte": str(ruta_reporte),
    }
