"""Pruebas de la Etapa 1: auditoría reproducible de fuentes SQLite."""
import sqlite3
from pathlib import Path
from typing import Any, Dict

import pytest

from src.data.auditoria import (
    AuditoriaError,
    conectar_solo_lectura,
    ejecutar_auditoria,
)


def _crear_db(ruta: Path, tabla: str, ddl: str, registros: list) -> None:
    conexion = sqlite3.connect(ruta)
    conexion.execute(f'CREATE TABLE "{tabla}" ({ddl});')
    if registros:
        marcadores = ", ".join(["?"] * len(registros[0]))
        conexion.executemany(f'INSERT INTO "{tabla}" VALUES ({marcadores});', registros)
    conexion.commit()
    conexion.close()


def _crear_fuentes(raw: Path) -> None:
    raw.mkdir(parents=True, exist_ok=True)
    _crear_db(
        raw / "clientes.db",
        "clientes",
        "numero_id INTEGER, grupo_edad TEXT, desc_genero TEXT, desc_segmento TEXT, desc_tipo_de_vivienda TEXT, ingresos_mensuales REAL, total_egresos_mensuales REAL, total_activos REAL, total_pasivos REAL, total_patrimonio REAL",
        [
            (1, "26-35", "femenino", "personal", None, 100.0, 50.0, 500.0, 100.0, 400.0),
            (2, "36-49", "masculino", "plus", "PROPIA", 200.0, 80.0, 900.0, 200.0, 700.0),
            (2, "36-49", "masculino", "plus", "PROPIA", 200.0, 80.0, 900.0, 200.0, 700.0),
        ],
    )
    _crear_db(raw / "estimador_ing.db", "estimador_ing", "numero_id INTEGER, producto TEXT, estimador_ingreso REAL", [(1, "ESTIMADOR INGRESO", 110.0), (2, "ESTIMADOR INGRESO", 220.0)])
    historicas = [
        ("crean_aho_cte.db", "crean_aho_cte", "CUENTA DE AHORRO"),
        ("crean_bolsillos.db", "crean_bolsillos", "BOLSILLOS"),
        ("crean_fiducuenta.db", "crean_fiducuenta", "FIDUCUENTA"),
        ("crean_inv_virtual_cdt.db", "crean_inv_virtual_cdt", "CDT"),
        ("invesbot.db", "invesbot", "INVESBOT"),
    ]
    for archivo, tabla, producto in historicas:
        _crear_db(
            raw / archivo,
            tabla,
            "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
            [("2026-01-01", 1, producto, 0.0), ("2026-02-01", 2, producto, 100.0)],
        )


def _config(raw: Path, reporte: Path) -> Dict[str, Any]:
    return {
        "data": {"raw_path": str(raw)},
        "reporting": {"validation_report": str(reporte)},
    }


def test_conexion_es_solo_lectura(tmp_path: Path) -> None:
    ruta = tmp_path / "prueba.db"
    _crear_db(ruta, "datos", "id INTEGER", [(1,)])
    conexion = conectar_solo_lectura(ruta)
    try:
        with pytest.raises(sqlite3.OperationalError):
            conexion.execute("INSERT INTO datos VALUES (2);")
    finally:
        conexion.close()


def test_auditoria_genera_reporte_idempotente(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    reporte = tmp_path / "docs" / "reporte_validacion.md"
    _crear_fuentes(raw)
    resultado_1 = ejecutar_auditoria(_config(raw, reporte))
    resultado_2 = ejecutar_auditoria(_config(raw, reporte))
    texto = reporte.read_text(encoding="utf-8")
    assert resultado_1["tablas_auditadas"] == 7
    assert resultado_2["tablas_auditadas"] == 7
    assert texto.count("Auditoría reproducible de fuentes") == 1
    assert "Primeras apariciones observadas" in texto
    assert "Cobertura frente a la maestra" in texto
    assert "Comparación con la auditoría exploratoria" in texto


def test_auditoria_detecta_columna_faltante(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    reporte = tmp_path / "reporte.md"
    _crear_fuentes(raw)
    ruta = raw / "invesbot.db"
    ruta.unlink()
    _crear_db(ruta, "invesbot", "fecha TEXT, numero_id INTEGER, producto TEXT", [("2026-01-01", 1, "INVESBOT")])
    with pytest.raises(AuditoriaError, match="saldo"):
        ejecutar_auditoria(_config(raw, reporte))


def test_auditoria_detecta_producto_desconocido_y_ceros(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    reporte = tmp_path / "reporte.md"
    _crear_fuentes(raw)
    ruta = raw / "invesbot.db"
    conexion = sqlite3.connect(ruta)
    conexion.execute("INSERT INTO invesbot VALUES (?, ?, ?, ?)", ("2026-03-01", 1, "PRODUCTO NUEVO", -5.0))
    conexion.commit()
    conexion.close()
    ejecutar_auditoria(_config(raw, reporte))
    texto = reporte.read_text(encoding="utf-8")
    assert "PRODUCTO_DESCONOCIDO" in texto
    assert "SALDO_CERO" in texto
    assert "SALDO_NEGATIVO" in texto


def test_auditoria_no_crea_csv_auxiliares(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    reporte = tmp_path / "docs" / "reporte_validacion.md"
    _crear_fuentes(raw)
    ejecutar_auditoria(_config(raw, reporte))
    assert list(tmp_path.rglob("*.csv")) == []
