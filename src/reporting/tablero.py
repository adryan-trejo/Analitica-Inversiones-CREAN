"""Funciones puras para preparar los datos del tablero de la Etapa 6.

Separadas de `app/app.py` para que la lógica de carga, enmascarado y
agregación sea testable sin depender de Streamlit. El tablero solo consume
resultados precomputados (`outputs/`, `artifacts/metadata/`, `docs/`); no
entrena ni recalcula modelos.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from src.reporting.markdown import leer_seccion, parsear_tabla_bajo_encabezado

COLUMNAS_TABLA_PRIORIZADA = (
    "cliente_id",
    "probabilidad_adopcion",
    "saldo_potencial_condicional",
    "saldo_esperado_ajustado",
    "decil_adopcion",
    "decil_valor",
    "segmento_oportunidad",
    "nivel_confianza",
)


def enmascarar_numero_id(numero_id: int) -> str:
    """Enmascara `numero_id` mostrando solo los últimos 4 dígitos, sin exponer el identificador real."""
    return f"cliente_...{str(abs(int(numero_id))).zfill(4)[-4:]}"


def cargar_scoring(ruta: Path) -> pd.DataFrame:
    """Carga `scoring_clientes.parquet`. Lanza `FileNotFoundError` si no existe."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta: python run_pipeline.py --step scoring")
    return pd.read_parquet(ruta)


def cargar_resumen_oportunidad(ruta: Path) -> pd.DataFrame:
    """Carga `resumen_oportunidad.csv`. Lanza `FileNotFoundError` si no existe."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta: python run_pipeline.py --step scoring")
    return pd.read_csv(ruta)


def cargar_metadata_modelo(ruta: Path) -> Dict[str, Any]:
    """Carga `modelos.json`. Lanza `FileNotFoundError` si no existe."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta: python run_pipeline.py --step modelo_adopcion")
    return json.loads(ruta.read_text(encoding="utf-8"))


def calcular_resumen_ejecutivo(scoring: pd.DataFrame, resumen_oportunidad: pd.DataFrame) -> Dict[str, Any]:
    """Calcula los indicadores del Resumen ejecutivo a partir del scoring y la oportunidad por segmento."""
    return {
        "clientes_elegibles": int(len(scoring)),
        "adopciones_esperadas": float(scoring["probabilidad_adopcion"].sum()),
        "saldo_esperado_total": float(scoring["saldo_esperado_ajustado"].sum()),
        "oportunidad_conservadora": float(resumen_oportunidad["oportunidad_conservadora"].sum()),
        "oportunidad_base": float(resumen_oportunidad["oportunidad_base"].sum()),
        "oportunidad_expansiva": float(resumen_oportunidad["oportunidad_expansiva"].sum()),
        "distribucion_segmentos": scoring["segmento_oportunidad"].value_counts().to_dict(),
    }


def preparar_tabla_priorizada(scoring: pd.DataFrame) -> pd.DataFrame:
    """Prepara la tabla de priorización enmascarando `numero_id` y ordenando por valor esperado."""
    tabla = scoring.copy()
    tabla["cliente_id"] = tabla["numero_id"].map(enmascarar_numero_id)
    tabla = tabla.sort_values("saldo_esperado_ajustado", ascending=False)
    return tabla[list(COLUMNAS_TABLA_PRIORIZADA)].reset_index(drop=True)


def obtener_tabla_reporte(ruta_reporte: Path, id_seccion: str, encabezado: str) -> List[Dict[str, str]]:
    """Reutiliza una tabla ya generada en `docs/reporte_analitico.md` (no la recalcula)."""
    if not ruta_reporte.exists():
        raise FileNotFoundError(f"No se encontró {ruta_reporte}.")
    seccion = leer_seccion(ruta_reporte, id_seccion)
    return parsear_tabla_bajo_encabezado(seccion, encabezado)
