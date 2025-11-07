variable "db_name" {
  description = "The name of the database (e.g., 'mydb')"
  type        = string
}

variable "db_engine" {
  description = "Database engine (MySQL or PostgreSQL)"
  type        = string
  validation {
    condition     = contains(["mysql", "postgresql"], var.db_engine)
    error_message = "Allowed values for db_engine are 'mysql' or 'postgresql'."
  }
}

variable "environment" {
  description = "Environment (Dev/Prod), controls instance size and HA"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Allowed values for environment are 'dev' or 'prod'."
  }
}

variable "allocated_storage" {
  description = "The size of the database in GB"
  type        = number
  default     = 20
}

variable "allowed_access_sg_name" {
  description = "The NAME of a pre-existing Security Group that is allowed to access the RDS"
  type        = string
}
