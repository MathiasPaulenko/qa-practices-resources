"""Spark transformation under test (PySpark 3.5+)."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def daily_revenue(df: DataFrame) -> DataFrame:
    """Aggregate order amounts into daily revenue per currency."""
    return (
        df.groupBy("day", "currency")
        .agg(F.sum("amount").alias("total"))
        .orderBy("day", "currency")
    )
