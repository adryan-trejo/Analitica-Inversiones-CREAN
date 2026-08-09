# Reporte de validación CREAN

<!-- INICIO:CAPA_MENSUAL_PROXY -->
## Capa mensual y validación del proxy (Etapa 2)

`dim_cliente`: 860223 clientes (deduplicados).
`fact_saldos_mensuales`: 3825587 filas; granularidad `numero_id + mes + producto_original`.

### Clientes y filas por producto en `fact_saldos_mensuales`

| producto_original | clientes | filas_mensuales |
| --- | --- | --- |
| CUENTA DE AHORRO | 474248 | 987800 |
| BOLSILLOS | 260714 | 997547 |
| FIDUCUENTA | 181021 | 999806 |
| INVERSIÓN VIRTUAL | 61215 | 497533 |
| CDT | 26273 | 287836 |
| CUENTA DE CORRIENTE | 5645 | 12086 |
| INVESBOT | 5214 | 42979 |

### Primeras apariciones por producto y mes (proxy y sensibilidad)

Un `salto_cobertura` indica que ese mes todavía concentra una proporción relevante (> 15 % del primer mes) de clientes nuevos, y por tanto no se interpreta como adopción orgánica.

| producto_original | mes_primera | clientes_nuevos | proporcion_primer_mes | salto_cobertura |
| --- | --- | --- | --- | --- |
| BOLSILLOS | 2025-06 | 68505 | 1.0 | False |
| BOLSILLOS | 2025-07 | 58431 | 0.853 | True |
| BOLSILLOS | 2025-08 | 32268 | 0.471 | True |
| BOLSILLOS | 2025-09 | 20236 | 0.295 | True |
| BOLSILLOS | 2025-10 | 9765 | 0.143 | False |
| BOLSILLOS | 2025-11 | 6601 | 0.096 | False |
| BOLSILLOS | 2025-12 | 5438 | 0.079 | False |
| BOLSILLOS | 2026-01 | 8828 | 0.129 | False |
| BOLSILLOS | 2026-02 | 19988 | 0.292 | False |
| BOLSILLOS | 2026-03 | 4909 | 0.072 | False |
| BOLSILLOS | 2026-04 | 15876 | 0.232 | False |
| BOLSILLOS | 2026-05 | 7016 | 0.102 | False |
| BOLSILLOS | 2026-06 | 2853 | 0.042 | False |
| CDT | 2025-06 | 21363 | 1.0 | False |
| CDT | 2025-07 | 521 | 0.024 | False |
| CDT | 2025-08 | 477 | 0.022 | False |
| CDT | 2025-09 | 379 | 0.018 | False |
| CDT | 2025-10 | 386 | 0.018 | False |
| CDT | 2025-11 | 294 | 0.014 | False |
| CDT | 2025-12 | 410 | 0.019 | False |
| CDT | 2026-01 | 439 | 0.021 | False |
| CDT | 2026-02 | 464 | 0.022 | False |
| CDT | 2026-03 | 521 | 0.024 | False |
| CDT | 2026-04 | 413 | 0.019 | False |
| CDT | 2026-05 | 307 | 0.014 | False |
| CDT | 2026-06 | 299 | 0.014 | False |
| CUENTA DE AHORRO | 2025-06 | 72624 | 1.0 | False |
| CUENTA DE AHORRO | 2025-07 | 72589 | 1.0 | True |
| CUENTA DE AHORRO | 2025-08 | 38573 | 0.531 | True |
| CUENTA DE AHORRO | 2025-09 | 69946 | 0.963 | True |
| CUENTA DE AHORRO | 2025-10 | 25969 | 0.358 | True |
| CUENTA DE AHORRO | 2025-11 | 15704 | 0.216 | True |
| CUENTA DE AHORRO | 2025-12 | 61712 | 0.85 | True |
| CUENTA DE AHORRO | 2026-01 | 34187 | 0.471 | True |
| CUENTA DE AHORRO | 2026-02 | 34066 | 0.469 | True |
| CUENTA DE AHORRO | 2026-03 | 11588 | 0.16 | True |
| CUENTA DE AHORRO | 2026-04 | 5647 | 0.078 | False |
| CUENTA DE AHORRO | 2026-05 | 4624 | 0.064 | False |
| CUENTA DE AHORRO | 2026-06 | 27019 | 0.372 | False |
| CUENTA DE CORRIENTE | 2025-06 | 964 | 1.0 | False |
| CUENTA DE CORRIENTE | 2025-07 | 955 | 0.991 | True |
| CUENTA DE CORRIENTE | 2025-08 | 271 | 0.281 | True |
| CUENTA DE CORRIENTE | 2025-09 | 885 | 0.918 | True |
| CUENTA DE CORRIENTE | 2025-10 | 138 | 0.143 | False |
| CUENTA DE CORRIENTE | 2025-11 | 413 | 0.428 | False |
| CUENTA DE CORRIENTE | 2025-12 | 761 | 0.789 | False |
| CUENTA DE CORRIENTE | 2026-01 | 150 | 0.156 | False |
| CUENTA DE CORRIENTE | 2026-02 | 241 | 0.25 | False |
| CUENTA DE CORRIENTE | 2026-03 | 166 | 0.172 | False |
| CUENTA DE CORRIENTE | 2026-04 | 132 | 0.137 | False |
| CUENTA DE CORRIENTE | 2026-05 | 393 | 0.408 | False |
| CUENTA DE CORRIENTE | 2026-06 | 176 | 0.183 | False |
| FIDUCUENTA | 2025-06 | 73962 | 1.0 | False |
| FIDUCUENTA | 2025-07 | 27406 | 0.371 | True |
| FIDUCUENTA | 2025-08 | 45123 | 0.61 | True |
| FIDUCUENTA | 2025-09 | 13229 | 0.179 | True |
| FIDUCUENTA | 2025-10 | 5415 | 0.073 | False |
| FIDUCUENTA | 2025-11 | 3931 | 0.053 | False |
| FIDUCUENTA | 2025-12 | 1758 | 0.024 | False |
| FIDUCUENTA | 2026-01 | 1418 | 0.019 | False |
| FIDUCUENTA | 2026-02 | 2614 | 0.035 | False |
| FIDUCUENTA | 2026-03 | 1491 | 0.02 | False |
| FIDUCUENTA | 2026-04 | 1235 | 0.017 | False |
| FIDUCUENTA | 2026-05 | 2045 | 0.028 | False |
| FIDUCUENTA | 2026-06 | 1394 | 0.019 | False |
| INVERSIÓN VIRTUAL | 2025-06 | 37084 | 1.0 | False |
| INVERSIÓN VIRTUAL | 2025-07 | 2831 | 0.076 | False |
| INVERSIÓN VIRTUAL | 2025-08 | 2365 | 0.064 | False |
| INVERSIÓN VIRTUAL | 2025-09 | 1848 | 0.05 | False |
| INVERSIÓN VIRTUAL | 2025-10 | 1795 | 0.048 | False |
| INVERSIÓN VIRTUAL | 2025-11 | 1464 | 0.039 | False |
| INVERSIÓN VIRTUAL | 2025-12 | 2236 | 0.06 | False |
| INVERSIÓN VIRTUAL | 2026-01 | 2312 | 0.062 | False |
| INVERSIÓN VIRTUAL | 2026-02 | 1898 | 0.051 | False |
| INVERSIÓN VIRTUAL | 2026-03 | 2284 | 0.062 | False |
| INVERSIÓN VIRTUAL | 2026-04 | 1992 | 0.054 | False |
| INVERSIÓN VIRTUAL | 2026-05 | 1633 | 0.044 | False |
| INVERSIÓN VIRTUAL | 2026-06 | 1473 | 0.04 | False |
| INVESBOT | 2025-06 | 2031 | 1.0 | False |
| INVESBOT | 2025-07 | 297 | 0.146 | False |
| INVESBOT | 2025-08 | 128 | 0.063 | False |
| INVESBOT | 2025-09 | 190 | 0.094 | False |
| INVESBOT | 2025-10 | 146 | 0.072 | False |
| INVESBOT | 2025-11 | 290 | 0.143 | False |
| INVESBOT | 2025-12 | 282 | 0.139 | False |
| INVESBOT | 2026-01 | 490 | 0.241 | False |
| INVESBOT | 2026-02 | 298 | 0.147 | False |
| INVESBOT | 2026-03 | 402 | 0.198 | False |
| INVESBOT | 2026-04 | 241 | 0.119 | False |
| INVESBOT | 2026-05 | 239 | 0.118 | False |
| INVESBOT | 2026-06 | 180 | 0.089 | False |

### Meses excluidos del proxy por salto de cobertura

| producto_original | mes_primera | clientes_nuevos | proporcion_primer_mes |
| --- | --- | --- | --- |
| BOLSILLOS | 2025-07 | 58431 | 0.853 |
| BOLSILLOS | 2025-08 | 32268 | 0.471 |
| BOLSILLOS | 2025-09 | 20236 | 0.295 |
| CUENTA DE AHORRO | 2025-07 | 72589 | 1.0 |
| CUENTA DE AHORRO | 2025-08 | 38573 | 0.531 |
| CUENTA DE AHORRO | 2025-09 | 69946 | 0.963 |
| CUENTA DE AHORRO | 2025-10 | 25969 | 0.358 |
| CUENTA DE AHORRO | 2025-11 | 15704 | 0.216 |
| CUENTA DE AHORRO | 2025-12 | 61712 | 0.85 |
| CUENTA DE AHORRO | 2026-01 | 34187 | 0.471 |
| CUENTA DE AHORRO | 2026-02 | 34066 | 0.469 |
| CUENTA DE AHORRO | 2026-03 | 11588 | 0.16 |
| CUENTA DE CORRIENTE | 2025-07 | 955 | 0.991 |
| CUENTA DE CORRIENTE | 2025-08 | 271 | 0.281 |
| CUENTA DE CORRIENTE | 2025-09 | 885 | 0.918 |
| FIDUCUENTA | 2025-07 | 27406 | 0.371 |
| FIDUCUENTA | 2025-08 | 45123 | 0.61 |
| FIDUCUENTA | 2025-09 | 13229 | 0.179 |
<!-- FIN:CAPA_MENSUAL_PROXY -->


<!-- INICIO:DATASET_MODELADO_EDA -->
## Dataset de modelado y EDA dirigido (Etapa 3)

`dataset_modelado`: 3330642 filas; granularidad `numero_id + fecha_corte`.
Target: adopción digital (Invesbot, Fiducuenta, Inversión Virtual) dentro de 90 días posteriores al corte, excluyendo ventanas de carga inicial (ver `docs/decisiones_analiticas.md`).

### Clientes elegibles y tasa de adopción por fecha de corte

| fecha_corte | clientes_elegibles | adoptantes | tasa_adopcion |
| --- | --- | --- | --- |
| 2025-12-01 | 838692 | 11930 | 0.0142 |
| 2026-01-01 | 835037 | 11840 | 0.0142 |
| 2026-02-01 | 830151 | 10709 | 0.0129 |
| 2026-03-01 | 826762 | 8945 | 0.0108 |

### Auditoría de fecha máxima de variables usada (muestra)

Todas las filas deben cumplir `fecha_maxima_variable_usada < fecha_corte` (no se usa el mes del corte).

| numero_id | fecha_corte | fecha_maxima_variable_usada |
| --- | --- | --- |
| -1787255175305344189 | 2026-03-01 | 2025-10-01 |
| -4927767430203239166 | 2026-03-01 | 2025-11-01 |
| 5543607971104233604 | 2026-02-01 | 2025-12-01 |
| 5010344169842200821 | 2025-12-01 | 2025-07-01 |
| -8319797695061243498 | 2026-01-01 | 2025-10-01 |
| 674509557937937142 | 2025-12-01 | 2025-11-01 |
| -4325808713618203489 | 2026-03-01 | 2026-01-01 |
| 6287443539865821365 | 2025-12-01 | 2025-11-01 |
| 7819614621027585908 | 2026-01-01 | 2025-12-01 |
| 6811487604538625336 | 2026-01-01 | 2025-12-01 |

### EDA dirigido (6 visualizaciones)

![EDA Etapa 3](docs/eda_etapa3.png)

1. Composición del target: proporción de adoptantes frente a no adoptantes, fuertemente desbalanceada.
2. Tasa de adopción por cohorte: estabilidad de la tasa entre las cuatro fechas de corte.
3. Adopción por segmento: diferencias de tasa entre segmentos comerciales (`desc_segmento`).
4. Liquidez (saldo total observado) comparada entre adoptantes y no adoptantes.
5. Flujo libre (ingresos menos egresos) comparado entre adoptantes y no adoptantes.
6. Tasa de adopción según experiencia previa de inversión (Invesbot/Fiducuenta/Inversión Virtual/CDT).

Limitación: las variables de liquidez y flujo libre pueden tener valores extremos (ver banderas de calidad en el dataset); las visualizaciones excluyen atípicos solo para la escala del gráfico, no para el dataset persistido.
<!-- FIN:DATASET_MODELADO_EDA -->




<!-- INICIO:MODELO_ADOPCION -->
## Modelo de adopción digital (Etapa 4)

Separación temporal: entrenamiento en cortes ['2025-12-01', '2026-01-01'], prueba en cortes ['2026-02-01', '2026-03-01'].
**Modelo seleccionado: catboost** (mejor PR-AUC en prueba temporal, ver tabla).

### Comparación de modelos y baselines (conjunto de prueba temporal)

| modelo | pr_auc | roc_auc | brier | precision_top10 | recall_top10 | lift_top10 |
| --- | --- | --- | --- | --- | --- | --- |
| regresion_logistica | 0.0335 | 0.791 | 0.2246 | 0.0394 | 0.3326 | 3.3255 |
| catboost | 0.0964 | 0.8482 | 0.0112 | 0.0621 | 0.5238 | 5.2376 |
| baseline_prevalencia | 0.0119 | 0.5 | 0.0117 | 0.0037 | 0.0308 | 0.3083 |
| regla_simple_experiencia_previa | 0.0177 | 0.6188 | 0.2188 | 0.0203 | 0.1708 | 1.7081 |

### Estabilidad temporal básica (PR-AUC del modelo seleccionado por corte de prueba)

| fecha_corte | pr_auc | tasa_adopcion |
| --- | --- | --- |
| 2026-02-01 | 0.1193 | 0.0129 |
| 2026-03-01 | 0.0734 | 0.0108 |

### Tasa observada por decil (catboost, prueba)

| decil | clientes | tasa_adopcion |
| --- | --- | --- |
| 10 | 165692 | 0.0621 |
| 9 | 165691 | 0.0241 |
| 8 | 165691 | 0.0136 |
| 7 | 165691 | 0.0074 |
| 6 | 165691 | 0.004 |
| 5 | 165692 | 0.0026 |
| 4 | 165691 | 0.0019 |
| 3 | 165691 | 0.0014 |
| 2 | 165691 | 0.0009 |
| 1 | 165692 | 0.0006 |

### Composición del target de prueba por producto de adopción

| producto_adopcion | adoptantes |
| --- | --- |
| INVERSIÓN VIRTUAL | 11164 |
| FIDUCUENTA | 7004 |
| INVESBOT | 1486 |

### Explicabilidad

Top 10 coeficientes del baseline (regresión logística, variables estandarizadas):

| variable | coeficiente |
| --- | --- |
| desc_segmento_personal | -0.7932 |
| ingresos_mensuales | -0.716 |
| desc_genero_trans | -0.6906 |
| desc_segmento_preferencial | 0.5395 |
| grupo_edad_65+ | -0.4898 |
| desc_genero_SIN_INFORMACION | 0.4423 |
| meses_observados | 0.4304 |
| grupo_edad_18-25 | 0.393 |
| cantidad_productos | 0.3452 |
| desc_genero_femenino | 0.3216 |

Top 10 importancia global de CatBoost:

| variable | importancia |
| --- | --- |
| flujo_libre | 14.68 |
| cantidad_productos | 8.89 |
| ingresos_mensuales | 8.15 |
| grupo_edad | 7.67 |
| tenencia_bolsillos | 6.86 |
| saldo_promedio_3m | 5.37 |
| proporcion_meses_positivos | 4.17 |
| experiencia_previa_inversion | 4.03 |
| saldo_promedio_6m | 3.99 |
| tendencia_saldo_simple | 3.89 |

Top 5 variables por SHAP medio absoluto (muestra reproducible de 2000 filas de prueba):

| variable | shap_medio_abs |
| --- | --- |
| flujo_libre | 0.25 |
| saldo_promedio_6m | 0.2 |
| tenencia_bolsillos | 0.2 |
| saldo_promedio_3m | 0.17 |
| ingresos_mensuales | 0.16 |

Limitaciones: el desbalance es fuerte (prevalencia ~1-1.4 %); las métricas de precisión/recall en el top 10 % son más informativas que el ROC-AUC. El modelo debe recalibrarse con adopción real de la App una vez esté disponible.
<!-- FIN:MODELO_ADOPCION -->










<!-- INICIO:SALDO_SCORING_ESCENARIOS -->
## Saldo potencial, scoring y escenarios (Etapa 5)

Scoring generado para el corte 2026-03-01 (último corte disponible en `dataset_modelado`).
Saldo potencial: mediana del saldo observado entre 30 y 90 días después de la adopción real.

### Qué mide cada columna de `outputs/scoring_clientes.parquet`

- `probabilidad_adopcion`: salida del modelo CatBoost de Etapa 4 (probabilidad de adoptar dentro del horizonte de 90 días desde el corte).
- `saldo_potencial_condicional`: mediana histórica de saldo 30-90 días post-adopción, asignada por segmento comercial (marginal sobre producto, ver más abajo). No depende de la probabilidad.
- `saldo_esperado_ajustado` = `probabilidad_adopcion` × `saldo_potencial_condicional`: valor esperado agregable, usado para los escenarios y el ranking de valor (`decil_valor`).
- `decil_adopcion` (1-10, 10 = más alto): ranking por `probabilidad_adopcion`.
- `decil_valor` (1-10, 10 = más alto): ranking por `saldo_esperado_ajustado`.
- `segmento_oportunidad`: cruce de `probabilidad_adopcion` y `saldo_potencial_condicional` (no `saldo_esperado_ajustado`, para no correlacionar ambos ejes) contra sus medianas; el umbral de valor se calcula sobre los valores únicos observados, no ponderado por frecuencia, para que el segmento comercial mayoritario (`personal`, ~76 % de los clientes) no domine el corte.
- `nivel_confianza`: ALTA si hay ≥6 meses observados y ninguna variable financiera faltante; BAJA si faltan ≥2 variables financieras o no hay historia observada; MEDIA en el resto.
- `razones_principales`: top-3 variables por importancia global del modelo (mismas para todos los clientes; no se calcula SHAP individual para toda la población).

### Comparación de métodos de saldo potencial (separación temporal, MAE)

| metodo | mae | clientes_evaluados |
| --- | --- | --- |
| mediana_por_segmento_producto | 15008538.71 | 7689 |
| mediana_por_producto | 15265759.09 | 7689 |
| mediana_global | 16623095.49 | 7689 |

Método con menor error: **mediana_por_segmento_producto**. Para el scoring (clientes que aún no adoptan) se usa la mediana histórica por segmento (marginal sobre producto, con respaldo en la mediana global), porque el producto que elegirían es desconocido antes de adoptar.

### Segmentos de oportunidad (scoring)

| segmento_oportunidad | clientes | probabilidad_promedio | saldo_esperado_promedio |
| --- | --- | --- | --- |
| Alta probabilidad y alto valor | 179983 | 0.04 | 244753.55 |
| Alta probabilidad y valor moderado | 233398 | 0.02 | 54741.91 |
| Baja prioridad | 398541 | 0.0 | 5890.82 |
| Probabilidad moderada y alto valor | 14840 | 0.0 | 21748.74 |

### Escenarios de oportunidad total (factores explícitos, no observaciones reales)

| segmento_oportunidad | oportunidad_conservadora | oportunidad_base | oportunidad_expansiva |
| --- | --- | --- | --- |
| Alta probabilidad y alto valor | 30836034673.26 | 44051478104.66 | 57266921536.06 |
| Alta probabilidad y valor moderado | 8943655912.56 | 12776651303.66 | 16609646694.76 |
| Baja prioridad | 1643414465.71 | 2347734951.01 | 3052055436.31 |
| Probabilidad moderada y alto valor | 225925878.74 | 322751255.35 | 419576631.96 |

Variables más asociadas con la adopción (modelo seleccionado en Etapa 4): flujo_libre, cantidad_productos, ingresos_mensuales.

Limitaciones: el saldo potencial es una mediana histórica, no una predicción individual precisa; los escenarios aplican factores explícitos (0.7 / 1.0 / 1.3) sobre el saldo esperado ajustado y no deben interpretarse como observaciones reales ni como captación de dinero nuevo. No se distingue con certeza adquisición, migración o profundización con los datos disponibles.
<!-- FIN:SALDO_SCORING_ESCENARIOS -->






