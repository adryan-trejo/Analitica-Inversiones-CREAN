"""Carga y validación de la configuración centralizada del proyecto (`config.yaml`)."""

from pathlib import Path
from typing import Any, Dict

import yaml

CLAVES_OBLIGATORIAS = ("project", "data", "modeling", "outputs")


class ConfigInvalidaError(Exception):
    """Se genera cuando `config.yaml` no cumple la estructura mínima esperada."""


def cargar_configuracion(ruta_config: str = "config.yaml") -> Dict[str, Any]:
    """Carga `config.yaml` y valida que contenga las secciones obligatorias.

    Args:
        ruta_config: Ruta relativa (o absoluta) al archivo de configuración.

    Returns:
        Diccionario con la configuración cargada.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ConfigInvalidaError: Si el contenido no es un mapeo válido o faltan secciones.
    """
    ruta = Path(ruta_config)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración: {ruta}"
        )

    with ruta.open("r", encoding="utf-8") as archivo:
        configuracion = yaml.safe_load(archivo)

    if not isinstance(configuracion, dict):
        raise ConfigInvalidaError(
            "El archivo de configuración no contiene un mapeo válido."
        )

    faltantes = [
        clave for clave in CLAVES_OBLIGATORIAS if clave not in configuracion
    ]

    if faltantes:
        raise ConfigInvalidaError(
            f"Faltan secciones obligatorias en config.yaml: {faltantes}"
        )

    return configuracion
