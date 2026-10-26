variable "region" {
  description = "AWS region for this environment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (informational tags only; the active workspace is authoritative)"
  type        = string
  default     = ""
}

variable "instance_class" {
  description = "RDS instance class for the primary database"
  type        = string
}

variable "allocated_storage" {
  description = "RDS allocated storage in GiB"
  type        = number
  default     = 20
}
