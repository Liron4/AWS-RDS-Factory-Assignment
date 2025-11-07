resource "aws_db_instance" "this" {
  identifier           = var.db_name
  engine               = var.db_engine
  instance_class       = local.instance_size
  allocated_storage    = var.allocated_storage

  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  username               = jsondecode(aws_secretsmanager_secret_version.this.secret_string)["username"]
  password               = jsondecode(aws_secretsmanager_secret_version.this.secret_string)["password"]

  multi_az             = local.is_prod
  skip_final_snapshot  = !local.is_prod

  publicly_accessible = false
  storage_encrypted   = true
  
  deletion_protection = local.is_prod

  tags = {
    Name        = var.db_name
    Environment = var.environment
    CreatedBy   = "Terraform-Automation"
  }
}
