"""Pruebas de la Etapa 1: catálogo normalizado de productos."""

import pytest

from src.data.catalogo import (
    CATALOGO_FUENTES,
    CATALOGO_PRODUCTOS,
    normalizar_producto,
    obtener_producto_catalogado,
)


def test_catalogo_fuentes_tiene_siete_fuentes() -> None:
    """El catálogo debe declarar exactamente las siete fuentes esperadas."""
    assert len(CATALOGO_FUENTES) == 7


@pytest.mark.parametrize(
    "producto_crudo,familia_esperada,canal_esperado",
    [
        ("invesbot", "PORTAFOLIO_DIGITAL", "DIGITAL_CONFIRMADO"),
        (" Fiducuenta ", "FONDO_INVERSION_FLEXIBLE", "DIGITAL_CONFIRMADO"),
        ("inversión virtual", "INVERSION_A_TERMINO", "DIGITAL_CONFIRMADO"),
        ("cdt", "INVERSION_A_TERMINO", "NO_DETERMINADO"),
        ("cuenta de ahorro", "LIQUIDEZ", "NO_APLICA"),
        ("cuenta de corriente", "LIQUIDEZ", "NO_APLICA"),
        ("bolsillos", "AHORRO_POR_METAS", "NO_APLICA"),
    ],
)
def test_mapeo_de_productos(
    producto_crudo: str, familia_esperada: str, canal_esperado: str
) -> None:
    """Cada producto debe mapear a su familia y canal, sin mezclar ambos conceptos."""
    resultado = obtener_producto_catalogado(producto_crudo)

    assert resultado.familia_producto == familia_esperada
    assert resultado.canal_producto == canal_esperado


def test_producto_desconocido_falla() -> None:
    """Un producto fuera del catálogo debe fallar explícitamente, no ignorarse."""
    with pytest.raises(KeyError):
        obtener_producto_catalogado("PRODUCTO_INEXISTENTE")


def test_familia_y_canal_son_conceptos_independientes() -> None:
    """CDT e Inversión Virtual comparten familia pero difieren en canal."""
    cdt = CATALOGO_PRODUCTOS["CDT"]
    inversion_virtual = CATALOGO_PRODUCTOS["INVERSIÓN VIRTUAL"]

    assert cdt.familia_producto == inversion_virtual.familia_producto
    assert cdt.canal_producto != inversion_virtual.canal_producto


def test_normalizar_producto() -> None:
    """La normalización debe recortar espacios y pasar a mayúsculas conservando tildes."""
    assert normalizar_producto("  inversión virtual ") == "INVERSIÓN VIRTUAL"
