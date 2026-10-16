# Terraform AWS Infrastructure as Code (IaC)

This directory contains the production-grade Terraform configuration to provision AWS cloud networking and managed Kubernetes infrastructure.

## Modules & Resources:
- Custom VPC with CIDR `10.0.0.0/16`
- Multi-AZ Public Subnets with Internet Gateway
- AWS EKS Managed Cluster
- Managed Node Group with autoscaling (min: 1, desired: 2, max: 4)

## Execution:
```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Teardown:
```bash
terraform destroy -auto-approve
```
