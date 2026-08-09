"""Utilidades para consolidar resultados en reportes Markdown mediante secciones nombradas.

Permite que distintos comandos (inventario, calidad, pruebas, etc.) actualicen
su propia sección dentro de un mismo reporte consolidado sin pisar el resto
del contenido, evitando así archivos auxiliares independientes por control.
"""

from pathlib import Path
from typing import Dict, List, Mapping, Sequence

MARCADOR_INICIO = "<!-- INICIO:{id_seccion} -->"
MARCADOR_FIN = "<!-- FIN:{id_seccion} -->"


def tabla_markdown(filas: Sequence[Mapping[str, object]], columnas: Sequence[str]) -> str:
    """Convierte una lista de diccionarios en una tabla Markdown."""
    if not filas:
        return "_Sin resultados._"

    encabezado = "| " + " | ".join(columnas) + " |"
    separador = "| " + " | ".join(["---"] * len(columnas)) + " |"

    lineas = [encabezado, separador]
    for fila in filas:
        valores = [str(fila.get(columna, "")) for columna in columnas]
        lineas.append("| " + " | ".join(valores) + " |")

    return "\n".join(lineas)


def actualizar_seccion(
    ruta_reporte: Path,
    id_seccion: str,
    titulo: str,
    contenido: str,
) -> None:
    """Crea o reemplaza una sección delimitada por marcadores dentro de un reporte Markdown.

    Si el reporte no existe, se crea con un encabezado general. Si la sección
    ya existe, se reemplaza in situ conservando el resto del documento; si no
    existe, se agrega al final.
    """
    inicio = MARCADOR_INICIO.format(id_seccion=id_seccion)
    fin = MARCADOR_FIN.format(id_seccion=id_seccion)

    bloque = f"{inicio}\n## {titulo}\n\n{contenido}\n{fin}\n"

    if not ruta_reporte.exists():
        ruta_reporte.parent.mkdir(parents=True, exist_ok=True)
        ruta_reporte.write_text("# Reporte de validación CREAN\n\n" + bloque, encoding="utf-8")
        return

    texto_actual = ruta_reporte.read_text(encoding="utf-8")

    if inicio in texto_actual and fin in texto_actual:
        pre = texto_actual.split(inicio)[0]
        post = texto_actual.split(fin)[1]
        nuevo_texto = pre + bloque + post
    else:
        separador = "" if texto_actual.endswith("\n\n") else "\n"
        nuevo_texto = texto_actual + separador + bloque

    ruta_reporte.write_text(nuevo_texto, encoding="utf-8")


def leer_seccion(ruta_reporte: Path, id_seccion: str) -> str:
    """Devuelve el contenido de una sección (sin los marcadores de inicio/fin).

    Permite reutilizar tablas ya generadas por otras etapas (p. ej. en el
    tablero) sin volver a calcularlas. Lanza `KeyError` si la sección no existe.
    """
    texto = ruta_reporte.read_text(encoding="utf-8")
    inicio = MARCADOR_INICIO.format(id_seccion=id_seccion)
    fin = MARCADOR_FIN.format(id_seccion=id_seccion)

    if inicio not in texto or fin not in texto:
        raise KeyError(f"Sección no encontrada en el reporte: {id_seccion}")

    return texto.split(inicio)[1].split(fin)[0]


def parsear_tabla_bajo_encabezado(seccion: str, encabezado: str) -> List[Dict[str, str]]:
    """Extrae como lista de diccionarios la primera tabla Markdown bajo un `### encabezado`.

    Lanza `KeyError` si el encabezado no existe. Devuelve lista vacía si el
    encabezado existe pero no hay una tabla válida debajo.
    """
    lineas = seccion.splitlines()
    try:
        inicio = next(i for i, linea in enumerate(lineas) if linea.strip() == encabezado) + 1
    except StopIteration:
        raise KeyError(f"Encabezado no encontrado: {encabezado}")

    filas_tabla: List[str] = []
    for linea in lineas[inicio:]:
        if linea.strip().startswith("|"):
            filas_tabla.append(linea.strip())
        elif filas_tabla:
            break

    if len(filas_tabla) < 2:
        return []

    columnas = [columna.strip() for columna in filas_tabla[0].strip("|").split("|")]
    return [
        dict(zip(columnas, (valor.strip() for valor in linea.strip("|").split("|"))))
        for linea in filas_tabla[2:]
    ]
