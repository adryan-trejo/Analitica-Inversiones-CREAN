"""Catálogo de fuentes y productos utilizados en la integración de datos CREAN.

Este módulo centraliza dos catálogos que no deben mezclarse:

1. `CATALOGO_FUENTES`: describe los archivos `.db` esperados en `data/raw/`,
   la tabla que debe contener cada uno y sus columnas obligatorias.
2. `CATALOGO_PRODUCTOS`: describe, para cada producto observado en las fuentes,
   su `familia_producto` (agrupación financiera) y su `canal_producto`
   (evidencia de canal digital), como conceptos separados.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class FuenteEsperada:
    """Describe una fuente SQLite esperada dentro de `data/raw/`."""

    archivo: str
    tabla_esperada: str
    columnas_obligatorias: Tuple[str, ...]


CATALOGO_FUENTES: Tuple[FuenteEsperada, ...] = (
    FuenteEsperada(
        archivo="clientes.db",
        tabla_esperada="clientes",
        columnas_obligatorias=(
            "numero_id",
            "grupo_edad",
            "desc_genero",
            "desc_segmento",
            "desc_tipo_de_vivienda",
            "ingresos_mensuales",
            "total_egresos_mensuales",
            "total_activos",
            "total_pasivos",
            "total_patrimonio",
        ),
    ),
    FuenteEsperada(
        archivo="estimador_ing.db",
        tabla_esperada="estimador_ing",
        columnas_obligatorias=("numero_id", "producto", "estimador_ingreso"),
    ),
    FuenteEsperada(
        archivo="crean_aho_cte.db",
        tabla_esperada="crean_aho_cte",
        columnas_obligatorias=("fecha", "numero_id", "producto", "saldo"),
    ),
    FuenteEsperada(
        archivo="crean_bolsillos.db",
        tabla_esperada="crean_bolsillos",
        columnas_obligatorias=("fecha", "numero_id", "producto", "saldo"),
    ),
    FuenteEsperada(
        archivo="crean_fiducuenta.db",
        tabla_esperada="crean_fiducuenta",
        columnas_obligatorias=("fecha", "numero_id", "producto", "saldo"),
    ),
    FuenteEsperada(
        archivo="crean_inv_virtual_cdt.db",
        tabla_esperada="crean_inv_virtual_cdt",
        columnas_obligatorias=("fecha", "numero_id", "producto", "saldo"),
    ),
    FuenteEsperada(
        archivo="invesbot.db",
        tabla_esperada="invesbot",
        columnas_obligatorias=("fecha", "numero_id", "producto", "saldo"),
    ),
)


@dataclass(frozen=True)
class ProductoCatalogado:
    """Clasificación analítica de un producto observado en las fuentes."""

    producto_original: str
    familia_producto: str
    canal_producto: str


# Canal "NO_APLICA" se usa para productos de liquidez y ahorro por metas, donde
# el canal de apertura no es relevante para el proxy de adopción digital de
# inversión. Es una decisión de catalogación, no un supuesto de negocio validado.
CATALOGO_PRODUCTOS: Dict[str, ProductoCatalogado] = {
    "INVESBOT": ProductoCatalogado("INVESBOT", "PORTAFOLIO_DIGITAL", "DIGITAL_CONFIRMADO"),
    "FIDUCUENTA": ProductoCatalogado("FIDUCUENTA", "FONDO_INVERSION_FLEXIBLE", "DIGITAL_CONFIRMADO"),
    "INVERSIÓN VIRTUAL": ProductoCatalogado("INVERSIÓN VIRTUAL", "INVERSION_A_TERMINO", "DIGITAL_CONFIRMADO"),
    "CDT": ProductoCatalogado("CDT", "INVERSION_A_TERMINO", "NO_DETERMINADO"),
    "CUENTA DE AHORRO": ProductoCatalogado("CUENTA DE AHORRO", "LIQUIDEZ", "NO_APLICA"),
    "CUENTA DE CORRIENTE": ProductoCatalogado("CUENTA DE CORRIENTE", "LIQUIDEZ", "NO_APLICA"),
    "BOLSILLOS": ProductoCatalogado("BOLSILLOS", "AHORRO_POR_METAS", "NO_APLICA"),
}


def normalizar_producto(producto: str) -> str:
    """Normaliza un nombre de producto para buscarlo en el catálogo."""
    return producto.strip().upper()


def obtener_producto_catalogado(producto: str) -> ProductoCatalogado:
    """Devuelve la clasificación catalogada de un producto.

    Raises:
        KeyError: Si el producto no pertenece al catálogo conocido.
    """
    clave = normalizar_producto(producto)

    if clave not in CATALOGO_PRODUCTOS:
        raise KeyError(f"Producto no catalogado: '{producto}'")

    return CATALOGO_PRODUCTOS[clave]
