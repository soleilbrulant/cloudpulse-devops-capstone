variable "aws_region" {
  type        = string
  default     = "ap-south-1"
  description = "AWS deployment region"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Target deployment environment (dev, staging, production)"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR address space"
}

variable "cluster_name" {
  type        = string
  default     = "cloudpulse-eks-prod"
  description = "EKS Cluster identification name"
}

variable "node_instance_types" {
  type        = list(string)
  default     = ["t3.medium"]
  description = "EC2 instance types for EKS worker nodes"
}
