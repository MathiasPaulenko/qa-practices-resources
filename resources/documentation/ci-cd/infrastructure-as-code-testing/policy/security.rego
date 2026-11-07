# OPA policy evaluated against `terraform show -json tfplan > plan.json`
# Usage: opa eval --data policy/ --input plan.json "data.terraform.analysis.deny"
package terraform.analysis

import input.plan as plan

# Deny any security group rule that opens SSH to the world
deny[msg] {
  resource := plan.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  resource.change.after.from_port <= 22
  resource.change.after.to_port >= 22
  msg := sprintf("Security group %v allows SSH from anywhere", [resource.address])
}

# Deny unencrypted S3 buckets
deny[msg] {
  resource := plan.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not resource.change.after.server_side_encryption_configuration
  msg := sprintf("S3 bucket %v is not encrypted", [resource.address])
}
