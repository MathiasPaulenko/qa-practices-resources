"""Round-trip check for an S3 bucket: upload, encryption header, download, cleanup.

Run against a staging bucket only. Requires AWS credentials with
s3:PutObject, s3:GetObject and s3:DeleteObject on the target bucket.
"""

import os
import sys

import boto3
from botocore.exceptions import ClientError

BUCKET = os.environ.get("TEST_BUCKET", "my-app-bucket")
KEY = "test/cloud-storage-check.txt"

s3 = boto3.client("s3")  # boto3 >= 1.34


def test_upload_download_and_encryption() -> None:
    s3.put_object(Bucket=BUCKET, Key=KEY, Body="hello")
    head = s3.head_object(Bucket=BUCKET, Key=KEY)
    assert head.get("ServerSideEncryption") in ("AES256", "aws:kms"), (
        f"Object {KEY} landed without SSE on bucket {BUCKET}"
    )
    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    assert obj["Body"].read().decode() == "hello"
    s3.delete_object(Bucket=BUCKET, Key=KEY)


def test_anonymous_read_denied() -> None:
    """Unsigned access to a private bucket must return 403."""
    anon = boto3.client("s3", aws_access_key_id="", aws_secret_access_key="")
    anon.meta.events.register("choose-signer.s3.*", lambda **kw: None)
    try:
        anon.get_object(Bucket=BUCKET, Key=KEY)
    except ClientError as exc:
        assert exc.response["Error"]["Code"] in ("403", "AccessDenied"), exc
    else:
        raise AssertionError(f"Anonymous read succeeded on {BUCKET}")


if __name__ == "__main__":
    if BUCKET == "my-app-bucket":
        sys.exit("Set TEST_BUCKET to a staging bucket first.")
    test_upload_download_and_encryption()
    print("upload/download/encryption: OK")
