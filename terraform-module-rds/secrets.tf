resource "random_password" "db_password" {
  length  = 16
  special = true
  override_special = "!#$%&()*+,-.:;<=>?@[]^_`{|}~"
}

resource "aws_secretsmanager_secret" "this" {
  name        = "${var.db_name}-credentials"
  description = "Credentials for ${var.db_name} RDS instance"
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id     = aws_secretsmanager_secret.this.id
  secret_string = jsonencode({
    username = "admin"
    password = random_password.db_password.result
  })
}
