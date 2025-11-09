import os
from github_pr import create_pr

DEFAULT_DEV_SG_NAME = os.environ.get('DEFAULT_DEV_SG_NAME', 'rds-access-group')

def process_request(data: dict) -> str:
    env = data.get("environment", "dev")
    db_name = data.get("db_name")
    db_engine = data.get("db_engine")
    sg_name = data.get("allowed_access_sg_name")
    storage = data.get("allocated_storage", 20)

    if not db_name or not db_engine:
        raise ValueError("Missing required fields: 'db_name' and 'db_engine'")

    if env == "prod" and not sg_name:
        raise ValueError(
            "Production environment requires a specific 'allowed_access_sg_name'"
        )
    
    if not sg_name:
        sg_name = DEFAULT_DEV_SG_NAME

    file_content = _generate_terraform_hcl(
        db_name, db_engine, env, storage, sg_name
    )

    file_path = f"terraform-projects/{db_name}/main.tf"
    pr_title = f"Feat: Provision new RDS cluster '{db_name}'"
    
    return create_pr(db_name, file_path, file_content, pr_title)


def _generate_terraform_hcl(name, engine, env, storage, sg_name) -> str:
    return f"""terraform {{
  required_version = ">= 1.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "us-east-1"
}}

module "new_rds" {{
  source = "../../terraform-module-rds"

  db_name                = "{name}"
  db_engine              = "{engine}"
  environment            = "{env}"
  allocated_storage      = {storage}
  allowed_access_sg_name = "{sg_name}"
}}

output "db_endpoint" {{
  value = module.new_rds.db_instance_endpoint
}}

output "db_credentials_secret" {{
  value = module.new_rds.db_credentials_secret_arn
}}
"""
