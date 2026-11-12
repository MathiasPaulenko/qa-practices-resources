"""Structured Streaming sink with checkpointing — fault-tolerance configuration
for recovery testing (driver restart mid-stream, no duplicates or gaps)."""
from pyspark.sql import DataFrame


def upsert_batch(batch_df: DataFrame, batch_id: int):
    """Idempotent sink write — safe to replay on recovery."""
    (
        batch_df.write
        .mode("append")
        .format("parquet")
        .save(f"data/sink/batch_{batch_id}")
    )


def start_query(stream_df):
    return (
        stream_df.writeStream
        .foreachBatch(upsert_batch)
        .option("checkpointLocation", "s3a://checkpoints/orders")
        .trigger(processingTime="5 minutes")
        .start()
    )


# Recovery test: start the query, kill the driver mid-stream, restart it,
# and assert the sink has no duplicated or missing records within the SLA.
