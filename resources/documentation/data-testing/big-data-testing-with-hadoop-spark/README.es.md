# Companion de Testing de Big Data con Hadoop / Spark

Recurso companion de [Testing de Big Data con Hadoop / Spark](https://qapractices.com/es/documentation/big-data-testing-with-hadoop-spark). Ejemplos ejecutables de las tres capas de testing de la guía: unit tests de transformaciones, chequeos de calidad de datos y configuración de streaming tolerante a fallos.

## Archivos

| Archivo | Qué testea | Stack |
|---------|------------|-------|
| `transforms.py` | Transformación bajo test (`daily_revenue`) | PySpark 3.5+ |
| `test_transform.py` | Unit tests de transformación, incl. input vacío | pytest 8.x, `assertDataFrameEqual` |
| `test_data_quality.py` | Gates de tasa de nulls y valores permitidos | Asserts de PySpark |
| `streaming_checkpoint.py` | Config de sink de streaming con checkpoint | Structured Streaming |

## Inicio Rápido

```bash
pip install "pyspark==3.5.*" "pytest==8.*"
pytest -v
```

`test_transform.py` y `test_data_quality.py` corren enteros en modo local de Spark — no hace falta clúster. `streaming_checkpoint.py` es una referencia de configuración: corréla contra un clúster de test o una fuente de streaming local para verificar la recuperación por checkpoint (reiniciá el driver a mitad de stream y buscá duplicados o huecos en el sink).

## Requisitos

- Java 11 o 17 (requisito de Spark 3.5), con `JAVA_HOME` configurado
- Python 3.9+ con `pyspark==3.5.*` y `pytest==8.*`
- Para el ejemplo de streaming: un clúster de test o fuente de stream local — nunca primera corrida en producción
