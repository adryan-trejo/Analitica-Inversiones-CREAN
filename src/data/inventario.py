"""Inventario de fuentes SQLite esperadas en `data/raw/` (Etapa 1).

Verifica existencia, tamaño y coincidencia de la tabla esperada de cada
fuente, sin leer sus registros. La auditoría profunda de calidad (nulos,
duplicados, cobertura, fechas) también corresponde a la Etapa 1 y se ejecuta
con el paso `auditoria`.
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.data.catalogo import CATALOGO_FUENTES
from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

COLUMNAS_REPORTE = (
    "archivo",
    "tabla_esperada",
    "existe",
    "tabla_encontrada",
    "tamano_mb",
    "estado_validacion",
)


class FuenteFaltanteError(Exception):
    """Se genera cuando una o más fuentes no superan la validación de inventario."""


def _tabla_existe(ruta_db: Path, tabla: str) -> bool:
    """Verifica si `tabla` existe dentro de la base SQLite, sin leer sus registros."""
    conexion = sqlite3.connect(ruta_db.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        cursor = conexion.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?;",
            (tabla,),
        )
        return cursor.fetchone() is not None
    finally:
        conexion.close()


def construir_inventario(raw_path: Path) -> List[Dict[str, Any]]:
    """Construye el inventario de las siete fuentes esperadas dentro de `raw_path`."""
    inventario: List[Dict[str, Any]] = []

    for fuente in CATALOGO_FUENTES:
        ruta_db = raw_path / fuente.archivo
        existe = ruta_db.is_file()
        tabla_encontrada = _tabla_existe(ruta_db, fuente.tabla_esperada) if existe else False
        tamano_mb = round(ruta_db.stat().st_size / (1024 * 1024), 2) if existe else "NA"

        if not existe:
            estado = "FALTA_ARCHIVO"
        elif not tabla_encontrada:
            estado = "FALTA_TABLA"
        else:
            estado = "OK"

        inventario.append(
            {
                "archivo": fuente.archivo,
                "tabla_esperada": fuente.tabla_esperada,
                "existe": existe,
                "tabla_encontrada": tabla_encontrada,
                "tamano_mb": tamano_mb,
                "estado_validacion": estado,
            }
        )

    return inventario


def generar_reporte_inventario(inventario: List[Dict[str, Any]], ruta_reporte: Path) -> None:
    """Incorpora el inventario como una sección de `docs/reporte_validacion.md`."""
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contenido = (
        f"Fecha de ejecución: `{fecha_ejecucion}`\n\n"
        + tabla_markdown(inventario, COLUMNAS_REPORTE)
    )

    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="INVENTARIO_FUENTES",
        titulo="Inventario de fuentes (Etapa 1)",
        contenido=contenido,
    )


def ejecutar_inventario(configuracion: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Orquesta la construcción del inventario y su incorporación al reporte de validación.

    Raises:
        FuenteFaltanteError: Si alguna fuente no supera la validación de inventario.
    """
    raw_path = Path(configuracion["data"]["raw_path"])
    inventario = construir_inventario(raw_path)

    generar_reporte_inventario(inventario, Path("docs/reporte_validacion.md"))

    for item in inventario:
        nivel = logging.INFO if item["estado_validacion"] == "OK" else logging.ERROR
        logger.log(nivel, "Fuente %s -> %s", item["archivo"], item["estado_validacion"])

    fallidas = [item for item in inventario if item["estado_validacion"] != "OK"]
    if fallidas:
        archivos = ", ".join(item["archivo"] for item in fallidas)
        raise FuenteFaltanteError(
            f"Las siguientes fuentes no superaron la validación de inventario: {archivos}"
        )

    return inventario
