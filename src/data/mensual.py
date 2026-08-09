"""Capa mensual y validación del proxy de adopción digital (Etapa 2).

Construye `dim_cliente` (una fila por cliente) y `fact_saldos_mensuales`
(granularidad `numero_id + mes + producto_original`) a partir de las cinco
fuentes históricas, y produce evidencia de cobertura y primeras apariciones
para aprobar el proxy de adopción digital. No construye todavía el dataset
de modelado ni entrena modelos.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from src.data.catalogo import CATALOGO_FUENTES, normalizar_producto, obtener_producto_catalogado
from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

FUENTES_MENSUALES = (
    "crean_aho_cte",
    "crean_bolsillos",
    "crean_fiducuenta",
    "crean_inv_virtual_cdt",
    "invesbot",
)

PRODUCTOS_PROXY_DIGITAL = ("INVESBOT", "FIDUCUENTA", "INVERSIÓN VIRTUAL")
PRODUCTO_SENSIBILIDAD = "CDT"
UMBRAL_SALTO_COBERTURA = 0.15  # proporción del primer mes que se considera aún "carga inicial"


def _ruta_fuente(raw_path: Path, tabla: str) -> Path:
    for fuente in CATALOGO_FUENTES:
        if fuente.tabla_esperada == tabla:
            return raw_path / fuente.archivo
    raise KeyError(f"Tabla no catalogada: {tabla}")


def _leer_tabla_solo_lectura(ruta_db: Path, consulta: str) -> pd.DataFrame:
    conexion = sqlite3.connect(ruta_db.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        return pd.read_sql_query(consulta, conexion)
    finally:
        conexion.close()


def deduplicar_clientes(clientes: pd.DataFrame) -> pd.DataFrame:
    """Elimina `numero_id` duplicados conservando el primer registro por `rowid`.

    Regla determinística: los duplicados observados en la auditoría son copias
    exactas de todas las columnas, por lo que basta con conservar la primera
    aparición ordenada por `rowid` (orden de inserción original).
    """
    return (
        clientes.sort_values("_rowid")
        .drop_duplicates(subset="numero_id", keep="first")
        .drop(columns="_rowid")
        .reset_index(drop=True)
    )


def construir_dim_cliente(configuracion: Dict[str, Any]) -> pd.DataFrame:
    """Construye `dim_cliente`: una fila por `numero_id` con perfil financiero y sociodemográfico."""
    raw_path = Path(configuracion["data"]["raw_path"])
    clientes = _leer_tabla_solo_lectura(
        _ruta_fuente(raw_path, "clientes"),
        "SELECT rowid AS _rowid, * FROM clientes;",
    )
    return deduplicar_clientes(clientes)


def construir_fact_saldos_mensuales(configuracion: Dict[str, Any]) -> pd.DataFrame:
    """Construye `fact_saldos_mensuales` agregando las cinco fuentes históricas.

    Granularidad: `numero_id + mes + producto_original`. Solo se persisten
    combinaciones observadas (sin crear un panel artificial completo), y el
    último saldo se calcula respetando la fecha real más reciente del mes.
    """
    raw_path = Path(configuracion["data"]["raw_path"])
    agregados = []

    for tabla in FUENTES_MENSUALES:
        datos = _leer_tabla_solo_lectura(
            _ruta_fuente(raw_path, tabla),
            f"SELECT fecha, numero_id, producto, saldo FROM {tabla};",
        )
        datos = datos.dropna(subset=["numero_id", "producto", "fecha", "saldo"])
        datos["producto_original"] = datos["producto"].map(normalizar_producto)
        datos["mes"] = datos["fecha"].str.slice(0, 7)
        datos = datos.sort_values("fecha")

        agregado = datos.groupby(["numero_id", "mes", "producto_original"], as_index=False).agg(
            saldo_ultimo=("saldo", "last"),
            saldo_promedio=("saldo", "mean"),
            saldo_minimo=("saldo", "min"),
            saldo_maximo=("saldo", "max"),
            numero_observaciones=("saldo", "count"),
            primera_fecha_mes=("fecha", "min"),
            ultima_fecha_mes=("fecha", "max"),
        )
        agregados.append(agregado)

    fact = pd.concat(agregados, ignore_index=True)
    fact["estado_observacion"] = fact["saldo_ultimo"].apply(
        lambda saldo: "OBSERVADO_CON_CERO" if saldo == 0 else "OBSERVADO_CON_SALDO"
    )
    catalogado = fact["producto_original"].map(obtener_producto_catalogado)
    fact["familia_producto"] = catalogado.map(lambda producto: producto.familia_producto)
    fact["canal_producto"] = catalogado.map(lambda producto: producto.canal_producto)

    columnas = [
        "numero_id", "mes", "producto_original", "familia_producto", "canal_producto",
        "saldo_ultimo", "saldo_promedio", "saldo_minimo", "saldo_maximo",
        "numero_observaciones", "primera_fecha_mes", "ultima_fecha_mes", "estado_observacion",
    ]
    return fact[columnas].sort_values(["numero_id", "mes", "producto_original"]).reset_index(drop=True)


def analizar_primeras_apariciones(fact: pd.DataFrame) -> pd.DataFrame:
    """Calcula, por producto, cuántos clientes aparecen por primera vez en cada mes.

    Marca `salto_cobertura` cuando un mes distinto al primero todavía concentra
    una proporción relevante de clientes nuevos respecto al primer mes de la
    fuente, señal de carga inicial extendida en lugar de adopción orgánica.
    """
    primeras = fact.groupby(["numero_id", "producto_original"], as_index=False)["mes"].min()
    primeras = primeras.rename(columns={"mes": "mes_primera"})
    resumen = (
        primeras.groupby(["producto_original", "mes_primera"], as_index=False)
        .size()
        .rename(columns={"size": "clientes_nuevos"})
        .sort_values(["producto_original", "mes_primera"])
    )

    clientes_primer_mes = resumen.groupby("producto_original")["clientes_nuevos"].transform("first")
    resumen["proporcion_primer_mes"] = (resumen["clientes_nuevos"] / clientes_primer_mes).round(3)
    resumen["salto_cobertura"] = resumen.groupby("producto_original", group_keys=False)[
        "proporcion_primer_mes"
    ].apply(_marcar_carga_inicial_contigua)
    return resumen.reset_index(drop=True)


def _marcar_carga_inicial_contigua(proporciones: pd.Series) -> pd.Series:
    """Marca como salto solo los meses posteriores al primero que forman un bloque
    contiguo de carga inicial (proporción > umbral), deteniéndose en el primer mes
    que ya se estabiliza. Evita marcar picos org\u00e1nicos aislados más adelante en la serie.
    """
    salto = pd.Series(False, index=proporciones.index)
    valores = proporciones.to_numpy()
    for posicion in range(1, len(valores)):
        if valores[posicion] > UMBRAL_SALTO_COBERTURA:
            salto.iloc[posicion] = True
        else:
            break
    return salto


def _generar_reporte_analitico(
    ruta_reporte: Path,
    dim_cliente: pd.DataFrame,
    fact: pd.DataFrame,
    primeras_apariciones: pd.DataFrame,
) -> None:
    resumen_fuentes = (
        fact.groupby("producto_original", as_index=False)
        .agg(clientes=("numero_id", "nunique"), filas_mensuales=("numero_id", "count"))
        .sort_values("clientes", ascending=False)
    )
    saltos = primeras_apariciones[primeras_apariciones["salto_cobertura"]]

    contenido = [
        f"`dim_cliente`: {len(dim_cliente)} clientes (deduplicados).",
        f"`fact_saldos_mensuales`: {len(fact)} filas; granularidad `numero_id + mes + producto_original`.",
        "",
        "### Clientes y filas por producto en `fact_saldos_mensuales`",
        "",
        tabla_markdown(resumen_fuentes.to_dict("records"), ("producto_original", "clientes", "filas_mensuales")),
        "",
        "### Primeras apariciones por producto y mes (proxy y sensibilidad)",
        "",
        "Un `salto_cobertura` indica que ese mes todavía concentra una proporción "
        f"relevante (> {int(UMBRAL_SALTO_COBERTURA * 100)} % del primer mes) de clientes "
        "nuevos, y por tanto no se interpreta como adopción orgánica.",
        "",
        tabla_markdown(
            primeras_apariciones.to_dict("records"),
            ("producto_original", "mes_primera", "clientes_nuevos", "proporcion_primer_mes", "salto_cobertura"),
        ),
        "",
        "### Meses excluidos del proxy por salto de cobertura",
        "",
        tabla_markdown(saltos.to_dict("records"), ("producto_original", "mes_primera", "clientes_nuevos", "proporcion_primer_mes"))
        if not saltos.empty
        else "_Ningún producto presenta saltos de cobertura adicionales al primer mes._",
    ]
    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="CAPA_MENSUAL_PROXY",
        titulo="Capa mensual y validación del proxy (Etapa 2)",
        contenido="\n".join(contenido),
    )


def ejecutar_capa_mensual(configuracion: Dict[str, Any]) -> Dict[str, Any]:
    """Orquesta la construcción de `dim_cliente`, `fact_saldos_mensuales` y la evidencia del proxy."""
    processed_path = Path(configuracion["data"]["processed_path"])
    processed_path.mkdir(parents=True, exist_ok=True)

    dim_cliente = construir_dim_cliente(configuracion)
    fact = construir_fact_saldos_mensuales(configuracion)
    primeras_apariciones = analizar_primeras_apariciones(fact)

    ruta_dim_cliente = processed_path / "dim_cliente.parquet"
    ruta_fact = processed_path / "fact_saldos_mensuales.parquet"
    dim_cliente.to_parquet(ruta_dim_cliente, index=False)
    fact.to_parquet(ruta_fact, index=False)

    ruta_reporte = Path(configuracion.get("reporting", {}).get("analytic_report", "docs/reporte_analitico.md"))
    _generar_reporte_analitico(ruta_reporte, dim_cliente, fact, primeras_apariciones)

    logger.info(
        "Capa mensual generada: %s clientes, %s filas en fact_saldos_mensuales.",
        len(dim_cliente),
        len(fact),
    )
    return {
        "clientes": len(dim_cliente),
        "filas_fact": len(fact),
        "ruta_dim_cliente": str(ruta_dim_cliente),
        "ruta_fact": str(ruta_fact),
        "ruta_reporte": str(ruta_reporte),
    }
