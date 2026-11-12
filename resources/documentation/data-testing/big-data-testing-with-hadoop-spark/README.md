# Big Data Testing with Hadoop / Spark Companion

Companion resource for [Big Data Testing with Hadoop / Spark](https://qapractices.com/documentation/big-data-testing-with-hadoop-spark). Runnable examples of the three test layers covered in the guide: transformation unit tests, data quality checks, and fault-tolerant streaming configuration.

## Files

| File | What it tests | Stack |
|------|---------------|-------|
| `transforms.py` | Transformation under test (`daily_revenue`) | PySpark 3.5+ |
| `test_transform.py` | Transform unit tests, incl. empty input | pytest 8.x, `assertDataFrameEqual` |
| `test_data_quality.py` | Null rate and allowed-value gates | PySpark assertions |
| `streaming_checkpoint.py` | Checkpointed streaming sink config | Structured Streaming |

## Quick Start

```bash
pip install "pyspark==3.5.*" "pytest==8.*"
pytest -v
```

`test_transform.py` and `test_data_quality.py` run entirely in Spark local mode — no cluster needed. `streaming_checkpoint.py` is a configuration reference: run it against a test cluster or local streaming source to verify checkpoint recovery (restart the driver mid-stream and check for duplicates or gaps in the sink).

## Requirements

- Java 11 or 17 (Spark 3.5 requirement), `JAVA_HOME` set
- Python 3.9+ with `pyspark==3.5.*` and `pytest==8.*`
- For the streaming example: a test cluster or local stream source — never first-run in production
