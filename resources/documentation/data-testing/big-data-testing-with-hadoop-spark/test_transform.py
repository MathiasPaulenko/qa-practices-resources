"""Unit test for a Spark transformation — pytest 8.x + PySpark 3.5+ local mode."""
import pytest
from pyspark.sql import SparkSession
from pyspark.testing import assertDataFrameEqual  # Spark 3.5+

from transforms import daily_revenue


@pytest.fixture(scope="session")
def spark():
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("transform-tests")
        .getOrCreate()
    )


def test_daily_revenue_aggregation(spark):
    input_df = spark.createDataFrame(
        [("2025-06-01", "EUR", 10.0),
         ("2025-06-01", "EUR", 15.5),
         ("2025-06-02", "USD", 20.0)],
        ["day", "currency", "amount"],
    )
    expected = spark.createDataFrame(
        [("2025-06-01", "EUR", 25.5),
         ("2025-06-02", "USD", 20.0)],
        ["day", "currency", "total"],
    )
    result = daily_revenue(input_df)
    assertDataFrameEqual(result, expected)


def test_daily_revenue_empty_input(spark):
    input_df = spark.createDataFrame([], "day STRING, currency STRING, amount DOUBLE")
    expected = spark.createDataFrame([], "day STRING, currency STRING, total DOUBLE")
    assertDataFrameEqual(daily_revenue(input_df), expected)
