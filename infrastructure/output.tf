output "instance_ip" {
  value = aws_instance.django_instance.public_ip
}

output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.charity.address
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.charity.port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.charity.username
  sensitive   = false
}

output "instance_profile_name" {
  description = "The name of the instance profile"
  value       = aws_iam_instance_profile.ec2_instance_profile.name
}


output "instance_role_arn" {
  description = "ARN of EC2 instance role"
  value = aws_iam_role.ec2_s3_access.arn
}