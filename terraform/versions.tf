terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.35"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CloudPulse"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Platform-DevOps"
    }
  }
}
