"""Pruebas de la Etapa 1: importación del paquete y validación de `config.yaml`."""

from pathlib import Path

import pytest

from src.config import ConfigInvalidaError, cargar_configuracion


def test_import_paquete_src() -> None:
    """El paquete `src` y sus submódulos deben poder importarse sin errores."""
    import src  # noqa: F401
    import src.config  # noqa: F401


def test_config_yaml_del_repositorio_es_valido() -> None:
    """El `config.yaml` del repositorio debe cargar y contener las secciones obligatorias."""
    configuracion = cargar_configuracion("config.yaml")

    assert "project" in configuracion
    assert "data" in configuracion
    assert "modeling" in configuracion
    assert "outputs" in configuracion
    assert configuracion["project"]["python_version"] == "3.9.12"


def test_cargar_configuracion_falla_si_no_existe(tmp_path: Path) -> None:
    """Debe fallar con un error claro si el archivo de configuración no existe."""
    ruta_inexistente = tmp_path / "no_existe.yaml"

    with pytest.raises(FileNotFoundError):
        cargar_configuracion(str(ruta_inexistente))


def test_cargar_configuracion_falla_si_faltan_secciones(tmp_path: Path) -> None:
    """Debe fallar con un error claro si faltan secciones obligatorias."""
    ruta_config = tmp_path / "config_incompleto.yaml"
    ruta_config.write_text("project:\n  random_seed: 1\n", encoding="utf-8")

    with pytest.raises(ConfigInvalidaError):
        cargar_configuracion(str(ruta_config))
