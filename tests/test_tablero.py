"""Pruebas de la Etapa 6: funciones puras del tablero (sin Streamlit)."""
from pathlib import Path

import pandas as pd
import pytest

from src.reporting.markdown import actualizar_seccion, leer_seccion, parsear_tabla_bajo_encabezado, tabla_markdown
from src.reporting.tablero import (
    calcular_resumen_ejecutivo,
    cargar_metadata_modelo,
    cargar_resumen_oportunidad,
    cargar_scoring,
    enmascarar_numero_id,
    obtener_tabla_reporte,
    preparar_tabla_priorizada,
)


def test_enmascarar_numero_id_no_expone_el_valor_real() -> None:
    enmascarado = enmascarar_numero_id(-8245474570363424359)
    assert "8245474570363424359" not in enmascarado
    assert enmascarado == "cliente_...4359"


def test_enmascarar_numero_id_rellena_ids_cortos() -> None:
    assert enmascarar_numero_id(7) == "cliente_...0007"


def _scoring_sintetico() -> pd.DataFrame:
    return pd.DataFrame({
        "numero_id": [1, 2, 3],
        "probabilidad_adopcion": [0.9, 0.5, 0.1],
        "saldo_potencial_condicional": [1000.0, 2000.0, 500.0],
        "saldo_esperado_ajustado": [900.0, 1000.0, 50.0],
        "decil_adopcion": [10, 6, 1],
        "decil_valor": [9, 10, 1],
        "segmento_oportunidad": ["Alta probabilidad y alto valor", "Probabilidad moderada y alto valor", "Baja prioridad"],
        "nivel_confianza": ["ALTA", "MEDIA", "BAJA"],
    })


def test_preparar_tabla_priorizada_enmascara_y_ordena() -> None:
    tabla = preparar_tabla_priorizada(_scoring_sintetico())
    assert "numero_id" not in tabla.columns
    assert "cliente_id" in tabla.columns
    assert tabla["saldo_esperado_ajustado"].tolist() == [1000.0, 900.0, 50.0]


def test_calcular_resumen_ejecutivo() -> None:
    scoring = _scoring_sintetico()
    resumen_oportunidad = pd.DataFrame({
        "segmento_oportunidad": ["Alta probabilidad y alto valor", "Baja prioridad"],
        "oportunidad_conservadora": [100.0, 10.0],
        "oportunidad_base": [200.0, 20.0],
        "oportunidad_expansiva": [300.0, 30.0],
    })
    resumen = calcular_resumen_ejecutivo(scoring, resumen_oportunidad)
    assert resumen["clientes_elegibles"] == 3
    assert resumen["adopciones_esperadas"] == pytest.approx(1.5)
    assert resumen["saldo_esperado_total"] == pytest.approx(1950.0)
    assert resumen["oportunidad_base"] == pytest.approx(220.0)
    assert resumen["distribucion_segmentos"]["Baja prioridad"] == 1


def test_cargar_scoring_lanza_error_claro_si_falta(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="run_pipeline.py --step scoring"):
        cargar_scoring(tmp_path / "no_existe.parquet")


def test_cargar_resumen_oportunidad_lanza_error_claro_si_falta(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        cargar_resumen_oportunidad(tmp_path / "no_existe.csv")


def test_cargar_metadata_modelo_lanza_error_claro_si_falta(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="modelo_adopcion"):
        cargar_metadata_modelo(tmp_path / "no_existe.json")


def test_leer_seccion_y_parsear_tabla(tmp_path: Path) -> None:
    ruta = tmp_path / "reporte.md"
    actualizar_seccion(
        ruta_reporte=ruta,
        id_seccion="PRUEBA",
        titulo="Prueba",
        contenido="### Encabezado\n\n" + tabla_markdown(
            [{"a": 1, "b": 2}, {"a": 3, "b": 4}], ("a", "b")
        ) + "\n\nTexto posterior que no debe incluirse en la tabla.",
    )
    seccion = leer_seccion(ruta, "PRUEBA")
    filas = parsear_tabla_bajo_encabezado(seccion, "### Encabezado")
    assert filas == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]


def test_obtener_tabla_reporte_reutiliza_tabla_existente(tmp_path: Path) -> None:
    ruta = tmp_path / "reporte.md"
    actualizar_seccion(
        ruta_reporte=ruta,
        id_seccion="MODELO_ADOPCION",
        titulo="Modelo",
        contenido="### Tasa observada por decil\n\n" + tabla_markdown(
            [{"decil": 10, "tasa_adopcion": 0.06}], ("decil", "tasa_adopcion")
        ),
    )
    filas = obtener_tabla_reporte(ruta, "MODELO_ADOPCION", "### Tasa observada por decil")
    assert filas[0]["decil"] == "10"
