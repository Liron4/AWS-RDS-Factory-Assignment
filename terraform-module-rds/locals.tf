locals {
  is_prod       = var.environment == "prod"
  instance_size = local.is_prod ? "db.t3.small" : "db.t3.micro"
  
  db_port_map = {
    mysql      = 3306
    postgresql = 5432
  }
  db_port = local.db_port_map[var.db_engine]
}
