"""Punto de entrada principal del pipeline analítico CREAN.

Permite ejecutar pasos independientes. En la Etapa 1 están disponibles el
inventario de fuentes y la auditoría reproducible. En la Etapa 2 está disponible
la capa mensual y la validación del proxy de adopción digital.
"""

import argparse
import logging

from src.config import cargar_configuracion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

PASOS_DISPONIBLES = ["inventario", "auditoria", "mensual", "dataset_modelado", "modelo_adopcion", "scoring"]


def construir_parser() -> argparse.ArgumentParser:
    """Construye el parser de línea de comandos del pipeline."""
    parser = argparse.ArgumentParser(description="Pipeline analítico CREAN")
    parser.add_argument(
        "--step",
        choices=PASOS_DISPONIBLES,
        help="Etapa específica a ejecutar. Si se omite, no se ejecuta ningún paso.",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Ruta al archivo de configuración (por defecto: config.yaml).",
    )
    return parser


def main() -> None:
    """Punto de entrada de línea de comandos."""
    parser = construir_parser()
    args = parser.parse_args()

    configuracion = cargar_configuracion(args.config)

    if args.step is None:
        logger.info(
            "No se especificó --step. Pasos disponibles: %s",
            PASOS_DISPONIBLES,
        )
        return

    if args.step == "inventario":
        from src.data.inventario import ejecutar_inventario

        ejecutar_inventario(configuracion)
        logger.info(
            "Inventario ejecutado. Revisa docs/reporte_validacion.md"
        )
        return

    if args.step == "auditoria":
        from src.data.auditoria import ejecutar_auditoria

        resumen = ejecutar_auditoria(configuracion)
        logger.info(
            "Auditoría ejecutada en %.2f segundos. Alertas: %s",
            resumen["duracion_segundos"],
            resumen["alertas_por_severidad"],
        )
        logger.info(
            "Revisa docs/reporte_validacion.md"
        )
        return

    if args.step == "mensual":
        from src.data.mensual import ejecutar_capa_mensual

        resumen = ejecutar_capa_mensual(configuracion)
        logger.info(
            "Capa mensual generada: %s clientes, %s filas en fact_saldos_mensuales.",
            resumen["clientes"],
            resumen["filas_fact"],
        )
        logger.info("Revisa %s", resumen["ruta_reporte"])
        return

    if args.step == "dataset_modelado":
        from src.features.dataset_modelado import ejecutar_dataset_modelado

        resumen = ejecutar_dataset_modelado(configuracion)
        logger.info("Dataset de modelado generado: %s filas.", resumen["filas"])
        logger.info("Revisa %s", resumen["ruta_reporte"])
        return

    if args.step == "modelo_adopcion":
        from src.models.adopcion import ejecutar_modelo_adopcion

        resumen = ejecutar_modelo_adopcion(configuracion)
        logger.info("Modelo seleccionado: %s", resumen["modelo_seleccionado"])
        logger.info("Revisa %s", resumen["ruta_reporte"])
        return

    if args.step == "scoring":
        from src.models.scoring import ejecutar_scoring

        resumen = ejecutar_scoring(configuracion)
        logger.info("Scoring generado: %s clientes. Método de saldo: %s.", resumen["clientes"], resumen["metodo_saldo"])
        logger.info("Revisa %s", resumen["ruta_reporte"])
        return

    raise NotImplementedError(
        f"El paso '{args.step}' aún no está implementado."
    )


if __name__ == "__main__":
    main()