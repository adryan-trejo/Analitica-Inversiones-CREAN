"""Auditoría reproducible de las fuentes SQLite CREAN (Etapa 1).

El módulo ejecuta consultas agregadas directamente en SQLite, abre todas las
bases en modo de solo lectura y consolida los resultados en un único reporte
Markdown. No corrige, imputa, deduplica ni transforma los datos originales.
"""
import logging
import sqlite3
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from src.data.catalogo import CATALOGO_FUENTES, CATALOGO_PRODUCTOS, normalizar_producto
from src.reporting.markdown import actualizar_seccion, tabla_markdown

logger = logging.getLogger(__name__)

SEVERIDAD_ERROR = "ERROR"
SEVERIDAD_ADVERTENCIA = "ADVERTENCIA"
SEVERIDAD_INFORMACION = "INFORMACION"

FUENTES_HISTORICAS = {
    "crean_aho_cte",
    "crean_bolsillos",
    "crean_fiducuenta",
    "crean_inv_virtual_cdt",
    "invesbot",
}

TIPOS_ESPERADOS: Dict[str, Dict[str, Tuple[str, ...]]] = {
    "clientes": {
        "numero_id": ("INTEGER",),
        "grupo_edad": ("TEXT",),
        "desc_genero": ("TEXT",),
        "desc_segmento": ("TEXT",),
        "desc_tipo_de_vivienda": ("TEXT",),
        "ingresos_mensuales": ("REAL", "INTEGER", "NUMERIC"),
        "total_egresos_mensuales": ("REAL", "INTEGER", "NUMERIC"),
        "total_activos": ("REAL", "INTEGER", "NUMERIC"),
        "total_pasivos": ("REAL", "INTEGER", "NUMERIC"),
        "total_patrimonio": ("REAL", "INTEGER", "NUMERIC"),
    },
    "estimador_ing": {
        "numero_id": ("INTEGER",),
        "producto": ("TEXT",),
        "estimador_ingreso": ("REAL", "INTEGER", "NUMERIC"),
    },
}
for _tabla in FUENTES_HISTORICAS:
    TIPOS_ESPERADOS[_tabla] = {
        "fecha": ("TEXT", "DATE", "DATETIME"),
        "numero_id": ("INTEGER",),
        "producto": ("TEXT",),
        "saldo": ("REAL", "INTEGER", "NUMERIC"),
    }

REFERENCIA_AUDITORIA: Dict[str, Dict[str, Any]] = {
    "clientes": {"registros": 860231, "clientes": 860223},
    "estimador_ing": {"registros": 745792, "clientes": 745792},
    "crean_aho_cte": {"registros": 1000000, "clientes": 475719},
    "crean_bolsillos": {"registros": 1000000, "clientes": 260714},
    "crean_fiducuenta": {"registros": 1000000, "clientes": 181021},
    "crean_inv_virtual_cdt": {"registros": 994177, "clientes": 84104},
    "invesbot": {"registros": 1000000, "clientes": 5214},
}


class AuditoriaError(Exception):
    """Error estructural que impide completar la auditoría."""


def escapar_identificador(nombre: str) -> str:
    """Escapa un identificador para uso seguro en sentencias SQLite."""
    return '"' + nombre.replace('"', '""') + '"'


def conectar_solo_lectura(ruta_db: Path) -> sqlite3.Connection:
    """Abre una base SQLite existente en modo de solo lectura."""
    if not ruta_db.is_file():
        raise FileNotFoundError(f"No se encontró la base SQLite: {ruta_db}")
    conexion = sqlite3.connect(ruta_db.resolve().as_uri() + "?mode=ro", uri=True)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA query_only = ON;")
    return conexion


def _consultar_uno(conexion: sqlite3.Connection, consulta: str) -> Dict[str, Any]:
    fila = conexion.execute(consulta).fetchone()
    return dict(fila) if fila is not None else {}


def _consultar_varios(conexion: sqlite3.Connection, consulta: str) -> List[Dict[str, Any]]:
    return [dict(fila) for fila in conexion.execute(consulta).fetchall()]


def _cantidad_nulos_sql(columnas: Sequence[str]) -> str:
    partes = []
    for columna in columnas:
        col = escapar_identificador(columna)
        partes.append(f"SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS {columna}_nulos")
    return ", ".join(partes)


def _duplicados_por_clave(
    conexion: sqlite3.Connection,
    tabla: str,
    claves: Sequence[str],
    incluir_saldo: bool = False,
) -> Dict[str, Any]:
    """Cuenta combinaciones duplicadas de `claves` dentro de `tabla`.

    Si `incluir_saldo` es verdadero, además reporta cuántas de esas claves
    duplicadas tienen valores de `saldo` distintos entre sí.
    """
    claves_sql = ", ".join(escapar_identificador(c) for c in claves)
    filtro = " AND ".join(f"{escapar_identificador(c)} IS NOT NULL" for c in claves)
    columna_extra = ", COUNT(DISTINCT saldo) AS saldos_distintos" if incluir_saldo else ""
    select_extra = (
        ", COALESCE(SUM(CASE WHEN saldos_distintos > 1 THEN 1 ELSE 0 END), 0) AS claves_con_saldos_distintos"
        if incluir_saldo
        else ""
    )
    return _consultar_uno(
        conexion,
        f"""
        SELECT COUNT(*) AS combinaciones_duplicadas,
               COALESCE(SUM(n - 1), 0) AS registros_excedentes,
               COALESCE(MAX(n), 0) AS maximo_por_combinacion{select_extra}
        FROM (SELECT {claves_sql}, COUNT(*) AS n{columna_extra} FROM {escapar_identificador(tabla)}
              WHERE {filtro} GROUP BY {claves_sql} HAVING COUNT(*) > 1);
        """,
    )


def _alertas_por_umbral(
    tabla: str,
    resumen: Mapping[str, Any],
    reglas: Sequence[Tuple[str, str, str]],
) -> List[Dict[str, Any]]:
    """Genera una alerta por cada `(campo, control, severidad)` cuyo valor en `resumen` sea mayor que cero."""
    return [
        _alerta(severidad, tabla, control, str(resumen[campo]))
        for campo, control, severidad in reglas
        if resumen.get(campo, 0)
    ]


def _esquema(conexion: sqlite3.Connection, tabla: str) -> List[Dict[str, Any]]:
    filas = _consultar_varios(
        conexion,
        f"PRAGMA table_info({escapar_identificador(tabla)});",
    )
    return [
        {
            "columna": fila["name"],
            "tipo_sqlite": (fila["type"] or "SIN_TIPO").upper(),
            "not_null": fila["notnull"],
            "llave_primaria": fila["pk"],
        }
        for fila in filas
    ]


def _validar_esquema(
    tabla: str,
    esquema: Sequence[Mapping[str, Any]],
    columnas_obligatorias: Sequence[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    disponibles = {str(fila["columna"]): str(fila["tipo_sqlite"]).upper() for fila in esquema}
    faltantes = sorted(set(columnas_obligatorias) - set(disponibles))
    alertas: List[Dict[str, Any]] = []
    tipos = TIPOS_ESPERADOS.get(tabla, {})

    for columna in faltantes:
        alertas.append(_alerta(SEVERIDAD_ERROR, tabla, "COLUMNA_FALTANTE", columna))

    validacion = []
    for columna in columnas_obligatorias:
        tipo = disponibles.get(columna, "NO_EXISTE")
        compatibles = tipos.get(columna, ())
        tipo_ok = tipo != "NO_EXISTE" and (not compatibles or tipo in compatibles)
        validacion.append(
            {
                "tabla": tabla,
                "columna": columna,
                "tipo_sqlite": tipo,
                "tipos_compatibles": ", ".join(compatibles) if compatibles else "NO_DEFINIDO",
                "estado": "OK" if tipo_ok else "REVISAR",
            }
        )
        if tipo != "NO_EXISTE" and not tipo_ok:
            alertas.append(
                _alerta(
                    SEVERIDAD_ADVERTENCIA,
                    tabla,
                    "TIPO_INESPERADO",
                    f"{columna}: {tipo}; esperado {compatibles}",
                )
            )
    return validacion, alertas


def _alerta(severidad: str, tabla: str, control: str, detalle: str) -> Dict[str, Any]:
    return {
        "severidad": severidad,
        "tabla": tabla,
        "control": control,
        "detalle": detalle,
    }


def _auditar_clientes(
    conexion: sqlite3.Connection,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    tabla_sql = escapar_identificador("clientes")
    columnas_financieras = [
        "ingresos_mensuales",
        "total_egresos_mensuales",
        "total_activos",
        "total_pasivos",
        "total_patrimonio",
    ]
    resumen = _consultar_uno(
        conexion,
        f"""
        SELECT COUNT(*) AS registros,
               COUNT(DISTINCT numero_id) AS clientes,
               {_cantidad_nulos_sql(['numero_id', 'grupo_edad', 'desc_genero', 'desc_segmento', 'desc_tipo_de_vivienda'] + columnas_financieras)}
        FROM {tabla_sql};
        """,
    )
    duplicados = _duplicados_por_clave(conexion, "clientes", ["numero_id"])
    finanzas = [
        _consultar_uno(
            conexion,
            f"""SELECT '{columna}' AS variable, MIN({escapar_identificador(columna)}) AS minimo,
                       AVG({escapar_identificador(columna)}) AS promedio, MAX({escapar_identificador(columna)}) AS maximo,
                       SUM(CASE WHEN {escapar_identificador(columna)} < 0 THEN 1 ELSE 0 END) AS negativos,
                       SUM(CASE WHEN {escapar_identificador(columna)} = 0 THEN 1 ELSE 0 END) AS ceros
                FROM {tabla_sql};""",
        )
        for columna in columnas_financieras
    ]

    resumen.update({f"duplicados_{k}": v for k, v in duplicados.items()})
    alertas = _alertas_por_umbral(
        "clientes",
        {**resumen, "duplicados": duplicados.get("combinaciones_duplicadas", 0)},
        [
            ("numero_id_nulos", "ID_NULO", SEVERIDAD_ERROR),
            ("duplicados", "ID_DUPLICADO", SEVERIDAD_ADVERTENCIA),
            ("desc_tipo_de_vivienda_nulos", "VIVIENDA_NULA", SEVERIDAD_ADVERTENCIA),
        ],
    )
    alertas.append(_alerta(SEVERIDAD_INFORMACION, "clientes", "RESUMEN", f"{resumen['registros']} registros; {resumen['clientes']} clientes"))
    return resumen, finanzas, alertas


def _auditar_estimador(
    conexion: sqlite3.Connection,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    tabla = escapar_identificador("estimador_ing")
    resumen = _consultar_uno(
        conexion,
        f"""
        SELECT COUNT(*) AS registros, COUNT(DISTINCT numero_id) AS clientes,
               COUNT(DISTINCT producto) AS productos,
               SUM(CASE WHEN numero_id IS NULL THEN 1 ELSE 0 END) AS ids_nulos,
               SUM(CASE WHEN producto IS NULL OR TRIM(producto) = '' THEN 1 ELSE 0 END) AS productos_nulos,
               SUM(CASE WHEN estimador_ingreso IS NULL THEN 1 ELSE 0 END) AS valores_nulos,
               SUM(CASE WHEN estimador_ingreso < 0 THEN 1 ELSE 0 END) AS negativos,
               SUM(CASE WHEN estimador_ingreso = 0 THEN 1 ELSE 0 END) AS ceros,
               MIN(estimador_ingreso) AS minimo, AVG(estimador_ingreso) AS promedio,
               MAX(estimador_ingreso) AS maximo
        FROM {tabla};
        """,
    )
    duplicados = _duplicados_por_clave(conexion, "estimador_ing", ["numero_id", "producto"])
    productos = _consultar_varios(
        conexion,
        f"""SELECT COALESCE(producto, 'NA') AS producto, COUNT(*) AS registros,
                    COUNT(DISTINCT numero_id) AS clientes,
                    MIN(estimador_ingreso) AS minimo, AVG(estimador_ingreso) AS promedio,
                    MAX(estimador_ingreso) AS maximo
             FROM {tabla} GROUP BY producto ORDER BY registros DESC;""",
    )
    resumen.update({f"duplicados_{k}": v for k, v in duplicados.items()})
    alertas = _alertas_por_umbral(
        "estimador_ing",
        {
            "ids_nulos": resumen["ids_nulos"],
            "duplicados": duplicados.get("combinaciones_duplicadas", 0),
            "negativos": resumen["negativos"],
        },
        [
            ("ids_nulos", "ID_NULO", SEVERIDAD_ERROR),
            ("duplicados", "DUPLICADO_GRANULARIDAD", SEVERIDAD_ADVERTENCIA),
            ("negativos", "ESTIMADOR_NEGATIVO", SEVERIDAD_ADVERTENCIA),
        ],
    )
    alertas.append(_alerta(SEVERIDAD_INFORMACION, "estimador_ing", "RESUMEN", f"{resumen['registros']} registros; {resumen['clientes']} clientes"))
    return resumen, productos, alertas


def _productos_catalogados_normalizados() -> set:
    return {normalizar_producto(nombre) for nombre in CATALOGO_PRODUCTOS}


def _auditar_historica(
    conexion: sqlite3.Connection,
    tabla_nombre: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    tabla = escapar_identificador(tabla_nombre)
    resumen = _consultar_uno(
        conexion,
        f"""
        SELECT COUNT(*) AS registros, COUNT(DISTINCT numero_id) AS clientes,
               COUNT(DISTINCT producto) AS productos, COUNT(DISTINCT fecha) AS fechas,
               MIN(fecha) AS fecha_minima, MAX(fecha) AS fecha_maxima,
               SUM(CASE WHEN fecha IS NULL OR TRIM(fecha) = '' THEN 1 ELSE 0 END) AS fechas_nulas,
               SUM(CASE WHEN fecha IS NOT NULL AND TRIM(fecha) <> '' AND date(fecha) IS NULL THEN 1 ELSE 0 END) AS fechas_invalidas,
               SUM(CASE WHEN numero_id IS NULL THEN 1 ELSE 0 END) AS ids_nulos,
               SUM(CASE WHEN producto IS NULL OR TRIM(producto) = '' THEN 1 ELSE 0 END) AS productos_nulos,
               SUM(CASE WHEN saldo IS NULL THEN 1 ELSE 0 END) AS saldos_nulos,
               SUM(CASE WHEN saldo < 0 THEN 1 ELSE 0 END) AS saldos_negativos,
               SUM(CASE WHEN saldo = 0 THEN 1 ELSE 0 END) AS saldos_cero,
               SUM(CASE WHEN saldo > 0 THEN 1 ELSE 0 END) AS saldos_positivos,
               MIN(saldo) AS saldo_minimo, AVG(saldo) AS saldo_promedio, MAX(saldo) AS saldo_maximo
        FROM {tabla};
        """,
    )
    duplicados = _duplicados_por_clave(conexion, tabla_nombre, ["fecha", "numero_id", "producto"], incluir_saldo=True)
    productos = _consultar_varios(
        conexion,
        f"""
        SELECT COALESCE(producto, 'NA') AS producto, COUNT(*) AS registros,
               COUNT(DISTINCT numero_id) AS clientes, COUNT(DISTINCT fecha) AS fechas,
               MIN(fecha) AS fecha_minima, MAX(fecha) AS fecha_maxima,
               SUM(CASE WHEN saldo < 0 THEN 1 ELSE 0 END) AS negativos,
               SUM(CASE WHEN saldo = 0 THEN 1 ELSE 0 END) AS ceros,
               SUM(CASE WHEN saldo > 0 THEN 1 ELSE 0 END) AS positivos,
               MIN(saldo) AS saldo_minimo, AVG(saldo) AS saldo_promedio, MAX(saldo) AS saldo_maximo
        FROM {tabla} GROUP BY producto ORDER BY registros DESC;
        """,
    )
    cobertura_mensual = _consultar_varios(
        conexion,
        f"""
        SELECT substr(fecha, 1, 7) AS mes, COUNT(DISTINCT fecha) AS fechas_distintas,
               COUNT(*) AS registros, COUNT(DISTINCT numero_id) AS clientes
        FROM {tabla} WHERE date(fecha) IS NOT NULL
        GROUP BY substr(fecha, 1, 7) ORDER BY mes;
        """,
    )
    primeras_apariciones = _consultar_varios(
        conexion,
        f"""
        SELECT producto, primera_fecha, COUNT(*) AS clientes
        FROM (SELECT numero_id, producto, MIN(fecha) AS primera_fecha
              FROM {tabla} WHERE numero_id IS NOT NULL AND producto IS NOT NULL
              AND date(fecha) IS NOT NULL GROUP BY numero_id, producto)
        GROUP BY producto, primera_fecha ORDER BY producto, primera_fecha;
        """,
    )
    resumen.update({f"duplicados_{k}": v for k, v in duplicados.items()})
    alertas = _alertas_por_umbral(
        tabla_nombre,
        resumen,
        [
            ("ids_nulos", "ID_NULO", SEVERIDAD_ERROR),
            ("fechas_invalidas", "FECHA_INVALIDA", SEVERIDAD_ERROR),
            ("productos_nulos", "PRODUCTO_NULO", SEVERIDAD_ADVERTENCIA),
            ("saldos_nulos", "SALDO_NULO", SEVERIDAD_ADVERTENCIA),
            ("saldos_negativos", "SALDO_NEGATIVO", SEVERIDAD_ADVERTENCIA),
            ("saldos_cero", "SALDO_CERO", SEVERIDAD_ADVERTENCIA),
        ],
    )
    if duplicados.get("combinaciones_duplicadas", 0):
        alertas.append(_alerta(SEVERIDAD_ADVERTENCIA, tabla_nombre, "DUPLICADO_GRANULARIDAD", str(duplicados)))

    catalogados = _productos_catalogados_normalizados()
    desconocidos = []
    for producto in productos:
        valor = str(producto["producto"])
        if valor != "NA" and normalizar_producto(valor) not in catalogados:
            desconocidos.append(valor)
    if desconocidos:
        alertas.append(_alerta(SEVERIDAD_ADVERTENCIA, tabla_nombre, "PRODUCTO_DESCONOCIDO", ", ".join(desconocidos)))
    alertas.append(_alerta(SEVERIDAD_INFORMACION, tabla_nombre, "RESUMEN", f"{resumen['registros']} registros; {resumen['clientes']} clientes"))
    return resumen, productos, cobertura_mensual, primeras_apariciones, alertas


def _calcular_cobertura_maestra(
    ruta_clientes: Path,
    ruta_fuente: Path,
    tabla_fuente: str,
) -> Dict[str, Any]:
    conexion = conectar_solo_lectura(ruta_clientes)
    try:
        conexion.execute("ATTACH DATABASE ? AS fuente", (ruta_fuente.resolve().as_uri() + "?mode=ro",))
        tabla = escapar_identificador(tabla_fuente)
        resultado = _consultar_uno(
            conexion,
            f"""
            WITH maestra AS (SELECT DISTINCT numero_id FROM main.clientes WHERE numero_id IS NOT NULL),
                 origen AS (SELECT DISTINCT numero_id FROM fuente.{tabla} WHERE numero_id IS NOT NULL),
                 coincidencias AS (SELECT COUNT(*) AS n FROM origen o INNER JOIN maestra m USING(numero_id)),
                 fuera AS (SELECT COUNT(*) AS n FROM origen o LEFT JOIN maestra m USING(numero_id) WHERE m.numero_id IS NULL)
            SELECT '{tabla_fuente}' AS tabla,
                   (SELECT COUNT(*) FROM origen) AS clientes_fuente,
                   (SELECT COUNT(*) FROM maestra) AS clientes_maestra,
                   (SELECT n FROM coincidencias) AS clientes_coincidentes,
                   (SELECT n FROM fuera) AS clientes_fuera_maestra;
            """,
        )
        maestra = resultado["clientes_maestra"]
        fuente = resultado["clientes_fuente"]
        resultado["clientes_maestra_sin_fuente"] = maestra - resultado["clientes_coincidentes"]
        resultado["porcentaje_maestra_con_fuente"] = round(100 * resultado["clientes_coincidentes"] / maestra, 2) if maestra else 0.0
        resultado["porcentaje_fuente_en_maestra"] = round(100 * resultado["clientes_coincidentes"] / fuente, 2) if fuente else 0.0
        return resultado
    finally:
        conexion.close()


def _comparar_referencia(resumenes: Mapping[str, Mapping[str, Any]]) -> List[Dict[str, Any]]:
    filas = []
    for tabla, esperado in REFERENCIA_AUDITORIA.items():
        actual = resumenes.get(tabla, {})
        for metrica in ("registros", "clientes"):
            valor_actual = actual.get(metrica)
            valor_esperado = esperado[metrica]
            diferencia = None if valor_actual is None else valor_actual - valor_esperado
            filas.append(
                {
                    "tabla": tabla,
                    "metrica": metrica,
                    "referencia_legacy": valor_esperado,
                    "recalculado": valor_actual if valor_actual is not None else "NA",
                    "diferencia": diferencia if diferencia is not None else "NA",
                    "estado": "COINCIDE" if diferencia == 0 else "DIFIERE",
                }
            )
    return filas


def _formatear_seccion_fuente(
    tabla: str,
    esquema: Sequence[Mapping[str, Any]],
    validacion_tipos: Sequence[Mapping[str, Any]],
    resumen: Mapping[str, Any],
    detalle: Sequence[Mapping[str, Any]],
    cobertura_mensual: Optional[Sequence[Mapping[str, Any]]] = None,
    primeras_apariciones: Optional[Sequence[Mapping[str, Any]]] = None,
) -> str:
    partes = [f"### Tabla `{tabla}`", "", "#### Esquema", "", tabla_markdown(esquema, ("columna", "tipo_sqlite", "not_null", "llave_primaria")), "", "#### Compatibilidad de tipos", "", tabla_markdown(validacion_tipos, ("tabla", "columna", "tipo_sqlite", "tipos_compatibles", "estado")), "", "#### Resumen", "", tabla_markdown([resumen], tuple(resumen.keys())), "", "#### Productos o variables financieras", ""]
    if detalle:
        partes.append(tabla_markdown(detalle, tuple(detalle[0].keys())))
    else:
        partes.append("_Sin resultados._")
    if cobertura_mensual is not None:
        partes.extend(["", "#### Cobertura temporal mensual", "", tabla_markdown(cobertura_mensual, ("mes", "fechas_distintas", "registros", "clientes"))])
    if primeras_apariciones is not None:
        partes.extend(["", "#### Primeras apariciones observadas por producto y fecha", "", "Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.", ""])
        if primeras_apariciones:
            partes.append(tabla_markdown(primeras_apariciones, ("producto", "primera_fecha", "clientes")))
        else:
            partes.append("_Sin resultados._")
    return "\n".join(partes)


def _generar_reporte(
    ruta_reporte: Path,
    fecha: str,
    duracion: float,
    secciones_fuentes: Sequence[str],
    coberturas: Sequence[Mapping[str, Any]],
    alertas: Sequence[Mapping[str, Any]],
    comparacion: Sequence[Mapping[str, Any]],
) -> None:
    conteo = Counter(str(item["severidad"]) for item in alertas)
    contenido = [
        f"Fecha de ejecución: `{fecha}`",
        f"Duración aproximada: `{duracion:.2f}` segundos.",
        "",
        "Las bases se abrieron mediante URI SQLite con `mode=ro` y `PRAGMA query_only = ON`.",
        "No se corrigieron datos ni se interpretó la ausencia de registros como saldo cero.",
        "",
        "### Resumen de alertas",
        "",
        tabla_markdown(
            [{"severidad": nivel, "cantidad": conteo.get(nivel, 0)} for nivel in (SEVERIDAD_ERROR, SEVERIDAD_ADVERTENCIA, SEVERIDAD_INFORMACION)],
            ("severidad", "cantidad"),
        ),
        "",
        "### Alertas detalladas",
        "",
        tabla_markdown(alertas, ("severidad", "tabla", "control", "detalle")),
        "",
        "### Auditoría por fuente",
        "",
        "\n\n".join(secciones_fuentes),
        "",
        "### Cobertura frente a la maestra de clientes",
        "",
        tabla_markdown(coberturas, ("tabla", "clientes_fuente", "clientes_maestra", "clientes_coincidentes", "clientes_fuera_maestra", "clientes_maestra_sin_fuente", "porcentaje_maestra_con_fuente", "porcentaje_fuente_en_maestra")),
        "",
        "### Comparación con la auditoría exploratoria inicial",
        "",
        "La referencia corresponde a `legacy/auditoria_crean.md`. Los valores se recalculan desde las bases actuales.",
        "",
        tabla_markdown(comparacion, ("tabla", "metrica", "referencia_legacy", "recalculado", "diferencia", "estado")),
        "",
        "### Interpretación y asuntos pendientes",
        "",
        "- Las primeras apariciones son evidencia descriptiva, no aperturas confirmadas.",
        "- Los saldos negativos se reportan sin corregir. En cuenta corriente pueden representar sobregiros.",
        "- Los saldos cero se distinguen de la ausencia de registros.",
        "- La resolución de duplicados y la agregación mensual pertenecen a la Etapa 2.",
        "- Cualquier diferencia frente a la auditoría inicial debe revisarse contra la versión exacta de las bases.",
    ]
    actualizar_seccion(
        ruta_reporte=ruta_reporte,
        id_seccion="AUDITORIA_REPRODUCIBLE",
        titulo="Auditoría reproducible de fuentes (Etapa 1)",
        contenido="\n".join(contenido),
    )


def ejecutar_auditoria(configuracion: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta la auditoría completa y actualiza el reporte consolidado."""
    inicio = time.perf_counter()
    raw_path = Path(configuracion["data"]["raw_path"])
    ruta_reporte = Path(configuracion.get("reporting", {}).get("validation_report", "docs/reporte_validacion.md"))
    rutas = {fuente.tabla_esperada: raw_path / fuente.archivo for fuente in CATALOGO_FUENTES}

    faltantes = [str(ruta) for ruta in rutas.values() if not ruta.is_file()]
    if faltantes:
        raise AuditoriaError("Faltan fuentes requeridas: " + ", ".join(faltantes))

    resumenes: Dict[str, Dict[str, Any]] = {}
    secciones: List[str] = []
    alertas: List[Dict[str, Any]] = []

    for fuente in CATALOGO_FUENTES:
        tabla = fuente.tabla_esperada
        conexion = conectar_solo_lectura(rutas[tabla])
        try:
            tablas = {fila["name"] for fila in _consultar_varios(conexion, "SELECT name FROM sqlite_master WHERE type='table';")}
            if tabla not in tablas:
                raise AuditoriaError(f"La tabla esperada '{tabla}' no existe en {rutas[tabla]}")
            esquema = _esquema(conexion, tabla)
            validacion_tipos, alertas_esquema = _validar_esquema(tabla, esquema, fuente.columnas_obligatorias)
            alertas.extend(alertas_esquema)
            faltan_columnas = [fila for fila in validacion_tipos if fila["tipo_sqlite"] == "NO_EXISTE"]
            if faltan_columnas:
                columnas = ", ".join(str(fila["columna"]) for fila in faltan_columnas)
                raise AuditoriaError(f"No se puede auditar '{tabla}'; faltan columnas: {columnas}")

            if tabla == "clientes":
                resumen, detalle, nuevas_alertas = _auditar_clientes(conexion)
                seccion = _formatear_seccion_fuente(tabla, esquema, validacion_tipos, resumen, detalle)
            elif tabla == "estimador_ing":
                resumen, detalle, nuevas_alertas = _auditar_estimador(conexion)
                seccion = _formatear_seccion_fuente(tabla, esquema, validacion_tipos, resumen, detalle)
            else:
                resumen, detalle, mensual, primeras, nuevas_alertas = _auditar_historica(conexion, tabla)
                seccion = _formatear_seccion_fuente(tabla, esquema, validacion_tipos, resumen, detalle, mensual, primeras)
            resumenes[tabla] = resumen
            alertas.extend(nuevas_alertas)
            secciones.append(seccion)
            logger.info("Auditada fuente %s", tabla)
        finally:
            conexion.close()

    ruta_clientes = rutas["clientes"]
    coberturas = []
    for fuente in CATALOGO_FUENTES:
        if fuente.tabla_esperada == "clientes":
            continue
        cobertura = _calcular_cobertura_maestra(ruta_clientes, rutas[fuente.tabla_esperada], fuente.tabla_esperada)
        coberturas.append(cobertura)
        if cobertura["clientes_fuera_maestra"]:
            alertas.append(_alerta(SEVERIDAD_ERROR, fuente.tabla_esperada, "ID_FUERA_MAESTRA", str(cobertura["clientes_fuera_maestra"])))
        else:
            alertas.append(_alerta(SEVERIDAD_INFORMACION, fuente.tabla_esperada, "COBERTURA_MAESTRA", f"{cobertura['porcentaje_maestra_con_fuente']}%"))

    comparacion = _comparar_referencia(resumenes)
    for fila in comparacion:
        if fila["estado"] == "DIFIERE":
            alertas.append(_alerta(SEVERIDAD_ADVERTENCIA, str(fila["tabla"]), "DIFERENCIA_LEGACY", f"{fila['metrica']}: {fila['diferencia']}"))

    duracion = time.perf_counter() - inicio
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _generar_reporte(ruta_reporte, fecha, duracion, secciones, coberturas, alertas, comparacion)
    conteo = Counter(str(item["severidad"]) for item in alertas)
    return {
        "duracion_segundos": duracion,
        "tablas_auditadas": len(resumenes),
        "alertas_por_severidad": dict(conteo),
        "ruta_reporte": str(ruta_reporte),
    }
