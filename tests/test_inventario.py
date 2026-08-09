"""Pruebas de la Etapa 1: inventario reproducible de fuentes en `data/raw/`."""

import sqlite3
from pathlib import Path
from typing import Any, Dict

import pytest

from src.data.inventario import (
    FuenteFaltanteError,
    construir_inventario,
    ejecutar_inventario,
    generar_reporte_inventario,
)

MAPEO_ARCHIVO_TABLA = {
    "clientes.db": "clientes",
    "estimador_ing.db": "estimador_ing",
    "crean_aho_cte.db": "crean_aho_cte",
    "crean_bolsillos.db": "crean_bolsillos",
    "crean_fiducuenta.db": "crean_fiducuenta",
    "crean_inv_virtual_cdt.db": "crean_inv_virtual_cdt",
    "invesbot.db": "invesbot",
}


def _crear_db_minima(ruta: Path, tabla: str) -> None:
    """Crea una base SQLite mínima con una tabla y un registro, para pruebas."""
    conexion = sqlite3.connect(ruta)
    conexion.execute(f"CREATE TABLE {tabla} (numero_id INTEGER);")
    conexion.execute(f"INSERT INTO {tabla} (numero_id) VALUES (1);")
    conexion.commit()
    conexion.close()


def _crear_raw_completo(raw_path: Path) -> None:
    """Crea las siete fuentes esperadas con su tabla correcta, dentro de `raw_path`."""
    raw_path.mkdir(parents=True, exist_ok=True)
    for archivo, tabla in MAPEO_ARCHIVO_TABLA.items():
        _crear_db_minima(raw_path / archivo, tabla)


def test_construir_inventario_todo_ok(tmp_path: Path) -> None:
    """Cuando las siete fuentes existen con su tabla esperada, el estado debe ser OK."""
    raw_path = tmp_path / "data" / "raw"
    _crear_raw_completo(raw_path)

    inventario = construir_inventario(raw_path)

    assert len(inventario) == 7
    assert all(item["estado_validacion"] == "OK" for item in inventario)


def test_construir_inventario_detecta_archivo_faltante(tmp_path: Path) -> None:
    """Si falta un archivo `.db`, debe marcarse `FALTA_ARCHIVO`."""
    raw_path = tmp_path / "data" / "raw"
    _crear_raw_completo(raw_path)
    (raw_path / "invesbot.db").unlink()

    inventario = construir_inventario(raw_path)
    item_invesbot = next(item for item in inventario if item["archivo"] == "invesbot.db")

    assert item_invesbot["estado_validacion"] == "FALTA_ARCHIVO"
    assert item_invesbot["existe"] is False


def test_construir_inventario_detecta_tabla_incorrecta(tmp_path: Path) -> None:
    """Si el archivo existe pero no contiene la tabla esperada, debe marcarse `FALTA_TABLA`."""
    raw_path = tmp_path / "data" / "raw"
    _crear_raw_completo(raw_path)
    (raw_path / "invesbot.db").unlink()
    _crear_db_minima(raw_path / "invesbot.db", "tabla_incorrecta")

    inventario = construir_inventario(raw_path)
    item_invesbot = next(item for item in inventario if item["archivo"] == "invesbot.db")

    assert item_invesbot["estado_validacion"] == "FALTA_TABLA"


def test_generar_reporte_inventario_es_idempotente(tmp_path: Path) -> None:
    """Ejecutar el inventario dos veces debe actualizar la sección, no duplicarla."""
    raw_path = tmp_path / "data" / "raw"
    _crear_raw_completo(raw_path)
    ruta_reporte = tmp_path / "docs" / "reporte_validacion.md"

    inventario = construir_inventario(raw_path)
    generar_reporte_inventario(inventario, ruta_reporte)
    generar_reporte_inventario(inventario, ruta_reporte)

    texto = ruta_reporte.read_text(encoding="utf-8")
    assert texto.count("Inventario de fuentes") == 1


def test_ejecutar_inventario_falla_con_mensaje_claro_si_falta_fuente(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Debe fallar con un mensaje claro cuando falta alguna de las siete fuentes."""
    raw_path = tmp_path / "data" / "raw"
    _crear_raw_completo(raw_path)
    (raw_path / "invesbot.db").unlink()

    monkeypatch.chdir(tmp_path)
    configuracion: Dict[str, Any] = {"data": {"raw_path": str(raw_path)}}

    with pytest.raises(FuenteFaltanteError, match="invesbot.db"):
        ejecutar_inventario(configuracion)
