# Reporte de validación CREAN

<!-- INICIO:INVENTARIO_FUENTES -->
## Inventario de fuentes (Etapa 1)

Fecha de ejecución: `2026-08-07 20:27:24`

| archivo | tabla_esperada | existe | tabla_encontrada | tamano_mb | estado_validacion |
| --- | --- | --- | --- | --- | --- |
| clientes.db | clientes | True | True | 49.93 | OK |
| estimador_ing.db | estimador_ing | True | True | 30.28 | OK |
| crean_aho_cte.db | crean_aho_cte | True | True | 50.71 | OK |
| crean_bolsillos.db | crean_bolsillos | True | True | 39.42 | OK |
| crean_fiducuenta.db | crean_fiducuenta | True | True | 45.18 | OK |
| crean_inv_virtual_cdt.db | crean_inv_virtual_cdt | True | True | 44.62 | OK |
| invesbot.db | invesbot | True | True | 43.34 | OK |
<!-- FIN:INVENTARIO_FUENTES -->


<!-- INICIO:AUDITORIA_REPRODUCIBLE -->
## Auditoría reproducible de fuentes (Etapa 1)

Fecha de ejecución: `2026-08-07 20:34:03`
Duración aproximada: `397.58` segundos.

Las bases se abrieron mediante URI SQLite con `mode=ro` y `PRAGMA query_only = ON`.
No se corrigieron datos ni se interpretó la ausencia de registros como saldo cero.

### Resumen de alertas

| severidad | cantidad |
| --- | --- |
| ERROR | 0 |
| ADVERTENCIA | 6 |
| INFORMACION | 13 |

### Alertas detalladas

| severidad | tabla | control | detalle |
| --- | --- | --- | --- |
| ADVERTENCIA | clientes | ID_DUPLICADO | 8 |
| ADVERTENCIA | clientes | VIVIENDA_NULA | 591699 |
| INFORMACION | clientes | RESUMEN | 860231 registros; 860223 clientes |
| INFORMACION | estimador_ing | RESUMEN | 745792 registros; 745792 clientes |
| ADVERTENCIA | crean_aho_cte | SALDO_NEGATIVO | 1470 |
| ADVERTENCIA | crean_aho_cte | SALDO_CERO | 48210 |
| INFORMACION | crean_aho_cte | RESUMEN | 1000000 registros; 475719 clientes |
| ADVERTENCIA | crean_bolsillos | SALDO_CERO | 467155 |
| INFORMACION | crean_bolsillos | RESUMEN | 1000000 registros; 260714 clientes |
| INFORMACION | crean_fiducuenta | RESUMEN | 1000000 registros; 181021 clientes |
| ADVERTENCIA | crean_inv_virtual_cdt | SALDO_CERO | 4017 |
| INFORMACION | crean_inv_virtual_cdt | RESUMEN | 994177 registros; 84104 clientes |
| INFORMACION | invesbot | RESUMEN | 1000000 registros; 5214 clientes |
| INFORMACION | estimador_ing | COBERTURA_MAESTRA | 86.7% |
| INFORMACION | crean_aho_cte | COBERTURA_MAESTRA | 55.3% |
| INFORMACION | crean_bolsillos | COBERTURA_MAESTRA | 30.31% |
| INFORMACION | crean_fiducuenta | COBERTURA_MAESTRA | 21.04% |
| INFORMACION | crean_inv_virtual_cdt | COBERTURA_MAESTRA | 9.78% |
| INFORMACION | invesbot | COBERTURA_MAESTRA | 0.61% |

### Auditoría por fuente

### Tabla `clientes`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| numero_id | INTEGER | 0 | 0 |
| grupo_edad | TEXT | 0 | 0 |
| desc_genero | TEXT | 0 | 0 |
| desc_segmento | TEXT | 0 | 0 |
| desc_tipo_de_vivienda | TEXT | 0 | 0 |
| ingresos_mensuales | REAL | 0 | 0 |
| total_egresos_mensuales | REAL | 0 | 0 |
| total_activos | REAL | 0 | 0 |
| total_pasivos | REAL | 0 | 0 |
| total_patrimonio | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| clientes | numero_id | INTEGER | INTEGER | OK |
| clientes | grupo_edad | TEXT | TEXT | OK |
| clientes | desc_genero | TEXT | TEXT | OK |
| clientes | desc_segmento | TEXT | TEXT | OK |
| clientes | desc_tipo_de_vivienda | TEXT | TEXT | OK |
| clientes | ingresos_mensuales | REAL | REAL, INTEGER, NUMERIC | OK |
| clientes | total_egresos_mensuales | REAL | REAL, INTEGER, NUMERIC | OK |
| clientes | total_activos | REAL | REAL, INTEGER, NUMERIC | OK |
| clientes | total_pasivos | REAL | REAL, INTEGER, NUMERIC | OK |
| clientes | total_patrimonio | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | numero_id_nulos | grupo_edad_nulos | desc_genero_nulos | desc_segmento_nulos | desc_tipo_de_vivienda_nulos | ingresos_mensuales_nulos | total_egresos_mensuales_nulos | total_activos_nulos | total_pasivos_nulos | total_patrimonio_nulos | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 860231 | 860223 | 0 | 0 | 93 | 0 | 591699 | 249 | 249 | 249 | 249 | 260 | 8 | 8 | 2 |

#### Productos o variables financieras

| variable | minimo | promedio | maximo | negativos | ceros |
| --- | --- | --- | --- | --- | --- |
| ingresos_mensuales | 0.0 | 39323048.760206684 | 9000008796700.0 | 0 | 9297 |
| total_egresos_mensuales | 0.0 | 147800881.97737056 | 8500000850000.0 | 0 | 136251 |
| total_activos | 0.0 | 199790079.42897826 | 9041914166666.0 | 0 | 97104 |
| total_pasivos | 0.0 | 96876727.99330467 | 9000012000000.0 | 0 | 644634 |
| total_patrimonio | -8999512000000.0 | 131115604.87826566 | 9041902166666.0 | 6173 | 164336 |

### Tabla `estimador_ing`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| estimador_ingreso | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| estimador_ing | numero_id | INTEGER | INTEGER | OK |
| estimador_ing | producto | TEXT | TEXT | OK |
| estimador_ing | estimador_ingreso | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | ids_nulos | productos_nulos | valores_nulos | negativos | ceros | minimo | promedio | maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 745792 | 745792 | 1 | 0 | 0 | 0 | 0 | 0 | 67058.5 | 3888830.4051613463 | 300000000.0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | minimo | promedio | maximo |
| --- | --- | --- | --- | --- | --- |
| ESTIMADOR INGRESO | 745792 | 745792 | 67058.5 | 3888830.4051613463 | 300000000.0 |

### Tabla `crean_aho_cte`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| fecha | TEXT | 0 | 0 |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| saldo | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| crean_aho_cte | fecha | TEXT | TEXT, DATE, DATETIME | OK |
| crean_aho_cte | numero_id | INTEGER | INTEGER | OK |
| crean_aho_cte | producto | TEXT | TEXT | OK |
| crean_aho_cte | saldo | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | fechas | fecha_minima | fecha_maxima | fechas_nulas | fechas_invalidas | ids_nulos | productos_nulos | saldos_nulos | saldos_negativos | saldos_cero | saldos_positivos | saldo_minimo | saldo_promedio | saldo_maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion | duplicados_claves_con_saldos_distintos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000000 | 475719 | 2 | 91 | 2025-06-01 | 2026-06-07 | 0 | 0 | 0 | 0 | 0 | 1470 | 48210 | 950320 | -20281714.09 | 5262366.096470429 | 3758882491.65 | 0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | fechas | fecha_minima | fecha_maxima | negativos | ceros | positivos | saldo_minimo | saldo_promedio | saldo_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CUENTA DE AHORRO | 987914 | 474248 | 91 | 2025-06-01 | 2026-06-07 | 3 | 47992 | 939919 | -2911.62 | 5241304.075420106 | 3758882491.65 |
| CUENTA DE CORRIENTE | 12086 | 5645 | 67 | 2025-06-01 | 2026-06-06 | 1467 | 218 | 10401 | -20281714.09 | 6983983.295200205 | 1056795163.02 |

#### Cobertura temporal mensual

| mes | fechas_distintas | registros | clientes |
| --- | --- | --- | --- |
| 2025-06 | 7 | 73603 | 73473 |
| 2025-07 | 7 | 73773 | 73629 |
| 2025-08 | 7 | 73916 | 73793 |
| 2025-09 | 7 | 74551 | 74413 |
| 2025-10 | 7 | 75073 | 74963 |
| 2025-11 | 7 | 75677 | 75550 |
| 2025-12 | 7 | 76615 | 76502 |
| 2026-01 | 7 | 76813 | 76689 |
| 2026-02 | 7 | 78509 | 78396 |
| 2026-03 | 7 | 79444 | 79304 |
| 2026-04 | 7 | 79508 | 79381 |
| 2026-05 | 7 | 81018 | 80922 |
| 2026-06 | 7 | 81500 | 81374 |

#### Primeras apariciones observadas por producto y fecha

Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.

| producto | primera_fecha | clientes |
| --- | --- | --- |
| CUENTA DE AHORRO | 2025-06-01 | 70911 |
| CUENTA DE AHORRO | 2025-06-02 | 201 |
| CUENTA DE AHORRO | 2025-06-03 | 160 |
| CUENTA DE AHORRO | 2025-06-04 | 318 |
| CUENTA DE AHORRO | 2025-06-05 | 376 |
| CUENTA DE AHORRO | 2025-06-06 | 436 |
| CUENTA DE AHORRO | 2025-06-07 | 222 |
| CUENTA DE AHORRO | 2025-07-01 | 71083 |
| CUENTA DE AHORRO | 2025-07-02 | 515 |
| CUENTA DE AHORRO | 2025-07-03 | 274 |
| CUENTA DE AHORRO | 2025-07-04 | 234 |
| CUENTA DE AHORRO | 2025-07-05 | 276 |
| CUENTA DE AHORRO | 2025-07-06 | 169 |
| CUENTA DE AHORRO | 2025-07-07 | 38 |
| CUENTA DE AHORRO | 2025-08-01 | 37326 |
| CUENTA DE AHORRO | 2025-08-02 | 460 |
| CUENTA DE AHORRO | 2025-08-03 | 150 |
| CUENTA DE AHORRO | 2025-08-04 | 80 |
| CUENTA DE AHORRO | 2025-08-05 | 166 |
| CUENTA DE AHORRO | 2025-08-06 | 257 |
| CUENTA DE AHORRO | 2025-08-07 | 134 |
| CUENTA DE AHORRO | 2025-09-01 | 68605 |
| CUENTA DE AHORRO | 2025-09-02 | 301 |
| CUENTA DE AHORRO | 2025-09-03 | 258 |
| CUENTA DE AHORRO | 2025-09-04 | 182 |
| CUENTA DE AHORRO | 2025-09-05 | 194 |
| CUENTA DE AHORRO | 2025-09-06 | 304 |
| CUENTA DE AHORRO | 2025-09-07 | 102 |
| CUENTA DE AHORRO | 2025-10-01 | 24906 |
| CUENTA DE AHORRO | 2025-10-02 | 302 |
| CUENTA DE AHORRO | 2025-10-03 | 140 |
| CUENTA DE AHORRO | 2025-10-04 | 303 |
| CUENTA DE AHORRO | 2025-10-05 | 91 |
| CUENTA DE AHORRO | 2025-10-06 | 76 |
| CUENTA DE AHORRO | 2025-10-07 | 151 |
| CUENTA DE AHORRO | 2025-11-01 | 14804 |
| CUENTA DE AHORRO | 2025-11-02 | 321 |
| CUENTA DE AHORRO | 2025-11-03 | 46 |
| CUENTA DE AHORRO | 2025-11-04 | 62 |
| CUENTA DE AHORRO | 2025-11-05 | 142 |
| CUENTA DE AHORRO | 2025-11-06 | 207 |
| CUENTA DE AHORRO | 2025-11-07 | 122 |
| CUENTA DE AHORRO | 2025-12-01 | 60611 |
| CUENTA DE AHORRO | 2025-12-02 | 182 |
| CUENTA DE AHORRO | 2025-12-03 | 248 |
| CUENTA DE AHORRO | 2025-12-04 | 114 |
| CUENTA DE AHORRO | 2025-12-05 | 177 |
| CUENTA DE AHORRO | 2025-12-06 | 240 |
| CUENTA DE AHORRO | 2025-12-07 | 140 |
| CUENTA DE AHORRO | 2026-01-01 | 33541 |
| CUENTA DE AHORRO | 2026-01-02 | 52 |
| CUENTA DE AHORRO | 2026-01-03 | 196 |
| CUENTA DE AHORRO | 2026-01-04 | 55 |
| CUENTA DE AHORRO | 2026-01-05 | 47 |
| CUENTA DE AHORRO | 2026-01-06 | 175 |
| CUENTA DE AHORRO | 2026-01-07 | 121 |
| CUENTA DE AHORRO | 2026-02-01 | 33184 |
| CUENTA DE AHORRO | 2026-02-02 | 56 |
| CUENTA DE AHORRO | 2026-02-03 | 224 |
| CUENTA DE AHORRO | 2026-02-04 | 157 |
| CUENTA DE AHORRO | 2026-02-05 | 144 |
| CUENTA DE AHORRO | 2026-02-06 | 132 |
| CUENTA DE AHORRO | 2026-02-07 | 169 |
| CUENTA DE AHORRO | 2026-03-01 | 10817 |
| CUENTA DE AHORRO | 2026-03-02 | 62 |
| CUENTA DE AHORRO | 2026-03-03 | 160 |
| CUENTA DE AHORRO | 2026-03-04 | 151 |
| CUENTA DE AHORRO | 2026-03-05 | 121 |
| CUENTA DE AHORRO | 2026-03-06 | 144 |
| CUENTA DE AHORRO | 2026-03-07 | 133 |
| CUENTA DE AHORRO | 2026-04-01 | 5145 |
| CUENTA DE AHORRO | 2026-04-02 | 207 |
| CUENTA DE AHORRO | 2026-04-03 | 38 |
| CUENTA DE AHORRO | 2026-04-04 | 28 |
| CUENTA DE AHORRO | 2026-04-05 | 52 |
| CUENTA DE AHORRO | 2026-04-06 | 37 |
| CUENTA DE AHORRO | 2026-04-07 | 140 |
| CUENTA DE AHORRO | 2026-05-01 | 4024 |
| CUENTA DE AHORRO | 2026-05-02 | 98 |
| CUENTA DE AHORRO | 2026-05-03 | 78 |
| CUENTA DE AHORRO | 2026-05-04 | 32 |
| CUENTA DE AHORRO | 2026-05-05 | 154 |
| CUENTA DE AHORRO | 2026-05-06 | 157 |
| CUENTA DE AHORRO | 2026-05-07 | 81 |
| CUENTA DE AHORRO | 2026-06-01 | 26053 |
| CUENTA DE AHORRO | 2026-06-02 | 273 |
| CUENTA DE AHORRO | 2026-06-03 | 210 |
| CUENTA DE AHORRO | 2026-06-04 | 82 |
| CUENTA DE AHORRO | 2026-06-05 | 65 |
| CUENTA DE AHORRO | 2026-06-06 | 258 |
| CUENTA DE AHORRO | 2026-06-07 | 78 |
| CUENTA DE CORRIENTE | 2025-06-01 | 960 |
| CUENTA DE CORRIENTE | 2025-06-03 | 1 |
| CUENTA DE CORRIENTE | 2025-06-04 | 2 |
| CUENTA DE CORRIENTE | 2025-06-05 | 1 |
| CUENTA DE CORRIENTE | 2025-07-01 | 944 |
| CUENTA DE CORRIENTE | 2025-07-02 | 5 |
| CUENTA DE CORRIENTE | 2025-07-03 | 4 |
| CUENTA DE CORRIENTE | 2025-07-05 | 1 |
| CUENTA DE CORRIENTE | 2025-07-06 | 1 |
| CUENTA DE CORRIENTE | 2025-08-01 | 263 |
| CUENTA DE CORRIENTE | 2025-08-02 | 3 |
| CUENTA DE CORRIENTE | 2025-08-03 | 1 |
| CUENTA DE CORRIENTE | 2025-08-05 | 1 |
| CUENTA DE CORRIENTE | 2025-08-06 | 2 |
| CUENTA DE CORRIENTE | 2025-08-07 | 1 |
| CUENTA DE CORRIENTE | 2025-09-01 | 881 |
| CUENTA DE CORRIENTE | 2025-09-04 | 2 |
| CUENTA DE CORRIENTE | 2025-09-07 | 2 |
| CUENTA DE CORRIENTE | 2025-10-01 | 134 |
| CUENTA DE CORRIENTE | 2025-10-02 | 2 |
| CUENTA DE CORRIENTE | 2025-10-03 | 1 |
| CUENTA DE CORRIENTE | 2025-10-05 | 1 |
| CUENTA DE CORRIENTE | 2025-11-01 | 410 |
| CUENTA DE CORRIENTE | 2025-11-02 | 1 |
| CUENTA DE CORRIENTE | 2025-11-05 | 2 |
| CUENTA DE CORRIENTE | 2025-12-01 | 757 |
| CUENTA DE CORRIENTE | 2025-12-02 | 1 |
| CUENTA DE CORRIENTE | 2025-12-05 | 3 |
| CUENTA DE CORRIENTE | 2026-01-01 | 148 |
| CUENTA DE CORRIENTE | 2026-01-03 | 2 |
| CUENTA DE CORRIENTE | 2026-02-01 | 239 |
| CUENTA DE CORRIENTE | 2026-02-05 | 2 |
| CUENTA DE CORRIENTE | 2026-03-01 | 162 |
| CUENTA DE CORRIENTE | 2026-03-03 | 3 |
| CUENTA DE CORRIENTE | 2026-03-06 | 1 |
| CUENTA DE CORRIENTE | 2026-04-01 | 132 |
| CUENTA DE CORRIENTE | 2026-05-01 | 391 |
| CUENTA DE CORRIENTE | 2026-05-02 | 2 |
| CUENTA DE CORRIENTE | 2026-06-01 | 176 |

### Tabla `crean_bolsillos`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| fecha | TEXT | 0 | 0 |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| saldo | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| crean_bolsillos | fecha | TEXT | TEXT, DATE, DATETIME | OK |
| crean_bolsillos | numero_id | INTEGER | INTEGER | OK |
| crean_bolsillos | producto | TEXT | TEXT | OK |
| crean_bolsillos | saldo | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | fechas | fecha_minima | fecha_maxima | fechas_nulas | fechas_invalidas | ids_nulos | productos_nulos | saldos_nulos | saldos_negativos | saldos_cero | saldos_positivos | saldo_minimo | saldo_promedio | saldo_maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion | duplicados_claves_con_saldos_distintos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000000 | 260714 | 1 | 37 | 2025-06-01 | 2026-06-01 | 0 | 0 | 0 | 0 | 0 | 0 | 467155 | 532845 | 0.0 | 1090564.3009568057 | 2050000000.0 | 0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | fechas | fecha_minima | fecha_maxima | negativos | ceros | positivos | saldo_minimo | saldo_promedio | saldo_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOLSILLOS | 1000000 | 260714 | 37 | 2025-06-01 | 2026-06-01 | 0 | 467155 | 532845 | 0.0 | 1090564.3009568057 | 2050000000.0 |

#### Cobertura temporal mensual

| mes | fechas_distintas | registros | clientes |
| --- | --- | --- | --- |
| 2025-06 | 1 | 68505 | 68505 |
| 2025-07 | 1 | 69894 | 69894 |
| 2025-08 | 1 | 71511 | 71511 |
| 2025-09 | 1 | 72400 | 72400 |
| 2025-10 | 1 | 73845 | 73845 |
| 2025-11 | 1 | 74716 | 74716 |
| 2025-12 | 1 | 76068 | 76068 |
| 2026-01 | 7 | 79328 | 78772 |
| 2026-02 | 7 | 81493 | 80779 |
| 2026-03 | 7 | 83266 | 82551 |
| 2026-04 | 7 | 83898 | 83430 |
| 2026-05 | 1 | 82736 | 82736 |
| 2026-06 | 1 | 82340 | 82340 |

#### Primeras apariciones observadas por producto y fecha

Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.

| producto | primera_fecha | clientes |
| --- | --- | --- |
| BOLSILLOS | 2025-06-01 | 68505 |
| BOLSILLOS | 2025-07-01 | 58431 |
| BOLSILLOS | 2025-08-01 | 32268 |
| BOLSILLOS | 2025-09-01 | 20236 |
| BOLSILLOS | 2025-10-01 | 9765 |
| BOLSILLOS | 2025-11-01 | 6601 |
| BOLSILLOS | 2025-12-01 | 5438 |
| BOLSILLOS | 2026-01-01 | 8230 |
| BOLSILLOS | 2026-01-02 | 98 |
| BOLSILLOS | 2026-01-03 | 76 |
| BOLSILLOS | 2026-01-04 | 108 |
| BOLSILLOS | 2026-01-05 | 45 |
| BOLSILLOS | 2026-01-06 | 194 |
| BOLSILLOS | 2026-01-07 | 77 |
| BOLSILLOS | 2026-02-01 | 19409 |
| BOLSILLOS | 2026-02-02 | 76 |
| BOLSILLOS | 2026-02-03 | 143 |
| BOLSILLOS | 2026-02-04 | 80 |
| BOLSILLOS | 2026-02-05 | 121 |
| BOLSILLOS | 2026-02-06 | 76 |
| BOLSILLOS | 2026-02-07 | 83 |
| BOLSILLOS | 2026-03-01 | 4380 |
| BOLSILLOS | 2026-03-02 | 113 |
| BOLSILLOS | 2026-03-03 | 75 |
| BOLSILLOS | 2026-03-04 | 127 |
| BOLSILLOS | 2026-03-05 | 72 |
| BOLSILLOS | 2026-03-06 | 68 |
| BOLSILLOS | 2026-03-07 | 74 |
| BOLSILLOS | 2026-04-01 | 15539 |
| BOLSILLOS | 2026-04-02 | 84 |
| BOLSILLOS | 2026-04-03 | 55 |
| BOLSILLOS | 2026-04-04 | 43 |
| BOLSILLOS | 2026-04-05 | 45 |
| BOLSILLOS | 2026-04-06 | 39 |
| BOLSILLOS | 2026-04-07 | 71 |
| BOLSILLOS | 2026-05-01 | 7016 |
| BOLSILLOS | 2026-06-01 | 2853 |

### Tabla `crean_fiducuenta`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| fecha | TEXT | 0 | 0 |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| saldo | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| crean_fiducuenta | fecha | TEXT | TEXT, DATE, DATETIME | OK |
| crean_fiducuenta | numero_id | INTEGER | INTEGER | OK |
| crean_fiducuenta | producto | TEXT | TEXT | OK |
| crean_fiducuenta | saldo | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | fechas | fecha_minima | fecha_maxima | fechas_nulas | fechas_invalidas | ids_nulos | productos_nulos | saldos_nulos | saldos_negativos | saldos_cero | saldos_positivos | saldo_minimo | saldo_promedio | saldo_maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion | duplicados_claves_con_saldos_distintos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000000 | 181021 | 1 | 64 | 2025-06-01 | 2026-06-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1000000 | 0.05 | 8374629.896962052 | 4499723786.14 | 0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | fechas | fecha_minima | fecha_maxima | negativos | ceros | positivos | saldo_minimo | saldo_promedio | saldo_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FIDUCUENTA | 1000000 | 181021 | 64 | 2025-06-01 | 2026-06-06 | 0 | 0 | 1000000 | 0.05 | 8374629.896962052 | 4499723786.14 |

#### Cobertura temporal mensual

| mes | fechas_distintas | registros | clientes |
| --- | --- | --- | --- |
| 2025-06 | 1 | 73962 | 73962 |
| 2025-07 | 1 | 74353 | 74353 |
| 2025-08 | 6 | 74909 | 74889 |
| 2025-09 | 6 | 75458 | 75441 |
| 2025-10 | 6 | 76467 | 76448 |
| 2025-11 | 5 | 76239 | 76233 |
| 2025-12 | 6 | 76224 | 76200 |
| 2026-01 | 5 | 77040 | 77024 |
| 2026-02 | 7 | 78155 | 78130 |
| 2026-03 | 6 | 78616 | 78602 |
| 2026-04 | 4 | 78851 | 78835 |
| 2026-05 | 5 | 79342 | 79328 |
| 2026-06 | 6 | 80384 | 80361 |

#### Primeras apariciones observadas por producto y fecha

Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.

| producto | primera_fecha | clientes |
| --- | --- | --- |
| FIDUCUENTA | 2025-06-01 | 73962 |
| FIDUCUENTA | 2025-07-01 | 27406 |
| FIDUCUENTA | 2025-08-01 | 44980 |
| FIDUCUENTA | 2025-08-02 | 35 |
| FIDUCUENTA | 2025-08-04 | 8 |
| FIDUCUENTA | 2025-08-05 | 42 |
| FIDUCUENTA | 2025-08-06 | 25 |
| FIDUCUENTA | 2025-08-07 | 33 |
| FIDUCUENTA | 2025-09-01 | 13047 |
| FIDUCUENTA | 2025-09-02 | 39 |
| FIDUCUENTA | 2025-09-03 | 47 |
| FIDUCUENTA | 2025-09-04 | 33 |
| FIDUCUENTA | 2025-09-05 | 33 |
| FIDUCUENTA | 2025-09-06 | 30 |
| FIDUCUENTA | 2025-10-01 | 5275 |
| FIDUCUENTA | 2025-10-02 | 46 |
| FIDUCUENTA | 2025-10-03 | 27 |
| FIDUCUENTA | 2025-10-04 | 29 |
| FIDUCUENTA | 2025-10-05 | 6 |
| FIDUCUENTA | 2025-10-07 | 32 |
| FIDUCUENTA | 2025-11-01 | 3828 |
| FIDUCUENTA | 2025-11-02 | 3 |
| FIDUCUENTA | 2025-11-05 | 37 |
| FIDUCUENTA | 2025-11-06 | 34 |
| FIDUCUENTA | 2025-11-07 | 29 |
| FIDUCUENTA | 2025-12-01 | 1605 |
| FIDUCUENTA | 2025-12-02 | 36 |
| FIDUCUENTA | 2025-12-03 | 23 |
| FIDUCUENTA | 2025-12-04 | 33 |
| FIDUCUENTA | 2025-12-05 | 36 |
| FIDUCUENTA | 2025-12-07 | 25 |
| FIDUCUENTA | 2026-01-01 | 1272 |
| FIDUCUENTA | 2026-01-03 | 42 |
| FIDUCUENTA | 2026-01-05 | 16 |
| FIDUCUENTA | 2026-01-06 | 38 |
| FIDUCUENTA | 2026-01-07 | 50 |
| FIDUCUENTA | 2026-02-01 | 2384 |
| FIDUCUENTA | 2026-02-02 | 19 |
| FIDUCUENTA | 2026-02-03 | 54 |
| FIDUCUENTA | 2026-02-04 | 41 |
| FIDUCUENTA | 2026-02-05 | 43 |
| FIDUCUENTA | 2026-02-06 | 40 |
| FIDUCUENTA | 2026-02-07 | 33 |
| FIDUCUENTA | 2026-03-01 | 1337 |
| FIDUCUENTA | 2026-03-03 | 46 |
| FIDUCUENTA | 2026-03-04 | 25 |
| FIDUCUENTA | 2026-03-05 | 26 |
| FIDUCUENTA | 2026-03-06 | 30 |
| FIDUCUENTA | 2026-03-07 | 27 |
| FIDUCUENTA | 2026-04-01 | 1147 |
| FIDUCUENTA | 2026-04-02 | 43 |
| FIDUCUENTA | 2026-04-06 | 9 |
| FIDUCUENTA | 2026-04-07 | 36 |
| FIDUCUENTA | 2026-05-01 | 1902 |
| FIDUCUENTA | 2026-05-03 | 19 |
| FIDUCUENTA | 2026-05-05 | 52 |
| FIDUCUENTA | 2026-05-06 | 34 |
| FIDUCUENTA | 2026-05-07 | 38 |
| FIDUCUENTA | 2026-06-01 | 1227 |
| FIDUCUENTA | 2026-06-02 | 41 |
| FIDUCUENTA | 2026-06-03 | 31 |
| FIDUCUENTA | 2026-06-04 | 35 |
| FIDUCUENTA | 2026-06-05 | 31 |
| FIDUCUENTA | 2026-06-06 | 29 |

### Tabla `crean_inv_virtual_cdt`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| fecha | TEXT | 0 | 0 |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| saldo | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| crean_inv_virtual_cdt | fecha | TEXT | TEXT, DATE, DATETIME | OK |
| crean_inv_virtual_cdt | numero_id | INTEGER | INTEGER | OK |
| crean_inv_virtual_cdt | producto | TEXT | TEXT | OK |
| crean_inv_virtual_cdt | saldo | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | fechas | fecha_minima | fecha_maxima | fechas_nulas | fechas_invalidas | ids_nulos | productos_nulos | saldos_nulos | saldos_negativos | saldos_cero | saldos_positivos | saldo_minimo | saldo_promedio | saldo_maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion | duplicados_claves_con_saldos_distintos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 994177 | 84104 | 2 | 391 | 2025-06-01 | 2026-06-30 | 0 | 0 | 0 | 0 | 0 | 0 | 4017 | 990160 | 0.0 | 41643712.21679985 | 6000000000.0 | 0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | fechas | fecha_minima | fecha_maxima | negativos | ceros | positivos | saldo_minimo | saldo_promedio | saldo_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVERSIóN VIRTUAL | 678038 | 61215 | 390 | 2025-06-01 | 2026-06-30 | 0 | 4017 | 674021 | 0.0 | 41412363.18184145 | 5664000000.0 |
| CDT | 316139 | 26273 | 338 | 2025-06-01 | 2026-06-28 | 0 | 0 | 316139 | 20000.0 | 42139897.2397815 | 6000000000.0 |

#### Cobertura temporal mensual

| mes | fechas_distintas | registros | clientes |
| --- | --- | --- | --- |
| 2025-06 | 30 | 74682 | 57292 |
| 2025-07 | 31 | 76317 | 57929 |
| 2025-08 | 31 | 75037 | 58214 |
| 2025-09 | 30 | 73387 | 58015 |
| 2025-10 | 30 | 73692 | 57996 |
| 2025-11 | 30 | 72134 | 57707 |
| 2025-12 | 30 | 78200 | 58415 |
| 2026-01 | 31 | 77351 | 58907 |
| 2026-02 | 27 | 75135 | 59136 |
| 2026-03 | 31 | 79853 | 60545 |
| 2026-04 | 30 | 78956 | 61516 |
| 2026-05 | 30 | 79328 | 61882 |
| 2026-06 | 30 | 80105 | 62133 |

#### Primeras apariciones observadas por producto y fecha

Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.

| producto | primera_fecha | clientes |
| --- | --- | --- |
| CDT | 2025-06-01 | 20394 |
| CDT | 2025-06-04 | 58 |
| CDT | 2025-06-05 | 239 |
| CDT | 2025-06-06 | 70 |
| CDT | 2025-06-07 | 70 |
| CDT | 2025-06-08 | 93 |
| CDT | 2025-06-09 | 1 |
| CDT | 2025-06-10 | 22 |
| CDT | 2025-06-11 | 92 |
| CDT | 2025-06-12 | 27 |
| CDT | 2025-06-13 | 29 |
| CDT | 2025-06-14 | 20 |
| CDT | 2025-06-15 | 3 |
| CDT | 2025-06-17 | 28 |
| CDT | 2025-06-18 | 25 |
| CDT | 2025-06-19 | 20 |
| CDT | 2025-06-20 | 17 |
| CDT | 2025-06-21 | 28 |
| CDT | 2025-06-22 | 3 |
| CDT | 2025-06-25 | 20 |
| CDT | 2025-06-26 | 33 |
| CDT | 2025-06-27 | 26 |
| CDT | 2025-06-28 | 40 |
| CDT | 2025-06-29 | 5 |
| CDT | 2025-07-01 | 1 |
| CDT | 2025-07-02 | 31 |
| CDT | 2025-07-03 | 27 |
| CDT | 2025-07-04 | 35 |
| CDT | 2025-07-05 | 30 |
| CDT | 2025-07-06 | 4 |
| CDT | 2025-07-08 | 32 |
| CDT | 2025-07-09 | 30 |
| CDT | 2025-07-10 | 34 |
| CDT | 2025-07-11 | 21 |
| CDT | 2025-07-12 | 29 |
| CDT | 2025-07-13 | 6 |
| CDT | 2025-07-15 | 18 |
| CDT | 2025-07-16 | 25 |
| CDT | 2025-07-17 | 24 |
| CDT | 2025-07-18 | 15 |
| CDT | 2025-07-19 | 20 |
| CDT | 2025-07-20 | 4 |
| CDT | 2025-07-22 | 14 |
| CDT | 2025-07-23 | 12 |
| CDT | 2025-07-24 | 19 |
| CDT | 2025-07-25 | 17 |
| CDT | 2025-07-26 | 18 |
| CDT | 2025-07-27 | 9 |
| CDT | 2025-07-29 | 15 |
| CDT | 2025-07-30 | 18 |
| CDT | 2025-07-31 | 13 |
| CDT | 2025-08-01 | 35 |
| CDT | 2025-08-02 | 18 |
| CDT | 2025-08-03 | 5 |
| CDT | 2025-08-05 | 33 |
| CDT | 2025-08-06 | 19 |
| CDT | 2025-08-07 | 33 |
| CDT | 2025-08-09 | 37 |
| CDT | 2025-08-10 | 4 |
| CDT | 2025-08-12 | 25 |
| CDT | 2025-08-13 | 16 |
| CDT | 2025-08-14 | 17 |
| CDT | 2025-08-15 | 24 |
| CDT | 2025-08-16 | 16 |
| CDT | 2025-08-17 | 2 |
| CDT | 2025-08-20 | 20 |
| CDT | 2025-08-21 | 20 |
| CDT | 2025-08-22 | 23 |
| CDT | 2025-08-23 | 20 |
| CDT | 2025-08-24 | 4 |
| CDT | 2025-08-26 | 21 |
| CDT | 2025-08-27 | 9 |
| CDT | 2025-08-28 | 15 |
| CDT | 2025-08-29 | 25 |
| CDT | 2025-08-30 | 31 |
| CDT | 2025-08-31 | 5 |
| CDT | 2025-09-02 | 27 |
| CDT | 2025-09-03 | 17 |
| CDT | 2025-09-04 | 14 |
| CDT | 2025-09-05 | 19 |
| CDT | 2025-09-06 | 13 |
| CDT | 2025-09-07 | 7 |
| CDT | 2025-09-09 | 26 |
| CDT | 2025-09-10 | 18 |
| CDT | 2025-09-11 | 13 |
| CDT | 2025-09-12 | 12 |
| CDT | 2025-09-13 | 24 |
| CDT | 2025-09-14 | 3 |
| CDT | 2025-09-16 | 23 |
| CDT | 2025-09-17 | 14 |
| CDT | 2025-09-18 | 14 |
| CDT | 2025-09-19 | 14 |
| CDT | 2025-09-20 | 13 |
| CDT | 2025-09-21 | 3 |
| CDT | 2025-09-23 | 21 |
| CDT | 2025-09-24 | 24 |
| CDT | 2025-09-25 | 14 |
| CDT | 2025-09-26 | 14 |
| CDT | 2025-09-27 | 15 |
| CDT | 2025-09-28 | 2 |
| CDT | 2025-09-30 | 15 |
| CDT | 2025-10-01 | 26 |
| CDT | 2025-10-02 | 17 |
| CDT | 2025-10-03 | 14 |
| CDT | 2025-10-04 | 15 |
| CDT | 2025-10-05 | 6 |
| CDT | 2025-10-07 | 13 |
| CDT | 2025-10-08 | 22 |
| CDT | 2025-10-09 | 19 |
| CDT | 2025-10-10 | 17 |
| CDT | 2025-10-11 | 22 |
| CDT | 2025-10-12 | 2 |
| CDT | 2025-10-15 | 21 |
| CDT | 2025-10-16 | 18 |
| CDT | 2025-10-17 | 14 |
| CDT | 2025-10-18 | 25 |
| CDT | 2025-10-19 | 5 |
| CDT | 2025-10-21 | 6 |
| CDT | 2025-10-22 | 14 |
| CDT | 2025-10-23 | 21 |
| CDT | 2025-10-25 | 17 |
| CDT | 2025-10-26 | 7 |
| CDT | 2025-10-28 | 12 |
| CDT | 2025-10-29 | 13 |
| CDT | 2025-10-30 | 17 |
| CDT | 2025-10-31 | 23 |
| CDT | 2025-11-01 | 11 |
| CDT | 2025-11-02 | 4 |
| CDT | 2025-11-05 | 12 |
| CDT | 2025-11-06 | 13 |
| CDT | 2025-11-07 | 10 |
| CDT | 2025-11-08 | 20 |
| CDT | 2025-11-09 | 5 |
| CDT | 2025-11-11 | 13 |
| CDT | 2025-11-12 | 21 |
| CDT | 2025-11-13 | 12 |
| CDT | 2025-11-14 | 9 |
| CDT | 2025-11-15 | 10 |
| CDT | 2025-11-16 | 7 |
| CDT | 2025-11-19 | 15 |
| CDT | 2025-11-20 | 13 |
| CDT | 2025-11-21 | 21 |
| CDT | 2025-11-22 | 15 |
| CDT | 2025-11-23 | 4 |
| CDT | 2025-11-25 | 13 |
| CDT | 2025-11-26 | 11 |
| CDT | 2025-11-27 | 17 |
| CDT | 2025-11-28 | 13 |
| CDT | 2025-11-29 | 20 |
| CDT | 2025-11-30 | 5 |
| CDT | 2025-12-02 | 16 |
| CDT | 2025-12-03 | 19 |
| CDT | 2025-12-04 | 12 |
| CDT | 2025-12-05 | 18 |
| CDT | 2025-12-06 | 20 |
| CDT | 2025-12-07 | 5 |
| CDT | 2025-12-10 | 11 |
| CDT | 2025-12-11 | 15 |
| CDT | 2025-12-12 | 20 |
| CDT | 2025-12-13 | 27 |
| CDT | 2025-12-15 | 5 |
| CDT | 2025-12-16 | 28 |
| CDT | 2025-12-17 | 19 |
| CDT | 2025-12-18 | 22 |
| CDT | 2025-12-19 | 20 |
| CDT | 2025-12-20 | 16 |
| CDT | 2025-12-21 | 2 |
| CDT | 2025-12-23 | 19 |
| CDT | 2025-12-24 | 15 |
| CDT | 2025-12-25 | 7 |
| CDT | 2025-12-27 | 35 |
| CDT | 2025-12-28 | 7 |
| CDT | 2025-12-30 | 35 |
| CDT | 2025-12-31 | 17 |
| CDT | 2026-01-01 | 1 |
| CDT | 2026-01-03 | 14 |
| CDT | 2026-01-04 | 5 |
| CDT | 2026-01-06 | 25 |
| CDT | 2026-01-07 | 18 |
| CDT | 2026-01-08 | 18 |
| CDT | 2026-01-09 | 18 |
| CDT | 2026-01-10 | 24 |
| CDT | 2026-01-11 | 6 |
| CDT | 2026-01-14 | 30 |
| CDT | 2026-01-15 | 22 |
| CDT | 2026-01-16 | 25 |
| CDT | 2026-01-17 | 21 |
| CDT | 2026-01-18 | 5 |
| CDT | 2026-01-20 | 17 |
| CDT | 2026-01-21 | 22 |
| CDT | 2026-01-22 | 16 |
| CDT | 2026-01-23 | 16 |
| CDT | 2026-01-24 | 28 |
| CDT | 2026-01-25 | 3 |
| CDT | 2026-01-27 | 22 |
| CDT | 2026-01-28 | 18 |
| CDT | 2026-01-29 | 18 |
| CDT | 2026-01-30 | 23 |
| CDT | 2026-01-31 | 24 |
| CDT | 2026-02-01 | 3 |
| CDT | 2026-02-03 | 24 |
| CDT | 2026-02-04 | 20 |
| CDT | 2026-02-05 | 21 |
| CDT | 2026-02-06 | 28 |
| CDT | 2026-02-07 | 18 |
| CDT | 2026-02-08 | 2 |
| CDT | 2026-02-10 | 19 |
| CDT | 2026-02-11 | 26 |
| CDT | 2026-02-12 | 30 |
| CDT | 2026-02-13 | 21 |
| CDT | 2026-02-14 | 15 |
| CDT | 2026-02-15 | 5 |
| CDT | 2026-02-17 | 24 |
| CDT | 2026-02-18 | 28 |
| CDT | 2026-02-19 | 24 |
| CDT | 2026-02-20 | 27 |
| CDT | 2026-02-21 | 28 |
| CDT | 2026-02-23 | 5 |
| CDT | 2026-02-24 | 5 |
| CDT | 2026-02-25 | 16 |
| CDT | 2026-02-26 | 27 |
| CDT | 2026-02-27 | 14 |
| CDT | 2026-02-28 | 34 |
| CDT | 2026-03-01 | 11 |
| CDT | 2026-03-03 | 34 |
| CDT | 2026-03-04 | 33 |
| CDT | 2026-03-05 | 32 |
| CDT | 2026-03-06 | 36 |
| CDT | 2026-03-07 | 25 |
| CDT | 2026-03-08 | 3 |
| CDT | 2026-03-10 | 27 |
| CDT | 2026-03-11 | 37 |
| CDT | 2026-03-12 | 19 |
| CDT | 2026-03-13 | 27 |
| CDT | 2026-03-14 | 19 |
| CDT | 2026-03-15 | 6 |
| CDT | 2026-03-17 | 29 |
| CDT | 2026-03-18 | 22 |
| CDT | 2026-03-19 | 18 |
| CDT | 2026-03-20 | 20 |
| CDT | 2026-03-21 | 21 |
| CDT | 2026-03-22 | 2 |
| CDT | 2026-03-25 | 13 |
| CDT | 2026-03-26 | 23 |
| CDT | 2026-03-27 | 16 |
| CDT | 2026-03-28 | 18 |
| CDT | 2026-03-29 | 3 |
| CDT | 2026-03-31 | 27 |
| CDT | 2026-04-01 | 15 |
| CDT | 2026-04-02 | 22 |
| CDT | 2026-04-05 | 1 |
| CDT | 2026-04-07 | 21 |
| CDT | 2026-04-08 | 26 |
| CDT | 2026-04-09 | 22 |
| CDT | 2026-04-10 | 23 |
| CDT | 2026-04-11 | 18 |
| CDT | 2026-04-12 | 3 |
| CDT | 2026-04-14 | 23 |
| CDT | 2026-04-15 | 21 |
| CDT | 2026-04-16 | 25 |
| CDT | 2026-04-17 | 25 |
| CDT | 2026-04-18 | 24 |
| CDT | 2026-04-19 | 1 |
| CDT | 2026-04-21 | 14 |
| CDT | 2026-04-22 | 16 |
| CDT | 2026-04-23 | 15 |
| CDT | 2026-04-24 | 20 |
| CDT | 2026-04-25 | 21 |
| CDT | 2026-04-26 | 4 |
| CDT | 2026-04-28 | 23 |
| CDT | 2026-04-29 | 13 |
| CDT | 2026-04-30 | 17 |
| CDT | 2026-05-01 | 16 |
| CDT | 2026-05-03 | 2 |
| CDT | 2026-05-05 | 16 |
| CDT | 2026-05-06 | 21 |
| CDT | 2026-05-07 | 14 |
| CDT | 2026-05-08 | 9 |
| CDT | 2026-05-09 | 21 |
| CDT | 2026-05-10 | 1 |
| CDT | 2026-05-12 | 17 |
| CDT | 2026-05-13 | 13 |
| CDT | 2026-05-14 | 17 |
| CDT | 2026-05-15 | 11 |
| CDT | 2026-05-16 | 12 |
| CDT | 2026-05-17 | 2 |
| CDT | 2026-05-20 | 11 |
| CDT | 2026-05-21 | 16 |
| CDT | 2026-05-23 | 29 |
| CDT | 2026-05-24 | 2 |
| CDT | 2026-05-26 | 19 |
| CDT | 2026-05-27 | 14 |
| CDT | 2026-05-28 | 14 |
| CDT | 2026-05-29 | 13 |
| CDT | 2026-05-30 | 15 |
| CDT | 2026-05-31 | 2 |
| CDT | 2026-06-02 | 20 |
| CDT | 2026-06-03 | 27 |
| CDT | 2026-06-04 | 11 |
| CDT | 2026-06-05 | 7 |
| CDT | 2026-06-06 | 21 |
| CDT | 2026-06-07 | 3 |
| CDT | 2026-06-10 | 26 |
| CDT | 2026-06-11 | 21 |
| CDT | 2026-06-12 | 14 |
| CDT | 2026-06-13 | 17 |
| CDT | 2026-06-14 | 5 |
| CDT | 2026-06-17 | 17 |
| CDT | 2026-06-18 | 20 |
| CDT | 2026-06-19 | 14 |
| CDT | 2026-06-20 | 11 |
| CDT | 2026-06-21 | 4 |
| CDT | 2026-06-23 | 15 |
| CDT | 2026-06-24 | 10 |
| CDT | 2026-06-25 | 12 |
| CDT | 2026-06-26 | 12 |
| CDT | 2026-06-27 | 10 |
| CDT | 2026-06-28 | 2 |
| INVERSIóN VIRTUAL | 2025-06-01 | 33794 |
| INVERSIóN VIRTUAL | 2025-06-02 | 67 |
| INVERSIóN VIRTUAL | 2025-06-03 | 93 |
| INVERSIóN VIRTUAL | 2025-06-04 | 132 |
| INVERSIóN VIRTUAL | 2025-06-05 | 246 |
| INVERSIóN VIRTUAL | 2025-06-06 | 180 |
| INVERSIóN VIRTUAL | 2025-06-07 | 174 |
| INVERSIóN VIRTUAL | 2025-06-08 | 90 |
| INVERSIóN VIRTUAL | 2025-06-09 | 54 |
| INVERSIóN VIRTUAL | 2025-06-10 | 133 |
| INVERSIóN VIRTUAL | 2025-06-11 | 120 |
| INVERSIóN VIRTUAL | 2025-06-12 | 116 |
| INVERSIóN VIRTUAL | 2025-06-13 | 113 |
| INVERSIóN VIRTUAL | 2025-06-14 | 192 |
| INVERSIóN VIRTUAL | 2025-06-15 | 90 |
| INVERSIóN VIRTUAL | 2025-06-16 | 50 |
| INVERSIóN VIRTUAL | 2025-06-17 | 177 |
| INVERSIóN VIRTUAL | 2025-06-18 | 140 |
| INVERSIóN VIRTUAL | 2025-06-19 | 115 |
| INVERSIóN VIRTUAL | 2025-06-20 | 96 |
| INVERSIóN VIRTUAL | 2025-06-21 | 123 |
| INVERSIóN VIRTUAL | 2025-06-22 | 60 |
| INVERSIóN VIRTUAL | 2025-06-23 | 28 |
| INVERSIóN VIRTUAL | 2025-06-24 | 29 |
| INVERSIóN VIRTUAL | 2025-06-25 | 95 |
| INVERSIóN VIRTUAL | 2025-06-26 | 121 |
| INVERSIóN VIRTUAL | 2025-06-27 | 137 |
| INVERSIóN VIRTUAL | 2025-06-28 | 166 |
| INVERSIóN VIRTUAL | 2025-06-29 | 102 |
| INVERSIóN VIRTUAL | 2025-06-30 | 51 |
| INVERSIóN VIRTUAL | 2025-07-01 | 60 |
| INVERSIóN VIRTUAL | 2025-07-02 | 148 |
| INVERSIóN VIRTUAL | 2025-07-03 | 159 |
| INVERSIóN VIRTUAL | 2025-07-04 | 153 |
| INVERSIóN VIRTUAL | 2025-07-05 | 127 |
| INVERSIóN VIRTUAL | 2025-07-06 | 80 |
| INVERSIóN VIRTUAL | 2025-07-07 | 14 |
| INVERSIóN VIRTUAL | 2025-07-08 | 111 |
| INVERSIóN VIRTUAL | 2025-07-09 | 133 |
| INVERSIóN VIRTUAL | 2025-07-10 | 121 |
| INVERSIóN VIRTUAL | 2025-07-11 | 106 |
| INVERSIóN VIRTUAL | 2025-07-12 | 116 |
| INVERSIóN VIRTUAL | 2025-07-13 | 55 |
| INVERSIóN VIRTUAL | 2025-07-14 | 44 |
| INVERSIóN VIRTUAL | 2025-07-15 | 118 |
| INVERSIóN VIRTUAL | 2025-07-16 | 120 |
| INVERSIóN VIRTUAL | 2025-07-17 | 119 |
| INVERSIóN VIRTUAL | 2025-07-18 | 93 |
| INVERSIóN VIRTUAL | 2025-07-19 | 89 |
| INVERSIóN VIRTUAL | 2025-07-20 | 57 |
| INVERSIóN VIRTUAL | 2025-07-21 | 27 |
| INVERSIóN VIRTUAL | 2025-07-22 | 82 |
| INVERSIóN VIRTUAL | 2025-07-23 | 90 |
| INVERSIóN VIRTUAL | 2025-07-24 | 83 |
| INVERSIóN VIRTUAL | 2025-07-25 | 84 |
| INVERSIóN VIRTUAL | 2025-07-26 | 93 |
| INVERSIóN VIRTUAL | 2025-07-27 | 50 |
| INVERSIóN VIRTUAL | 2025-07-28 | 31 |
| INVERSIóN VIRTUAL | 2025-07-29 | 85 |
| INVERSIóN VIRTUAL | 2025-07-30 | 80 |
| INVERSIóN VIRTUAL | 2025-07-31 | 103 |
| INVERSIóN VIRTUAL | 2025-08-01 | 122 |
| INVERSIóN VIRTUAL | 2025-08-02 | 137 |
| INVERSIóN VIRTUAL | 2025-08-03 | 73 |
| INVERSIóN VIRTUAL | 2025-08-04 | 42 |
| INVERSIóN VIRTUAL | 2025-08-05 | 108 |
| INVERSIóN VIRTUAL | 2025-08-06 | 100 |
| INVERSIóN VIRTUAL | 2025-08-07 | 104 |
| INVERSIóN VIRTUAL | 2025-08-08 | 47 |
| INVERSIóN VIRTUAL | 2025-08-09 | 84 |
| INVERSIóN VIRTUAL | 2025-08-10 | 45 |
| INVERSIóN VIRTUAL | 2025-08-11 | 36 |
| INVERSIóN VIRTUAL | 2025-08-12 | 87 |
| INVERSIóN VIRTUAL | 2025-08-13 | 95 |
| INVERSIóN VIRTUAL | 2025-08-14 | 68 |
| INVERSIóN VIRTUAL | 2025-08-15 | 87 |
| INVERSIóN VIRTUAL | 2025-08-16 | 91 |
| INVERSIóN VIRTUAL | 2025-08-17 | 64 |
| INVERSIóN VIRTUAL | 2025-08-18 | 30 |
| INVERSIóN VIRTUAL | 2025-08-19 | 27 |
| INVERSIóN VIRTUAL | 2025-08-20 | 104 |
| INVERSIóN VIRTUAL | 2025-08-21 | 91 |
| INVERSIóN VIRTUAL | 2025-08-22 | 78 |
| INVERSIóN VIRTUAL | 2025-08-23 | 80 |
| INVERSIóN VIRTUAL | 2025-08-24 | 41 |
| INVERSIóN VIRTUAL | 2025-08-25 | 28 |
| INVERSIóN VIRTUAL | 2025-08-26 | 81 |
| INVERSIóN VIRTUAL | 2025-08-27 | 81 |
| INVERSIóN VIRTUAL | 2025-08-28 | 84 |
| INVERSIóN VIRTUAL | 2025-08-29 | 79 |
| INVERSIóN VIRTUAL | 2025-08-30 | 112 |
| INVERSIóN VIRTUAL | 2025-08-31 | 59 |
| INVERSIóN VIRTUAL | 2025-09-01 | 37 |
| INVERSIóN VIRTUAL | 2025-09-02 | 109 |
| INVERSIóN VIRTUAL | 2025-09-03 | 95 |
| INVERSIóN VIRTUAL | 2025-09-04 | 63 |
| INVERSIóN VIRTUAL | 2025-09-05 | 85 |
| INVERSIóN VIRTUAL | 2025-09-06 | 72 |
| INVERSIóN VIRTUAL | 2025-09-07 | 32 |
| INVERSIóN VIRTUAL | 2025-09-08 | 32 |
| INVERSIóN VIRTUAL | 2025-09-09 | 89 |
| INVERSIóN VIRTUAL | 2025-09-10 | 84 |
| INVERSIóN VIRTUAL | 2025-09-11 | 72 |
| INVERSIóN VIRTUAL | 2025-09-12 | 68 |
| INVERSIóN VIRTUAL | 2025-09-13 | 85 |
| INVERSIóN VIRTUAL | 2025-09-14 | 35 |
| INVERSIóN VIRTUAL | 2025-09-15 | 23 |
| INVERSIóN VIRTUAL | 2025-09-16 | 86 |
| INVERSIóN VIRTUAL | 2025-09-17 | 83 |
| INVERSIóN VIRTUAL | 2025-09-18 | 76 |
| INVERSIóN VIRTUAL | 2025-09-19 | 66 |
| INVERSIóN VIRTUAL | 2025-09-20 | 65 |
| INVERSIóN VIRTUAL | 2025-09-21 | 30 |
| INVERSIóN VIRTUAL | 2025-09-22 | 27 |
| INVERSIóN VIRTUAL | 2025-09-23 | 54 |
| INVERSIóN VIRTUAL | 2025-09-24 | 54 |
| INVERSIóN VIRTUAL | 2025-09-25 | 41 |
| INVERSIóN VIRTUAL | 2025-09-26 | 64 |
| INVERSIóN VIRTUAL | 2025-09-27 | 80 |
| INVERSIóN VIRTUAL | 2025-09-28 | 40 |
| INVERSIóN VIRTUAL | 2025-09-29 | 17 |
| INVERSIóN VIRTUAL | 2025-09-30 | 84 |
| INVERSIóN VIRTUAL | 2025-10-01 | 100 |
| INVERSIóN VIRTUAL | 2025-10-02 | 91 |
| INVERSIóN VIRTUAL | 2025-10-03 | 79 |
| INVERSIóN VIRTUAL | 2025-10-04 | 79 |
| INVERSIóN VIRTUAL | 2025-10-05 | 52 |
| INVERSIóN VIRTUAL | 2025-10-06 | 26 |
| INVERSIóN VIRTUAL | 2025-10-07 | 77 |
| INVERSIóN VIRTUAL | 2025-10-08 | 78 |
| INVERSIóN VIRTUAL | 2025-10-09 | 60 |
| INVERSIóN VIRTUAL | 2025-10-10 | 81 |
| INVERSIóN VIRTUAL | 2025-10-11 | 69 |
| INVERSIóN VIRTUAL | 2025-10-12 | 36 |
| INVERSIóN VIRTUAL | 2025-10-13 | 21 |
| INVERSIóN VIRTUAL | 2025-10-14 | 24 |
| INVERSIóN VIRTUAL | 2025-10-15 | 88 |
| INVERSIóN VIRTUAL | 2025-10-16 | 82 |
| INVERSIóN VIRTUAL | 2025-10-17 | 66 |
| INVERSIóN VIRTUAL | 2025-10-18 | 81 |
| INVERSIóN VIRTUAL | 2025-10-19 | 47 |
| INVERSIóN VIRTUAL | 2025-10-20 | 18 |
| INVERSIóN VIRTUAL | 2025-10-21 | 24 |
| INVERSIóN VIRTUAL | 2025-10-22 | 78 |
| INVERSIóN VIRTUAL | 2025-10-23 | 58 |
| INVERSIóN VIRTUAL | 2025-10-25 | 77 |
| INVERSIóN VIRTUAL | 2025-10-26 | 41 |
| INVERSIóN VIRTUAL | 2025-10-27 | 21 |
| INVERSIóN VIRTUAL | 2025-10-28 | 72 |
| INVERSIóN VIRTUAL | 2025-10-29 | 46 |
| INVERSIóN VIRTUAL | 2025-10-30 | 55 |
| INVERSIóN VIRTUAL | 2025-10-31 | 68 |
| INVERSIóN VIRTUAL | 2025-11-01 | 61 |
| INVERSIóN VIRTUAL | 2025-11-02 | 34 |
| INVERSIóN VIRTUAL | 2025-11-03 | 26 |
| INVERSIóN VIRTUAL | 2025-11-04 | 21 |
| INVERSIóN VIRTUAL | 2025-11-05 | 67 |
| INVERSIóN VIRTUAL | 2025-11-06 | 66 |
| INVERSIóN VIRTUAL | 2025-11-07 | 56 |
| INVERSIóN VIRTUAL | 2025-11-08 | 75 |
| INVERSIóN VIRTUAL | 2025-11-09 | 41 |
| INVERSIóN VIRTUAL | 2025-11-10 | 25 |
| INVERSIóN VIRTUAL | 2025-11-11 | 70 |
| INVERSIóN VIRTUAL | 2025-11-12 | 66 |
| INVERSIóN VIRTUAL | 2025-11-13 | 48 |
| INVERSIóN VIRTUAL | 2025-11-14 | 50 |
| INVERSIóN VIRTUAL | 2025-11-15 | 65 |
| INVERSIóN VIRTUAL | 2025-11-16 | 32 |
| INVERSIóN VIRTUAL | 2025-11-17 | 14 |
| INVERSIóN VIRTUAL | 2025-11-18 | 12 |
| INVERSIóN VIRTUAL | 2025-11-19 | 51 |
| INVERSIóN VIRTUAL | 2025-11-20 | 57 |
| INVERSIóN VIRTUAL | 2025-11-21 | 47 |
| INVERSIóN VIRTUAL | 2025-11-22 | 56 |
| INVERSIóN VIRTUAL | 2025-11-23 | 35 |
| INVERSIóN VIRTUAL | 2025-11-24 | 19 |
| INVERSIóN VIRTUAL | 2025-11-25 | 51 |
| INVERSIóN VIRTUAL | 2025-11-26 | 48 |
| INVERSIóN VIRTUAL | 2025-11-27 | 58 |
| INVERSIóN VIRTUAL | 2025-11-28 | 65 |
| INVERSIóN VIRTUAL | 2025-11-29 | 98 |
| INVERSIóN VIRTUAL | 2025-11-30 | 50 |
| INVERSIóN VIRTUAL | 2025-12-01 | 21 |
| INVERSIóN VIRTUAL | 2025-12-02 | 64 |
| INVERSIóN VIRTUAL | 2025-12-03 | 80 |
| INVERSIóN VIRTUAL | 2025-12-04 | 119 |
| INVERSIóN VIRTUAL | 2025-12-05 | 80 |
| INVERSIóN VIRTUAL | 2025-12-06 | 97 |
| INVERSIóN VIRTUAL | 2025-12-07 | 47 |
| INVERSIóN VIRTUAL | 2025-12-08 | 25 |
| INVERSIóN VIRTUAL | 2025-12-09 | 29 |
| INVERSIóN VIRTUAL | 2025-12-10 | 70 |
| INVERSIóN VIRTUAL | 2025-12-11 | 73 |
| INVERSIóN VIRTUAL | 2025-12-12 | 86 |
| INVERSIóN VIRTUAL | 2025-12-13 | 91 |
| INVERSIóN VIRTUAL | 2025-12-15 | 92 |
| INVERSIóN VIRTUAL | 2025-12-16 | 107 |
| INVERSIóN VIRTUAL | 2025-12-17 | 86 |
| INVERSIóN VIRTUAL | 2025-12-18 | 63 |
| INVERSIóN VIRTUAL | 2025-12-19 | 101 |
| INVERSIóN VIRTUAL | 2025-12-20 | 103 |
| INVERSIóN VIRTUAL | 2025-12-21 | 70 |
| INVERSIóN VIRTUAL | 2025-12-22 | 24 |
| INVERSIóN VIRTUAL | 2025-12-23 | 87 |
| INVERSIóN VIRTUAL | 2025-12-24 | 99 |
| INVERSIóN VIRTUAL | 2025-12-25 | 75 |
| INVERSIóN VIRTUAL | 2025-12-26 | 21 |
| INVERSIóN VIRTUAL | 2025-12-27 | 115 |
| INVERSIóN VIRTUAL | 2025-12-28 | 48 |
| INVERSIóN VIRTUAL | 2025-12-29 | 24 |
| INVERSIóN VIRTUAL | 2025-12-30 | 109 |
| INVERSIóN VIRTUAL | 2025-12-31 | 130 |
| INVERSIóN VIRTUAL | 2026-01-01 | 50 |
| INVERSIóN VIRTUAL | 2026-01-02 | 36 |
| INVERSIóN VIRTUAL | 2026-01-03 | 109 |
| INVERSIóN VIRTUAL | 2026-01-04 | 54 |
| INVERSIóN VIRTUAL | 2026-01-05 | 29 |
| INVERSIóN VIRTUAL | 2026-01-06 | 114 |
| INVERSIóN VIRTUAL | 2026-01-07 | 93 |
| INVERSIóN VIRTUAL | 2026-01-08 | 110 |
| INVERSIóN VIRTUAL | 2026-01-09 | 108 |
| INVERSIóN VIRTUAL | 2026-01-10 | 95 |
| INVERSIóN VIRTUAL | 2026-01-11 | 65 |
| INVERSIóN VIRTUAL | 2026-01-12 | 22 |
| INVERSIóN VIRTUAL | 2026-01-13 | 29 |
| INVERSIóN VIRTUAL | 2026-01-14 | 73 |
| INVERSIóN VIRTUAL | 2026-01-15 | 108 |
| INVERSIóN VIRTUAL | 2026-01-16 | 97 |
| INVERSIóN VIRTUAL | 2026-01-17 | 102 |
| INVERSIóN VIRTUAL | 2026-01-18 | 40 |
| INVERSIóN VIRTUAL | 2026-01-19 | 29 |
| INVERSIóN VIRTUAL | 2026-01-20 | 77 |
| INVERSIóN VIRTUAL | 2026-01-21 | 86 |
| INVERSIóN VIRTUAL | 2026-01-22 | 91 |
| INVERSIóN VIRTUAL | 2026-01-23 | 86 |
| INVERSIóN VIRTUAL | 2026-01-24 | 62 |
| INVERSIóN VIRTUAL | 2026-01-25 | 57 |
| INVERSIóN VIRTUAL | 2026-01-26 | 26 |
| INVERSIóN VIRTUAL | 2026-01-27 | 90 |
| INVERSIóN VIRTUAL | 2026-01-28 | 95 |
| INVERSIóN VIRTUAL | 2026-01-29 | 96 |
| INVERSIóN VIRTUAL | 2026-01-30 | 81 |
| INVERSIóN VIRTUAL | 2026-01-31 | 102 |
| INVERSIóN VIRTUAL | 2026-02-01 | 70 |
| INVERSIóN VIRTUAL | 2026-02-02 | 48 |
| INVERSIóN VIRTUAL | 2026-02-03 | 126 |
| INVERSIóN VIRTUAL | 2026-02-04 | 85 |
| INVERSIóN VIRTUAL | 2026-02-05 | 93 |
| INVERSIóN VIRTUAL | 2026-02-06 | 67 |
| INVERSIóN VIRTUAL | 2026-02-07 | 101 |
| INVERSIóN VIRTUAL | 2026-02-08 | 46 |
| INVERSIóN VIRTUAL | 2026-02-09 | 30 |
| INVERSIóN VIRTUAL | 2026-02-10 | 96 |
| INVERSIóN VIRTUAL | 2026-02-11 | 81 |
| INVERSIóN VIRTUAL | 2026-02-12 | 66 |
| INVERSIóN VIRTUAL | 2026-02-13 | 68 |
| INVERSIóN VIRTUAL | 2026-02-14 | 76 |
| INVERSIóN VIRTUAL | 2026-02-15 | 44 |
| INVERSIóN VIRTUAL | 2026-02-16 | 37 |
| INVERSIóN VIRTUAL | 2026-02-17 | 60 |
| INVERSIóN VIRTUAL | 2026-02-18 | 63 |
| INVERSIóN VIRTUAL | 2026-02-19 | 58 |
| INVERSIóN VIRTUAL | 2026-02-20 | 86 |
| INVERSIóN VIRTUAL | 2026-02-21 | 73 |
| INVERSIóN VIRTUAL | 2026-02-23 | 47 |
| INVERSIóN VIRTUAL | 2026-02-25 | 86 |
| INVERSIóN VIRTUAL | 2026-02-26 | 114 |
| INVERSIóN VIRTUAL | 2026-02-27 | 51 |
| INVERSIóN VIRTUAL | 2026-02-28 | 126 |
| INVERSIóN VIRTUAL | 2026-03-01 | 77 |
| INVERSIóN VIRTUAL | 2026-03-02 | 42 |
| INVERSIóN VIRTUAL | 2026-03-03 | 102 |
| INVERSIóN VIRTUAL | 2026-03-04 | 105 |
| INVERSIóN VIRTUAL | 2026-03-05 | 97 |
| INVERSIóN VIRTUAL | 2026-03-06 | 83 |
| INVERSIóN VIRTUAL | 2026-03-07 | 88 |
| INVERSIóN VIRTUAL | 2026-03-08 | 47 |
| INVERSIóN VIRTUAL | 2026-03-09 | 30 |
| INVERSIóN VIRTUAL | 2026-03-10 | 77 |
| INVERSIóN VIRTUAL | 2026-03-11 | 68 |
| INVERSIóN VIRTUAL | 2026-03-12 | 80 |
| INVERSIóN VIRTUAL | 2026-03-13 | 70 |
| INVERSIóN VIRTUAL | 2026-03-14 | 95 |
| INVERSIóN VIRTUAL | 2026-03-15 | 45 |
| INVERSIóN VIRTUAL | 2026-03-16 | 21 |
| INVERSIóN VIRTUAL | 2026-03-17 | 107 |
| INVERSIóN VIRTUAL | 2026-03-18 | 69 |
| INVERSIóN VIRTUAL | 2026-03-19 | 64 |
| INVERSIóN VIRTUAL | 2026-03-20 | 68 |
| INVERSIóN VIRTUAL | 2026-03-21 | 65 |
| INVERSIóN VIRTUAL | 2026-03-22 | 47 |
| INVERSIóN VIRTUAL | 2026-03-23 | 17 |
| INVERSIóN VIRTUAL | 2026-03-24 | 24 |
| INVERSIóN VIRTUAL | 2026-03-25 | 83 |
| INVERSIóN VIRTUAL | 2026-03-26 | 72 |
| INVERSIóN VIRTUAL | 2026-03-27 | 70 |
| INVERSIóN VIRTUAL | 2026-03-28 | 234 |
| INVERSIóN VIRTUAL | 2026-03-29 | 71 |
| INVERSIóN VIRTUAL | 2026-03-30 | 38 |
| INVERSIóN VIRTUAL | 2026-03-31 | 128 |
| INVERSIóN VIRTUAL | 2026-04-01 | 106 |
| INVERSIóN VIRTUAL | 2026-04-02 | 133 |
| INVERSIóN VIRTUAL | 2026-04-03 | 52 |
| INVERSIóN VIRTUAL | 2026-04-04 | 35 |
| INVERSIóN VIRTUAL | 2026-04-05 | 41 |
| INVERSIóN VIRTUAL | 2026-04-06 | 35 |
| INVERSIóN VIRTUAL | 2026-04-07 | 117 |
| INVERSIóN VIRTUAL | 2026-04-08 | 101 |
| INVERSIóN VIRTUAL | 2026-04-09 | 104 |
| INVERSIóN VIRTUAL | 2026-04-10 | 96 |
| INVERSIóN VIRTUAL | 2026-04-11 | 90 |
| INVERSIóN VIRTUAL | 2026-04-12 | 54 |
| INVERSIóN VIRTUAL | 2026-04-13 | 21 |
| INVERSIóN VIRTUAL | 2026-04-14 | 83 |
| INVERSIóN VIRTUAL | 2026-04-15 | 65 |
| INVERSIóN VIRTUAL | 2026-04-16 | 69 |
| INVERSIóN VIRTUAL | 2026-04-17 | 84 |
| INVERSIóN VIRTUAL | 2026-04-18 | 73 |
| INVERSIóN VIRTUAL | 2026-04-19 | 39 |
| INVERSIóN VIRTUAL | 2026-04-20 | 22 |
| INVERSIóN VIRTUAL | 2026-04-21 | 81 |
| INVERSIóN VIRTUAL | 2026-04-22 | 67 |
| INVERSIóN VIRTUAL | 2026-04-23 | 53 |
| INVERSIóN VIRTUAL | 2026-04-24 | 50 |
| INVERSIóN VIRTUAL | 2026-04-25 | 65 |
| INVERSIóN VIRTUAL | 2026-04-26 | 39 |
| INVERSIóN VIRTUAL | 2026-04-27 | 28 |
| INVERSIóN VIRTUAL | 2026-04-28 | 58 |
| INVERSIóN VIRTUAL | 2026-04-29 | 66 |
| INVERSIóN VIRTUAL | 2026-04-30 | 65 |
| INVERSIóN VIRTUAL | 2026-05-01 | 99 |
| INVERSIóN VIRTUAL | 2026-05-02 | 58 |
| INVERSIóN VIRTUAL | 2026-05-03 | 43 |
| INVERSIóN VIRTUAL | 2026-05-04 | 19 |
| INVERSIóN VIRTUAL | 2026-05-05 | 74 |
| INVERSIóN VIRTUAL | 2026-05-06 | 85 |
| INVERSIóN VIRTUAL | 2026-05-07 | 78 |
| INVERSIóN VIRTUAL | 2026-05-08 | 61 |
| INVERSIóN VIRTUAL | 2026-05-09 | 64 |
| INVERSIóN VIRTUAL | 2026-05-10 | 28 |
| INVERSIóN VIRTUAL | 2026-05-11 | 18 |
| INVERSIóN VIRTUAL | 2026-05-12 | 83 |
| INVERSIóN VIRTUAL | 2026-05-13 | 52 |
| INVERSIóN VIRTUAL | 2026-05-14 | 61 |
| INVERSIóN VIRTUAL | 2026-05-15 | 74 |
| INVERSIóN VIRTUAL | 2026-05-16 | 77 |
| INVERSIóN VIRTUAL | 2026-05-17 | 30 |
| INVERSIóN VIRTUAL | 2026-05-18 | 16 |
| INVERSIóN VIRTUAL | 2026-05-19 | 17 |
| INVERSIóN VIRTUAL | 2026-05-20 | 66 |
| INVERSIóN VIRTUAL | 2026-05-21 | 55 |
| INVERSIóN VIRTUAL | 2026-05-23 | 97 |
| INVERSIóN VIRTUAL | 2026-05-24 | 25 |
| INVERSIóN VIRTUAL | 2026-05-25 | 13 |
| INVERSIóN VIRTUAL | 2026-05-26 | 45 |
| INVERSIóN VIRTUAL | 2026-05-27 | 60 |
| INVERSIóN VIRTUAL | 2026-05-28 | 59 |
| INVERSIóN VIRTUAL | 2026-05-29 | 61 |
| INVERSIóN VIRTUAL | 2026-05-30 | 73 |
| INVERSIóN VIRTUAL | 2026-05-31 | 42 |
| INVERSIóN VIRTUAL | 2026-06-01 | 26 |
| INVERSIóN VIRTUAL | 2026-06-02 | 72 |
| INVERSIóN VIRTUAL | 2026-06-03 | 65 |
| INVERSIóN VIRTUAL | 2026-06-04 | 77 |
| INVERSIóN VIRTUAL | 2026-06-05 | 70 |
| INVERSIóN VIRTUAL | 2026-06-06 | 83 |
| INVERSIóN VIRTUAL | 2026-06-07 | 40 |
| INVERSIóN VIRTUAL | 2026-06-08 | 21 |
| INVERSIóN VIRTUAL | 2026-06-09 | 19 |
| INVERSIóN VIRTUAL | 2026-06-10 | 56 |
| INVERSIóN VIRTUAL | 2026-06-11 | 59 |
| INVERSIóN VIRTUAL | 2026-06-12 | 62 |
| INVERSIóN VIRTUAL | 2026-06-13 | 65 |
| INVERSIóN VIRTUAL | 2026-06-14 | 57 |
| INVERSIóN VIRTUAL | 2026-06-15 | 24 |
| INVERSIóN VIRTUAL | 2026-06-16 | 26 |
| INVERSIóN VIRTUAL | 2026-06-17 | 72 |
| INVERSIóN VIRTUAL | 2026-06-18 | 54 |
| INVERSIóN VIRTUAL | 2026-06-19 | 73 |
| INVERSIóN VIRTUAL | 2026-06-20 | 51 |
| INVERSIóN VIRTUAL | 2026-06-21 | 32 |
| INVERSIóN VIRTUAL | 2026-06-22 | 14 |
| INVERSIóN VIRTUAL | 2026-06-23 | 48 |
| INVERSIóN VIRTUAL | 2026-06-24 | 53 |
| INVERSIóN VIRTUAL | 2026-06-25 | 45 |
| INVERSIóN VIRTUAL | 2026-06-26 | 61 |
| INVERSIóN VIRTUAL | 2026-06-27 | 79 |
| INVERSIóN VIRTUAL | 2026-06-28 | 36 |
| INVERSIóN VIRTUAL | 2026-06-29 | 13 |
| INVERSIóN VIRTUAL | 2026-06-30 | 20 |

### Tabla `invesbot`

#### Esquema

| columna | tipo_sqlite | not_null | llave_primaria |
| --- | --- | --- | --- |
| fecha | TEXT | 0 | 0 |
| numero_id | INTEGER | 0 | 0 |
| producto | TEXT | 0 | 0 |
| saldo | REAL | 0 | 0 |

#### Compatibilidad de tipos

| tabla | columna | tipo_sqlite | tipos_compatibles | estado |
| --- | --- | --- | --- | --- |
| invesbot | fecha | TEXT | TEXT, DATE, DATETIME | OK |
| invesbot | numero_id | INTEGER | INTEGER | OK |
| invesbot | producto | TEXT | TEXT | OK |
| invesbot | saldo | REAL | REAL, INTEGER, NUMERIC | OK |

#### Resumen

| registros | clientes | productos | fechas | fecha_minima | fecha_maxima | fechas_nulas | fechas_invalidas | ids_nulos | productos_nulos | saldos_nulos | saldos_negativos | saldos_cero | saldos_positivos | saldo_minimo | saldo_promedio | saldo_maximo | duplicados_combinaciones_duplicadas | duplicados_registros_excedentes | duplicados_maximo_por_combinacion | duplicados_claves_con_saldos_distintos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000000 | 5214 | 1 | 389 | 2025-06-01 | 2026-06-24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1000000 | 0.94 | 18787725.183728103 | 1347566620.54 | 0 | 0 | 0 | 0 |

#### Productos o variables financieras

| producto | registros | clientes | fechas | fecha_minima | fecha_maxima | negativos | ceros | positivos | saldo_minimo | saldo_promedio | saldo_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVESBOT | 1000000 | 5214 | 389 | 2025-06-01 | 2026-06-24 | 0 | 0 | 1000000 | 0.94 | 18787725.183728103 | 1347566620.54 |

#### Cobertura temporal mensual

| mes | fechas_distintas | registros | clientes |
| --- | --- | --- | --- |
| 2025-06 | 30 | 48435 | 2031 |
| 2025-07 | 31 | 55462 | 2300 |
| 2025-08 | 31 | 59096 | 2391 |
| 2025-09 | 30 | 60345 | 2554 |
| 2025-10 | 31 | 65419 | 2657 |
| 2025-11 | 30 | 66430 | 2910 |
| 2025-12 | 31 | 76807 | 3150 |
| 2026-01 | 31 | 83762 | 3604 |
| 2026-02 | 28 | 84662 | 3845 |
| 2026-03 | 31 | 99150 | 4182 |
| 2026-04 | 30 | 102018 | 4319 |
| 2026-05 | 31 | 110209 | 4459 |
| 2026-06 | 24 | 88205 | 4577 |

#### Primeras apariciones observadas por producto y fecha

Estas apariciones son descriptivas y no se interpretan todavía como aperturas reales.

| producto | primera_fecha | clientes |
| --- | --- | --- |
| INVESBOT | 2025-06-01 | 1529 |
| INVESBOT | 2025-06-02 | 305 |
| INVESBOT | 2025-06-03 | 56 |
| INVESBOT | 2025-06-04 | 23 |
| INVESBOT | 2025-06-05 | 6 |
| INVESBOT | 2025-06-06 | 5 |
| INVESBOT | 2025-06-09 | 13 |
| INVESBOT | 2025-06-10 | 10 |
| INVESBOT | 2025-06-11 | 3 |
| INVESBOT | 2025-06-12 | 11 |
| INVESBOT | 2025-06-13 | 3 |
| INVESBOT | 2025-06-14 | 10 |
| INVESBOT | 2025-06-15 | 2 |
| INVESBOT | 2025-06-16 | 7 |
| INVESBOT | 2025-06-17 | 8 |
| INVESBOT | 2025-06-18 | 7 |
| INVESBOT | 2025-06-19 | 8 |
| INVESBOT | 2025-06-20 | 2 |
| INVESBOT | 2025-06-21 | 1 |
| INVESBOT | 2025-06-24 | 8 |
| INVESBOT | 2025-06-25 | 7 |
| INVESBOT | 2025-06-27 | 6 |
| INVESBOT | 2025-06-28 | 1 |
| INVESBOT | 2025-07-01 | 44 |
| INVESBOT | 2025-07-02 | 15 |
| INVESBOT | 2025-07-03 | 31 |
| INVESBOT | 2025-07-04 | 18 |
| INVESBOT | 2025-07-06 | 1 |
| INVESBOT | 2025-07-07 | 10 |
| INVESBOT | 2025-07-08 | 22 |
| INVESBOT | 2025-07-09 | 12 |
| INVESBOT | 2025-07-10 | 10 |
| INVESBOT | 2025-07-11 | 1 |
| INVESBOT | 2025-07-13 | 7 |
| INVESBOT | 2025-07-14 | 8 |
| INVESBOT | 2025-07-15 | 12 |
| INVESBOT | 2025-07-16 | 9 |
| INVESBOT | 2025-07-17 | 14 |
| INVESBOT | 2025-07-18 | 12 |
| INVESBOT | 2025-07-21 | 13 |
| INVESBOT | 2025-07-22 | 9 |
| INVESBOT | 2025-07-23 | 5 |
| INVESBOT | 2025-07-24 | 7 |
| INVESBOT | 2025-07-25 | 2 |
| INVESBOT | 2025-07-28 | 14 |
| INVESBOT | 2025-07-29 | 12 |
| INVESBOT | 2025-07-30 | 7 |
| INVESBOT | 2025-07-31 | 2 |
| INVESBOT | 2025-08-01 | 3 |
| INVESBOT | 2025-08-02 | 2 |
| INVESBOT | 2025-08-04 | 20 |
| INVESBOT | 2025-08-05 | 13 |
| INVESBOT | 2025-08-06 | 2 |
| INVESBOT | 2025-08-08 | 3 |
| INVESBOT | 2025-08-09 | 3 |
| INVESBOT | 2025-08-10 | 1 |
| INVESBOT | 2025-08-11 | 9 |
| INVESBOT | 2025-08-12 | 4 |
| INVESBOT | 2025-08-13 | 7 |
| INVESBOT | 2025-08-14 | 1 |
| INVESBOT | 2025-08-15 | 1 |
| INVESBOT | 2025-08-19 | 1 |
| INVESBOT | 2025-08-20 | 7 |
| INVESBOT | 2025-08-21 | 3 |
| INVESBOT | 2025-08-22 | 4 |
| INVESBOT | 2025-08-25 | 7 |
| INVESBOT | 2025-08-26 | 2 |
| INVESBOT | 2025-08-27 | 6 |
| INVESBOT | 2025-08-28 | 3 |
| INVESBOT | 2025-08-29 | 22 |
| INVESBOT | 2025-08-30 | 2 |
| INVESBOT | 2025-08-31 | 2 |
| INVESBOT | 2025-09-01 | 16 |
| INVESBOT | 2025-09-02 | 12 |
| INVESBOT | 2025-09-03 | 10 |
| INVESBOT | 2025-09-04 | 7 |
| INVESBOT | 2025-09-05 | 9 |
| INVESBOT | 2025-09-06 | 1 |
| INVESBOT | 2025-09-08 | 6 |
| INVESBOT | 2025-09-09 | 4 |
| INVESBOT | 2025-09-10 | 5 |
| INVESBOT | 2025-09-11 | 10 |
| INVESBOT | 2025-09-12 | 6 |
| INVESBOT | 2025-09-14 | 1 |
| INVESBOT | 2025-09-15 | 9 |
| INVESBOT | 2025-09-16 | 8 |
| INVESBOT | 2025-09-17 | 11 |
| INVESBOT | 2025-09-18 | 7 |
| INVESBOT | 2025-09-19 | 9 |
| INVESBOT | 2025-09-22 | 7 |
| INVESBOT | 2025-09-23 | 4 |
| INVESBOT | 2025-09-24 | 7 |
| INVESBOT | 2025-09-25 | 10 |
| INVESBOT | 2025-09-26 | 10 |
| INVESBOT | 2025-09-29 | 11 |
| INVESBOT | 2025-09-30 | 10 |
| INVESBOT | 2025-10-01 | 12 |
| INVESBOT | 2025-10-02 | 7 |
| INVESBOT | 2025-10-03 | 8 |
| INVESBOT | 2025-10-04 | 1 |
| INVESBOT | 2025-10-06 | 7 |
| INVESBOT | 2025-10-07 | 4 |
| INVESBOT | 2025-10-08 | 5 |
| INVESBOT | 2025-10-09 | 7 |
| INVESBOT | 2025-10-10 | 7 |
| INVESBOT | 2025-10-14 | 2 |
| INVESBOT | 2025-10-15 | 1 |
| INVESBOT | 2025-10-16 | 5 |
| INVESBOT | 2025-10-17 | 11 |
| INVESBOT | 2025-10-18 | 1 |
| INVESBOT | 2025-10-21 | 3 |
| INVESBOT | 2025-10-22 | 9 |
| INVESBOT | 2025-10-23 | 2 |
| INVESBOT | 2025-10-27 | 16 |
| INVESBOT | 2025-10-28 | 6 |
| INVESBOT | 2025-10-29 | 10 |
| INVESBOT | 2025-10-30 | 10 |
| INVESBOT | 2025-10-31 | 12 |
| INVESBOT | 2025-11-01 | 1 |
| INVESBOT | 2025-11-04 | 6 |
| INVESBOT | 2025-11-05 | 11 |
| INVESBOT | 2025-11-06 | 10 |
| INVESBOT | 2025-11-07 | 4 |
| INVESBOT | 2025-11-08 | 1 |
| INVESBOT | 2025-11-10 | 4 |
| INVESBOT | 2025-11-11 | 12 |
| INVESBOT | 2025-11-12 | 10 |
| INVESBOT | 2025-11-13 | 14 |
| INVESBOT | 2025-11-14 | 11 |
| INVESBOT | 2025-11-15 | 1 |
| INVESBOT | 2025-11-16 | 1 |
| INVESBOT | 2025-11-18 | 9 |
| INVESBOT | 2025-11-19 | 2 |
| INVESBOT | 2025-11-20 | 4 |
| INVESBOT | 2025-11-24 | 2 |
| INVESBOT | 2025-11-25 | 38 |
| INVESBOT | 2025-11-26 | 45 |
| INVESBOT | 2025-11-27 | 69 |
| INVESBOT | 2025-11-28 | 26 |
| INVESBOT | 2025-11-29 | 8 |
| INVESBOT | 2025-11-30 | 1 |
| INVESBOT | 2025-12-01 | 8 |
| INVESBOT | 2025-12-02 | 11 |
| INVESBOT | 2025-12-03 | 15 |
| INVESBOT | 2025-12-04 | 34 |
| INVESBOT | 2025-12-05 | 16 |
| INVESBOT | 2025-12-06 | 1 |
| INVESBOT | 2025-12-07 | 1 |
| INVESBOT | 2025-12-09 | 25 |
| INVESBOT | 2025-12-10 | 14 |
| INVESBOT | 2025-12-11 | 14 |
| INVESBOT | 2025-12-12 | 14 |
| INVESBOT | 2025-12-13 | 2 |
| INVESBOT | 2025-12-15 | 11 |
| INVESBOT | 2025-12-16 | 14 |
| INVESBOT | 2025-12-17 | 11 |
| INVESBOT | 2025-12-18 | 10 |
| INVESBOT | 2025-12-19 | 11 |
| INVESBOT | 2025-12-20 | 2 |
| INVESBOT | 2025-12-21 | 1 |
| INVESBOT | 2025-12-22 | 12 |
| INVESBOT | 2025-12-24 | 5 |
| INVESBOT | 2025-12-25 | 3 |
| INVESBOT | 2025-12-26 | 14 |
| INVESBOT | 2025-12-27 | 3 |
| INVESBOT | 2025-12-29 | 6 |
| INVESBOT | 2025-12-30 | 18 |
| INVESBOT | 2025-12-31 | 6 |
| INVESBOT | 2026-01-02 | 14 |
| INVESBOT | 2026-01-03 | 1 |
| INVESBOT | 2026-01-05 | 11 |
| INVESBOT | 2026-01-06 | 18 |
| INVESBOT | 2026-01-07 | 15 |
| INVESBOT | 2026-01-08 | 15 |
| INVESBOT | 2026-01-09 | 8 |
| INVESBOT | 2026-01-10 | 3 |
| INVESBOT | 2026-01-13 | 5 |
| INVESBOT | 2026-01-14 | 17 |
| INVESBOT | 2026-01-15 | 20 |
| INVESBOT | 2026-01-16 | 18 |
| INVESBOT | 2026-01-17 | 1 |
| INVESBOT | 2026-01-19 | 88 |
| INVESBOT | 2026-01-20 | 57 |
| INVESBOT | 2026-01-21 | 29 |
| INVESBOT | 2026-01-22 | 27 |
| INVESBOT | 2026-01-23 | 20 |
| INVESBOT | 2026-01-24 | 6 |
| INVESBOT | 2026-01-26 | 27 |
| INVESBOT | 2026-01-27 | 20 |
| INVESBOT | 2026-01-28 | 23 |
| INVESBOT | 2026-01-29 | 23 |
| INVESBOT | 2026-01-30 | 22 |
| INVESBOT | 2026-01-31 | 2 |
| INVESBOT | 2026-02-01 | 2 |
| INVESBOT | 2026-02-02 | 36 |
| INVESBOT | 2026-02-03 | 25 |
| INVESBOT | 2026-02-04 | 19 |
| INVESBOT | 2026-02-05 | 10 |
| INVESBOT | 2026-02-06 | 24 |
| INVESBOT | 2026-02-07 | 8 |
| INVESBOT | 2026-02-08 | 1 |
| INVESBOT | 2026-02-09 | 9 |
| INVESBOT | 2026-02-10 | 11 |
| INVESBOT | 2026-02-11 | 12 |
| INVESBOT | 2026-02-12 | 19 |
| INVESBOT | 2026-02-13 | 15 |
| INVESBOT | 2026-02-14 | 3 |
| INVESBOT | 2026-02-15 | 1 |
| INVESBOT | 2026-02-16 | 9 |
| INVESBOT | 2026-02-17 | 7 |
| INVESBOT | 2026-02-18 | 14 |
| INVESBOT | 2026-02-19 | 13 |
| INVESBOT | 2026-02-20 | 6 |
| INVESBOT | 2026-02-21 | 4 |
| INVESBOT | 2026-02-24 | 1 |
| INVESBOT | 2026-02-25 | 14 |
| INVESBOT | 2026-02-26 | 10 |
| INVESBOT | 2026-02-27 | 23 |
| INVESBOT | 2026-02-28 | 2 |
| INVESBOT | 2026-03-02 | 17 |
| INVESBOT | 2026-03-03 | 16 |
| INVESBOT | 2026-03-04 | 10 |
| INVESBOT | 2026-03-05 | 9 |
| INVESBOT | 2026-03-06 | 14 |
| INVESBOT | 2026-03-07 | 3 |
| INVESBOT | 2026-03-09 | 13 |
| INVESBOT | 2026-03-10 | 7 |
| INVESBOT | 2026-03-11 | 5 |
| INVESBOT | 2026-03-12 | 4 |
| INVESBOT | 2026-03-13 | 8 |
| INVESBOT | 2026-03-14 | 1 |
| INVESBOT | 2026-03-15 | 1 |
| INVESBOT | 2026-03-16 | 7 |
| INVESBOT | 2026-03-17 | 6 |
| INVESBOT | 2026-03-18 | 21 |
| INVESBOT | 2026-03-19 | 40 |
| INVESBOT | 2026-03-20 | 19 |
| INVESBOT | 2026-03-21 | 10 |
| INVESBOT | 2026-03-25 | 23 |
| INVESBOT | 2026-03-26 | 52 |
| INVESBOT | 2026-03-27 | 63 |
| INVESBOT | 2026-03-28 | 2 |
| INVESBOT | 2026-03-29 | 6 |
| INVESBOT | 2026-03-30 | 25 |
| INVESBOT | 2026-03-31 | 20 |
| INVESBOT | 2026-04-01 | 9 |
| INVESBOT | 2026-04-02 | 4 |
| INVESBOT | 2026-04-03 | 1 |
| INVESBOT | 2026-04-06 | 14 |
| INVESBOT | 2026-04-07 | 7 |
| INVESBOT | 2026-04-08 | 13 |
| INVESBOT | 2026-04-09 | 15 |
| INVESBOT | 2026-04-10 | 9 |
| INVESBOT | 2026-04-11 | 3 |
| INVESBOT | 2026-04-13 | 6 |
| INVESBOT | 2026-04-14 | 15 |
| INVESBOT | 2026-04-15 | 10 |
| INVESBOT | 2026-04-16 | 11 |
| INVESBOT | 2026-04-17 | 14 |
| INVESBOT | 2026-04-18 | 1 |
| INVESBOT | 2026-04-20 | 3 |
| INVESBOT | 2026-04-21 | 5 |
| INVESBOT | 2026-04-22 | 8 |
| INVESBOT | 2026-04-23 | 16 |
| INVESBOT | 2026-04-24 | 15 |
| INVESBOT | 2026-04-25 | 5 |
| INVESBOT | 2026-04-27 | 15 |
| INVESBOT | 2026-04-28 | 14 |
| INVESBOT | 2026-04-29 | 10 |
| INVESBOT | 2026-04-30 | 18 |
| INVESBOT | 2026-05-01 | 1 |
| INVESBOT | 2026-05-04 | 5 |
| INVESBOT | 2026-05-05 | 26 |
| INVESBOT | 2026-05-06 | 13 |
| INVESBOT | 2026-05-07 | 24 |
| INVESBOT | 2026-05-08 | 8 |
| INVESBOT | 2026-05-09 | 2 |
| INVESBOT | 2026-05-11 | 19 |
| INVESBOT | 2026-05-12 | 14 |
| INVESBOT | 2026-05-13 | 8 |
| INVESBOT | 2026-05-14 | 16 |
| INVESBOT | 2026-05-15 | 12 |
| INVESBOT | 2026-05-16 | 2 |
| INVESBOT | 2026-05-18 | 1 |
| INVESBOT | 2026-05-19 | 18 |
| INVESBOT | 2026-05-20 | 13 |
| INVESBOT | 2026-05-21 | 9 |
| INVESBOT | 2026-05-22 | 15 |
| INVESBOT | 2026-05-25 | 5 |
| INVESBOT | 2026-05-26 | 8 |
| INVESBOT | 2026-05-27 | 8 |
| INVESBOT | 2026-05-28 | 4 |
| INVESBOT | 2026-05-29 | 7 |
| INVESBOT | 2026-05-31 | 1 |
| INVESBOT | 2026-06-01 | 10 |
| INVESBOT | 2026-06-02 | 17 |
| INVESBOT | 2026-06-03 | 15 |
| INVESBOT | 2026-06-04 | 13 |
| INVESBOT | 2026-06-05 | 9 |
| INVESBOT | 2026-06-06 | 1 |
| INVESBOT | 2026-06-09 | 4 |
| INVESBOT | 2026-06-10 | 2 |
| INVESBOT | 2026-06-11 | 23 |
| INVESBOT | 2026-06-12 | 9 |
| INVESBOT | 2026-06-13 | 3 |
| INVESBOT | 2026-06-14 | 2 |
| INVESBOT | 2026-06-16 | 16 |
| INVESBOT | 2026-06-17 | 9 |
| INVESBOT | 2026-06-18 | 6 |
| INVESBOT | 2026-06-19 | 7 |
| INVESBOT | 2026-06-22 | 9 |
| INVESBOT | 2026-06-23 | 16 |
| INVESBOT | 2026-06-24 | 9 |

### Cobertura frente a la maestra de clientes

| tabla | clientes_fuente | clientes_maestra | clientes_coincidentes | clientes_fuera_maestra | clientes_maestra_sin_fuente | porcentaje_maestra_con_fuente | porcentaje_fuente_en_maestra |
| --- | --- | --- | --- | --- | --- | --- | --- |
| estimador_ing | 745792 | 860223 | 745792 | 0 | 114431 | 86.7 | 100.0 |
| crean_aho_cte | 475719 | 860223 | 475719 | 0 | 384504 | 55.3 | 100.0 |
| crean_bolsillos | 260714 | 860223 | 260714 | 0 | 599509 | 30.31 | 100.0 |
| crean_fiducuenta | 181021 | 860223 | 181021 | 0 | 679202 | 21.04 | 100.0 |
| crean_inv_virtual_cdt | 84104 | 860223 | 84104 | 0 | 776119 | 9.78 | 100.0 |
| invesbot | 5214 | 860223 | 5214 | 0 | 855009 | 0.61 | 100.0 |

### Comparación con la auditoría exploratoria inicial

La referencia corresponde a `legacy/auditoria_crean.md`. Los valores se recalculan desde las bases actuales.

| tabla | metrica | referencia_legacy | recalculado | diferencia | estado |
| --- | --- | --- | --- | --- | --- |
| clientes | registros | 860231 | 860231 | 0 | COINCIDE |
| clientes | clientes | 860223 | 860223 | 0 | COINCIDE |
| estimador_ing | registros | 745792 | 745792 | 0 | COINCIDE |
| estimador_ing | clientes | 745792 | 745792 | 0 | COINCIDE |
| crean_aho_cte | registros | 1000000 | 1000000 | 0 | COINCIDE |
| crean_aho_cte | clientes | 475719 | 475719 | 0 | COINCIDE |
| crean_bolsillos | registros | 1000000 | 1000000 | 0 | COINCIDE |
| crean_bolsillos | clientes | 260714 | 260714 | 0 | COINCIDE |
| crean_fiducuenta | registros | 1000000 | 1000000 | 0 | COINCIDE |
| crean_fiducuenta | clientes | 181021 | 181021 | 0 | COINCIDE |
| crean_inv_virtual_cdt | registros | 994177 | 994177 | 0 | COINCIDE |
| crean_inv_virtual_cdt | clientes | 84104 | 84104 | 0 | COINCIDE |
| invesbot | registros | 1000000 | 1000000 | 0 | COINCIDE |
| invesbot | clientes | 5214 | 5214 | 0 | COINCIDE |

### Interpretación y asuntos pendientes

- Las primeras apariciones son evidencia descriptiva, no aperturas confirmadas.
- Los saldos negativos se reportan sin corregir. En cuenta corriente pueden representar sobregiros.
- Los saldos cero se distinguen de la ausencia de registros.
- La resolución de duplicados y la agregación mensual pertenecen a la Etapa 2.
- Cualquier diferencia frente a la auditoría inicial debe revisarse contra la versión exacta de las bases.
<!-- FIN:AUDITORIA_REPRODUCIBLE -->


