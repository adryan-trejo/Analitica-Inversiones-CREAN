"""Tablero Streamlit de la solución CREAN (Etapa 6).

Consume únicamente resultados precomputados (`outputs/`, `artifacts/metadata/`,
`docs/reporte_analitico.md`); no entrena ni recalcula modelos al iniciar.
Tres vistas: Resumen ejecutivo, Priorización y Modelo y calidad.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.reporting.tablero import (
    calcular_resumen_ejecutivo,
    cargar_metadata_modelo,
    cargar_resumen_oportunidad,
    cargar_scoring,
    obtener_tabla_reporte,
    preparar_tabla_priorizada,
)

RUTA_SCORING = Path("outputs/scoring_clientes.parquet")
RUTA_RESUMEN_OPORTUNIDAD = Path("outputs/resumen_oportunidad.csv")
RUTA_METADATA = Path("artifacts/metadata/modelos.json")
RUTA_REPORTE = Path("docs/reporte_analitico.md")

st.set_page_config(page_title="CREAN - App de inversiones", layout="wide")


@st.cache_data
def _cargar_scoring() -> pd.DataFrame:
    return cargar_scoring(RUTA_SCORING)


@st.cache_data
def _cargar_resumen_oportunidad() -> pd.DataFrame:
    return cargar_resumen_oportunidad(RUTA_RESUMEN_OPORTUNIDAD)


@st.cache_data
def _cargar_metadata():
    return cargar_metadata_modelo(RUTA_METADATA)


@st.cache_data
def _cargar_tabla_reporte(id_seccion: str, encabezado: str):
    return obtener_tabla_reporte(RUTA_REPORTE, id_seccion, encabezado)


def _formato_cop(valor: float) -> str:
    return f"${valor / 1e9:,.1f} mil millones"


def _vista_resumen_ejecutivo() -> None:
    st.header("Resumen ejecutivo")
    scoring = _cargar_scoring()
    resumen_oportunidad = _cargar_resumen_oportunidad()
    resumen = calcular_resumen_ejecutivo(scoring, resumen_oportunidad)

    columnas = st.columns(4)
    columnas[0].metric("Clientes elegibles", f"{resumen['clientes_elegibles']:,}")
    columnas[1].metric("Adopciones esperadas", f"{resumen['adopciones_esperadas']:,.0f}")
    columnas[2].metric("Saldo esperado total", _formato_cop(resumen["saldo_esperado_total"]))
    prioritarios = scoring["segmento_oportunidad"].str.startswith("Alta probabilidad").sum()
    columnas[3].metric("Clientes prioritarios", f"{prioritarios:,}", f"{prioritarios / len(scoring):.0%} de elegibles")

    st.subheader("Oportunidad total por escenario")
    st.caption(
        "Los escenarios aplican factores explícitos (0.7 / 1.0 / 1.3) sobre el saldo esperado "
        "ajustado; no son observaciones reales ni captación garantizada."
    )
    columnas_escenario = st.columns(3)
    columnas_escenario[0].metric("Conservador", _formato_cop(resumen["oportunidad_conservadora"]))
    columnas_escenario[1].metric("Base", _formato_cop(resumen["oportunidad_base"]))
    columnas_escenario[2].metric("Expansivo", _formato_cop(resumen["oportunidad_expansiva"]))

    st.success(
    "Recomendación: iniciar el lanzamiento con el segmento de alta probabilidad "
    r"y alto valor, que reúne cerca del 22 % de los clientes y concentra el 74 % "
    "de la oportunidad base."
    )
    
    st.subheader("¿Dónde está la oportunidad?")

    distribucion = (
        pd.Series(resumen["distribucion_segmentos"])
        .rename_axis("segmento_oportunidad")
        .reset_index(name="clientes")
        .sort_values("clientes")
    )

    figura = px.bar(
        distribucion,
        x="clientes",
        y="segmento_oportunidad",
        text="clientes",
        orientation="h",
        color="segmento_oportunidad",
    )
    figura.update_layout(
        showlegend=False,
        xaxis_title="Clientes",
        yaxis_title="",
    )
    st.plotly_chart(figura, use_container_width=True)


def _vista_priorizacion() -> None:
    st.header("Priorización de clientes")
    scoring = _cargar_scoring()

    columnas_filtro = st.columns(2)
    segmentos = columnas_filtro[0].multiselect(
        "Segmento de oportunidad", options=sorted(scoring["segmento_oportunidad"].unique()),
        default=sorted(scoring["segmento_oportunidad"].unique()),
    )
    confianzas = columnas_filtro[1].multiselect(
        "Nivel de confianza", options=sorted(scoring["nivel_confianza"].unique()),
        default=sorted(scoring["nivel_confianza"].unique()),
    )

    filtrado = scoring[
        scoring["segmento_oportunidad"].isin(segmentos) & scoring["nivel_confianza"].isin(confianzas)
    ]
    st.caption(f"{len(filtrado):,} clientes cumplen los filtros (de {len(scoring):,} elegibles totales).")
    if not filtrado.empty:
        kpis = st.columns(3)
        kpis[0].metric("Clientes seleccionados", f"{len(filtrado):,}")
        kpis[1].metric("Probabilidad promedio", f"{filtrado['probabilidad_adopcion'].mean():.2%}")
        kpis[2].metric("Saldo esperado", _formato_cop(filtrado["saldo_esperado_ajustado"].sum()))

    st.subheader("Matriz probabilidad vs. saldo potencial")
    muestra = filtrado.sample(n=min(5000, len(filtrado)), random_state=42) if len(filtrado) else filtrado
    if not muestra.empty:
        figura = px.scatter(
            muestra, x="probabilidad_adopcion", y="saldo_potencial_condicional",
            color="segmento_oportunidad", opacity=0.5,
            labels={"probabilidad_adopcion": "Probabilidad de adopción", "saldo_potencial_condicional": "Saldo potencial condicional"},
        )
        figura.update_xaxes(tickformat=".1%")
        figura.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(figura, use_container_width=True)
        st.caption("Muestra de hasta 5,000 clientes para la visualización; los filtros y la descarga usan el total filtrado.")
    else:
        st.warning("No hay clientes que cumplan los filtros seleccionados.")

    st.subheader("Tabla priorizada")
    tabla = preparar_tabla_priorizada(filtrado)
    st.dataframe(tabla.head(500), use_container_width=True)
    st.download_button(
        "Descargar CSV (clientes filtrados)",
        data=tabla.to_csv(index=False).encode("utf-8"),
        file_name="priorizacion_clientes.csv",
        mime="text/csv",
    )


def _vista_modelo_calidad() -> None:
    st.header("Modelo y calidad")
    metadata = _cargar_metadata()
    modelo_seleccionado = metadata["modelo_seleccionado"]
    st.caption(f"Modelo seleccionado: **{modelo_seleccionado}**.")

    st.subheader("Desempeño del modelo seleccionado")

    metricas = metadata["metricas_test"][modelo_seleccionado]
    columnas = st.columns(5)
    columnas[0].metric("PR-AUC", f"{metricas['pr_auc']:.4f}")
    columnas[1].metric("Precision top 10 %", f"{metricas['precision_top10']:.1%}")
    columnas[2].metric("Recall top 10 %", f"{metricas['recall_top10']:.1%}")
    columnas[3].metric("Lift top 10 %", f"{metricas['lift_top10']:.2f}x")
    columnas[4].metric("Brier", f"{metricas['brier']:.4f}")

    st.caption(
        "**PR-AUC:** capacidad general para priorizar adoptantes. "
        "**Precision:** tasa de adopción dentro del top 10 %. "
        "**Recall:** proporción de adoptantes capturada en ese grupo. "
        "**Lift:** mejora frente a seleccionar clientes al azar. "
        "**Brier:** error de las probabilidades, donde un valor menor es mejor."
    )

    st.info(
        f"El 10 % de clientes con mayor score concentra el "
        f"{metricas['recall_top10']:.0%} de los adoptantes y presenta una tasa "
        f"de adopción {metricas['lift_top10']:.2f} veces superior al promedio."
    )

    try:
        tabla_decil = _cargar_tabla_reporte(
            "MODELO_ADOPCION",
            f"### Tasa observada por decil ({modelo_seleccionado}, prueba)",
        )

        st.subheader("Tasa observada por decil")
        st.caption(
            "Los clientes se ordenan por su score y se dividen en diez grupos del mismo tamaño. "
            "El decil 10 contiene los clientes con mayor probabilidad estimada. La tasa de adopción "
            "muestra el porcentaje que realmente adoptó dentro de cada grupo."
        )

        decil = pd.DataFrame(tabla_decil).astype(
            {"decil": int, "tasa_adopcion": float}
        )
        figura = px.bar(
            decil, x="decil", y="tasa_adopcion", text_auto=".1%",
        )
        figura.update_yaxes(
            tickformat=".1%", title="Tasa observada de adopción",
        )
        figura.update_xaxes(
            title="Decil de score, 10 = mayor prioridad", dtick=1,
        )
        st.plotly_chart(figura, use_container_width=True)

        st.caption(
            "La adopción aumenta de forma consistente hacia los deciles superiores, "
            "lo que confirma que el modelo ordena adecuadamente a los clientes."
        )
    except KeyError:
        st.info("No se encontró la tabla de deciles en el reporte.")

    try:
        tabla_importancia = _cargar_tabla_reporte(
            "MODELO_ADOPCION",
            "Top 10 importancia global de CatBoost:",
        )

        st.subheader("Variables más relevantes")
        st.caption(
            "La importancia representa cuánto utiliza el modelo cada variable para generar "
            "sus predicciones. Un valor mayor indica mayor aporte relativo al modelo, pero "
            "no implica causalidad ni señala por sí solo una relación positiva o negativa."
        )

        st.dataframe(
            pd.DataFrame(tabla_importancia),
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "La priorización está explicada principalmente por capacidad financiera, "
            "amplitud de la relación con el banco y comportamiento histórico de ahorro."
        )
    except KeyError:
        st.info("No se encontró la tabla de importancia de variables en el reporte.")

    st.subheader("Limitaciones principales")
    st.markdown(
        "- El desbalance es fuerte (prevalencia ~1-1.4 %); precision/recall/lift en el top 10 % son "
        "más informativos que el ROC-AUC.\n"
        "- El saldo potencial es una mediana histórica, no una predicción individual precisa.\n"
        "- Los escenarios usan factores explícitos, no son observaciones reales ni captación garantizada.\n"
        "- La App no tiene historia propia: el modelo usa un proxy con productos análogos.\n"
        "- El modelo debe recalibrarse con adopción real una vez la App esté disponible."
    )


def main() -> None:
    st.title("Oportunidad App de Inversiones CREAN")
    st.caption(
        "Priorización de clientes actuales para el lanzamiento, estimación de saldo "
        "potencial administrado y dimensionamiento de escenarios."
    )
    vista = st.sidebar.radio("Vista", ("Resumen ejecutivo", "Priorización", "Modelo y calidad"))

    try:
        if vista == "Resumen ejecutivo":
            _vista_resumen_ejecutivo()
        elif vista == "Priorización":
            _vista_priorizacion()
        else:
            _vista_modelo_calidad()
    except FileNotFoundError as error:
        st.error(str(error))


if __name__ == "__main__":
    main()
