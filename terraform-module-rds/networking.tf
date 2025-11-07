resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.db_name}-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "${var.db_name} Subnet Group"
  }
}

resource "aws_security_group" "rds_sg" {
  name   = "${var.db_name}-sg"
  vpc_id = data.aws_vpc.default.id

  description = "Controls access to the ${var.db_name} RDS instance"

  ingress {
    from_port       = local.db_port
    to_port         = local.db_port
    protocol        = "tcp"
    security_groups = [data.aws_security_group.allowed_access.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
