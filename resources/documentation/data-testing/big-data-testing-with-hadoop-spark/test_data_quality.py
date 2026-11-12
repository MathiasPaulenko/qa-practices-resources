"""Data quality checks as pipeline gates — plain PySpark, no extra framework."""
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("dq-tests")
        .getOrCreate()
    )


def null_rate(df, column):
    total = df.count()
    if total == 0:
        return 0.0
    return df.filter(df[column].isNull()).count() / total


def distinct_in(df, column, allowed):
    return df.filter(~df[column].isin(allowed)).count() == 0


def test_null_rate_within_bounds(spark):
    events_df = spark.createDataFrame(
        [("u1", "click"), ("u2", "view"), (None, "click")],
        ["user_id", "event"],
    )
    assert null_rate(events_df, "user_id") < 0.5


def test_allowed_values(spark):
    events_df = spark.createDataFrame(
        [("u1", "click"), ("u2", "view")],
        ["user_id", "event"],
    )
    assert distinct_in(events_df, "event", ["click", "view", "purchase"])
