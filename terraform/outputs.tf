output "vpc_id" {
  description = "Provisioned VPC ID"
  value       = aws_vpc.main.id
}

output "cluster_name" {
  description = "EKS Cluster Name"
  value       = aws_eks_cluster.eks.name
}

output "cluster_endpoint" {
  description = "EKS API Control Plane Endpoint"
  value       = aws_eks_cluster.eks.endpoint
}

output "kubeconfig_command" {
  description = "Command to authenticate kubectl with cluster"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${var.cluster_name}"
}
