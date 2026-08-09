"""Pruebas de la Etapa 2: capa mensual y validación del proxy de adopción digital."""
import sqlite3
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import pytest

from src.data.mensual import (
    analizar_primeras_apariciones,
    construir_dim_cliente,
    construir_fact_saldos_mensuales,
    deduplicar_clientes,
    ejecutar_capa_mensual,
)


def _crear_db(ruta: Path, tabla: str, ddl: str, registros: list) -> None:
    conexion = sqlite3.connect(ruta)
    conexion.execute(f'CREATE TABLE "{tabla}" ({ddl});')
    marcadores = ", ".join(["?"] * len(registros[0]))
    conexion.executemany(f'INSERT INTO "{tabla}" VALUES ({marcadores});', registros)
    conexion.commit()
    conexion.close()


def _crear_fuentes(raw: Path) -> None:
    raw.mkdir(parents=True, exist_ok=True)
    _crear_db(
        raw / "clientes.db",
        "clientes",
        "numero_id INTEGER, grupo_edad TEXT, desc_genero TEXT, desc_segmento TEXT, "
        "desc_tipo_de_vivienda TEXT, ingresos_mensuales REAL, total_egresos_mensuales REAL, "
        "total_activos REAL, total_pasivos REAL, total_patrimonio REAL",
        [
            (1, "18-25", "femenino", "personal", "PROPIA", 100.0, 50.0, 500.0, 100.0, 400.0),
            (2, "26-35", "masculino", "plus", None, 200.0, 80.0, 900.0, 200.0, 700.0),
            (2, "26-35", "masculino", "plus", None, 200.0, 80.0, 900.0, 200.0, 700.0),
            (3, "36-49", "femenino", "personal", "ARRENDADA", 300.0, 90.0, 300.0, 50.0, 250.0),
        ],
    )
    _crear_db(raw / "estimador_ing.db", "estimador_ing", "numero_id INTEGER, producto TEXT, estimador_ingreso REAL", [(1, "ESTIMADOR INGRESO", 110.0)])

    # INVESBOT: cliente 1 aparece en el mes de arranque (2025-06) y el cliente 3 aparece después (adopción real).
    _crear_db(
        raw / "invesbot.db",
        "invesbot",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [
            ("2025-06-01", 1, "INVESBOT", 1000.0),
            ("2025-06-01", 2, "INVESBOT", 2000.0),
            ("2025-08-01", 3, "INVESBOT", 500.0),
            ("2025-08-15", 3, "INVESBOT", 700.0),
        ],
    )
    # FIDUCUENTA: carga inicial extendida en los primeros dos meses (salto de cobertura esperado).
    _crear_db(
        raw / "crean_fiducuenta.db",
        "crean_fiducuenta",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [
            ("2025-06-01", 1, "FIDUCUENTA", 0.0),
            ("2025-06-01", 2, "FIDUCUENTA", 0.0),
            ("2025-06-01", 3, "FIDUCUENTA", 0.0),
            ("2025-07-01", 1, "FIDUCUENTA", 0.0),
        ],
    )
    _crear_db(raw / "crean_bolsillos.db", "crean_bolsillos", "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL", [("2025-06-01", 1, "BOLSILLOS", 10.0)])
    _crear_db(
        raw / "crean_inv_virtual_cdt.db",
        "crean_inv_virtual_cdt",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [("2025-06-01", 1, "CDT", 500.0), ("2025-06-01", 1, "INVERSIóN VIRTUAL", 300.0)],
    )
    _crear_db(
        raw / "crean_aho_cte.db",
        "crean_aho_cte",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [
            ("2025-06-01", 1, "CUENTA DE AHORRO", 1000.0),
            ("2025-06-15", 1, "CUENTA DE AHORRO", 1200.0),
        ],
    )


def _config(raw: Path, processed: Path) -> Dict[str, Any]:
    return {"data": {"raw_path": str(raw), "processed_path": str(processed)}}


def test_deduplicar_clientes_conserva_un_registro_por_id(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes(raw)
    dim_cliente = construir_dim_cliente(_config(raw, tmp_path / "processed"))
    assert dim_cliente["numero_id"].is_unique
    assert len(dim_cliente) == 3


def test_deduplicar_clientes_es_determinístico() -> None:
    df = pd.DataFrame(
        {"_rowid": [2, 1], "numero_id": [1, 1], "ingresos_mensuales": [100.0, 100.0]}
    )
    resultado = deduplicar_clientes(df)
    assert len(resultado) == 1
    assert "_rowid" not in resultado.columns


def test_fact_saldos_mensuales_granularidad_unica(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes(raw)
    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    claves = fact[["numero_id", "mes", "producto_original"]]
    assert not claves.duplicated().any()


def test_fact_saldos_mensuales_usa_ultimo_saldo_por_fecha_real(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes(raw)
    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    fila = fact[(fact["numero_id"] == 1) & (fact["producto_original"] == "CUENTA DE AHORRO")].iloc[0]
    assert fila["saldo_ultimo"] == 1200.0
    assert fila["numero_observaciones"] == 2


def test_fact_saldos_mensuales_distingue_ausencia_de_cero(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes(raw)
    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    fila = fact[(fact["numero_id"] == 2) & (fact["producto_original"] == "FIDUCUENTA")].iloc[0]
    assert fila["estado_observacion"] == "OBSERVADO_CON_CERO"
    # El cliente 2 nunca aparece en INVESBOT en meses posteriores: no existe fila artificial.
    assert fact[(fact["numero_id"] == 2) & (fact["producto_original"] == "CUENTA DE AHORRO")].empty


def test_reconciliacion_de_clientes_por_producto(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes(raw)
    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    invesbot = fact[fact["producto_original"] == "INVESBOT"]
    assert invesbot["numero_id"].nunique() == 3


def _crear_fuentes_con_volumen(raw: Path) -> None:
    """Crea fuentes con proporciones realistas para probar la detección de saltos de cobertura.

    INVESBOT: 20 clientes en el mes de arranque y solo 2 clientes nuevos el mes
    siguiente (10 %, adopción orgánica). FIDUCUENTA: 20 clientes en el mes de
    arranque y 10 clientes nuevos el mes siguiente (50 %, carga inicial extendida).
    """
    raw.mkdir(parents=True, exist_ok=True)
    _crear_db(
        raw / "clientes.db",
        "clientes",
        "numero_id INTEGER, grupo_edad TEXT, desc_genero TEXT, desc_segmento TEXT, "
        "desc_tipo_de_vivienda TEXT, ingresos_mensuales REAL, total_egresos_mensuales REAL, "
        "total_activos REAL, total_pasivos REAL, total_patrimonio REAL",
        [(i, "18-25", "femenino", "personal", "PROPIA", 100.0, 50.0, 500.0, 100.0, 400.0) for i in range(1, 31)],
    )
    _crear_db(raw / "estimador_ing.db", "estimador_ing", "numero_id INTEGER, producto TEXT, estimador_ingreso REAL", [(1, "ESTIMADOR INGRESO", 110.0)])
    _crear_db(
        raw / "invesbot.db",
        "invesbot",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [("2025-06-01", i, "INVESBOT", 100.0) for i in range(1, 21)]
        + [("2025-07-01", i, "INVESBOT", 100.0) for i in range(21, 23)],
    )
    _crear_db(
        raw / "crean_fiducuenta.db",
        "crean_fiducuenta",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [("2025-06-01", i, "FIDUCUENTA", 0.0) for i in range(1, 21)]
        + [("2025-07-01", i, "FIDUCUENTA", 0.0) for i in range(21, 31)],
    )
    _crear_db(raw / "crean_bolsillos.db", "crean_bolsillos", "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL", [("2025-06-01", 1, "BOLSILLOS", 10.0)])
    _crear_db(
        raw / "crean_inv_virtual_cdt.db",
        "crean_inv_virtual_cdt",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [("2025-06-01", 1, "CDT", 500.0)],
    )
    _crear_db(
        raw / "crean_aho_cte.db",
        "crean_aho_cte",
        "fecha TEXT, numero_id INTEGER, producto TEXT, saldo REAL",
        [("2025-06-01", 1, "CUENTA DE AHORRO", 1000.0)],
    )


def test_analizar_primeras_apariciones_detecta_salto_de_cobertura(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _crear_fuentes_con_volumen(raw)
    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    primeras = analizar_primeras_apariciones(fact)

    fiducuenta = primeras[primeras["producto_original"] == "FIDUCUENTA"].set_index("mes_primera")
    assert bool(fiducuenta.loc["2025-07", "salto_cobertura"])

    invesbot = primeras[primeras["producto_original"] == "INVESBOT"].set_index("mes_primera")
    assert not bool(invesbot.loc["2025-07", "salto_cobertura"])


def test_analizar_primeras_apariciones_no_marca_picos_organicos_aislados(tmp_path: Path) -> None:
    """Un pico de clientes nuevos en un mes intermedio no contiguo al arranque no debe
    tratarse como carga inicial (regresión: INVESBOT mostraba esto con datos reales)."""
    raw = tmp_path / "raw"
    _crear_fuentes_con_volumen(raw)
    conexion = sqlite3.connect(raw / "invesbot.db")
    # Pico aislado en 2025-09, después de que el mes 2 (2025-07) ya se había estabilizado.
    conexion.executemany(
        "INSERT INTO invesbot VALUES (?, ?, ?, ?)",
        [("2025-09-01", 200 + i, "INVESBOT", 100.0) for i in range(6)],
    )
    conexion.commit()
    conexion.close()

    fact = construir_fact_saldos_mensuales(_config(raw, tmp_path / "processed"))
    primeras = analizar_primeras_apariciones(fact)
    invesbot = primeras[primeras["producto_original"] == "INVESBOT"].set_index("mes_primera")
    assert not bool(invesbot.loc["2025-09", "salto_cobertura"])


def test_ejecutar_capa_mensual_persiste_parquet_y_reporte(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    processed = tmp_path / "processed"
    _crear_fuentes(raw)
    configuracion = _config(raw, processed)
    configuracion["reporting"] = {"analytic_report": str(tmp_path / "docs" / "reporte_analitico.md")}

    resultado = ejecutar_capa_mensual(configuracion)

    assert Path(resultado["ruta_dim_cliente"]).is_file()
    assert Path(resultado["ruta_fact"]).is_file()
    assert Path(resultado["ruta_reporte"]).is_file()
    assert resultado["clientes"] == 3

    texto = Path(resultado["ruta_reporte"]).read_text(encoding="utf-8")
    assert "Capa mensual y validación del proxy" in texto
    assert texto.count("Capa mensual y validación del proxy") == 1
