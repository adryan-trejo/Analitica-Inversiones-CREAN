
# Analítica de Inversiones CREAN

Solución analítica para identificar clientes con mayor probabilidad de adoptar la nueva App de inversiones de CREAN y estimar el saldo potencial.

## Requisitos

- Python 3.9.12

> La solución fue desarrollada y probada en Windows. Los comandos de esta guía
> utilizan la estructura de un entorno virtual de Windows (`venv/Scripts/python.exe`).
> En Linux o macOS debe utilizarse el ejecutable equivalente, normalmente
> `venv/bin/python`; estos sistemas operativos no fueron validados.

## Datos de entrada

Las siete bases SQLite originales deben ubicarse en data/raw/:

```text
data/raw/clientes.db
data/raw/estimador_ing.db
data/raw/crean_aho_cte.db
data/raw/crean_bolsillos.db
data/raw/crean_fiducuenta.db
data/raw/crean_inv_virtual_cdt.db
data/raw/invesbot.db
```

## Creación del entorno

```powershell
py -3.9 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución del pipeline

### 1) Inventario de fuentes

```powershell
./venv/Scripts/python.exe run_pipeline.py --step inventario
```

### 2) Auditoría reproducible

```powershell
./venv/Scripts/python.exe run_pipeline.py --step auditoria
```

### 3) Capa mensual y proxy de adopción

```powershell
./venv/Scripts/python.exe run_pipeline.py --step mensual
```

### 4) Dataset de modelado

```powershell
./venv/Scripts/python.exe run_pipeline.py --step dataset_modelado
```

### 5) Modelo de adopción

```powershell
./venv/Scripts/python.exe run_pipeline.py --step modelo_adopcion
```

### 6) Scoring, segmentos y escenarios

```powershell
./venv/Scripts/python.exe run_pipeline.py --step scoring
```

## Pruebas

```powershell
./venv/Scripts/python.exe -m pytest -v
```

## Tablero Streamlit

El tablero consume únicamente resultados precomputados ya generados por el pipeline y no entrena ni recalcula modelos al iniciar. Requiere haber ejecutado los pasos anteriores.

```powershell
./venv/Scripts/python.exe run_dashboard.py
# o directamente
./venv/Scripts/python.exe -m streamlit run app/app.py
```

### Vistas del tablero

1. Resumen ejecutivo con clientes elegibles, adopciones esperadas, saldo esperado total y oportunidad por escenario.
2. Priorización con filtros por segmento y nivel de confianza, matriz de probabilidad vs. saldo potencial y descarga en CSV.
3. Modelo y calidad con métricas temporales, tasa por decil, importancia de variables y limitaciones principales.

## Estructura del repositorio

```text
app/
  app.py                Tablero Streamlit
artifacts/
  metadata/modelos.json Metadata del modelo entrenado
  models/modelo_adopcion.cbm Modelo CatBoost persistido
data/
  raw/                  Bases SQLite originales (no se modifican)
  interim/              Datos temporales regenerables
  processed/            Datos procesados reutilizables por etapa
outputs/
  scoring_clientes.parquet
  resumen_oportunidad.csv
docs/
  reporte_validacion.md
  reporte_analitico.md
src/
  config.py
  data/
  features/
  models/
  reporting/
tests/
run_pipeline.py
run_dashboard.py
config.yaml
requirements.txt
```

## Resultados principales del proyecto

- Auditoría reproducible y validación de fuentes en docs/reporte_validacion.md.
- Capa mensual y proxy de adopción digital en docs/reporte_analitico.md
- Dataset de modelado con controles de fuga temporal.
- Modelo de adopción con baseline y CatBoost, acompañado de métricas temporales.
- Scoring de clientes con probabilidad de adopción, saldo potencial condicional y escenarios comerciales.

## Limitaciones

- El proxy de adopción se basa en productos análogos porque la App no tiene historia propia.
- El saldo potencial se estima con una mediana histórica, no como una predicción individual precisa.
- Los escenarios son explícitamente conservadores, base y expansivos, y no deben interpretarse como captación garantizada.

