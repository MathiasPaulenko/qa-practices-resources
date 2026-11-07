# Native terraform test suite (Terraform 1.6+) — run with `terraform test`
# Expects a module exposing aws_s3_bucket.main and
# aws_s3_bucket_server_side_encryption_configuration.main
run "valid_bucket_name" {
  command = plan
  assert {
    condition     = aws_s3_bucket.main.bucket == "my-app-data-bucket"
    error_message = "S3 bucket name does not match expected value"
  }
}

run "bucket_is_encrypted" {
  command = apply
  assert {
    condition     = aws_s3_bucket_server_side_encryption_configuration.main.rule.apply_server_side_encryption_by_default.sse_algorithm == "AES256"
    error_message = "S3 bucket is not encrypted"
  }
}
