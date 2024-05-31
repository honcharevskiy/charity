variable "region" {
  default = "eu-central-1"
}

variable "availability_zones" {
  default = ["eu-central-1a", "eu-central-1b"]
}

variable "storage_region" {
  default = "eu-central-1"
}

variable "rds_db_name" {
  description = "RDS database name"
  default     = "charity"
}
variable "rds_username" {
  description = "RDS database username"
  default     = "charity"
}
variable "rds_password" {
  description = "postgres password for production DB"
}
variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t4g.micro"
}