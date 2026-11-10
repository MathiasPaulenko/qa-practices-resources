# Terraform — disposable test-runner instance (Q8)
# Companion file for: https://qapractices.com/documentation/devops-interview-questions-qa
# AMI IDs are region-specific: resolve yours with `aws ec2 describe-images` or an aws_ami data source

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_instance" "test_runner" {
  ami           = "ami-0c55b159cbfafe1f0" # Placeholder: example AMI from AWS docs — replace for your region
  instance_type = "t3.medium"

  tags = {
    Name        = "qa-test-runner"
    Environment = "test"
  }
}

output "instance_ip" {
  value = aws_instance.test_runner.public_ip
}
