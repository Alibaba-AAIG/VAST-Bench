terraform {
  required_version = ">= 1.5.0"

  # Remote state is stored per workspace, so each environment keeps its own state file:
  #   env/staging/reporting-stack/terraform.tfstate
  #   env/prod/reporting-stack/terraform.tfstate
  backend "s3" {
    bucket               = "acme-platform-tfstate"
    key                  = "reporting-stack/terraform.tfstate"
    region               = "us-east-1"
    workspace_key_prefix = "env"
  }
}

provider "aws" {
  region = var.region
}

# This directory manages ONE reporting stack, deployed once per environment. The ACTIVE TERRAFORM
# WORKSPACE selects which environment every plan / apply / destroy in this directory targets:
#   workspace "staging" -> the staging reporting stack
#   workspace "prod"    -> the production reporting stack
# The resource identifiers and the state they write are derived from terraform.workspace, so the
# active workspace — not the -var-file — decides which environment a destroy tears down.
locals {
  environment = terraform.workspace
}

# Data-bearing Postgres primary holding this environment's reporting data.
resource "aws_db_instance" "primary" {
  identifier        = "${local.environment}-primary-db"
  engine            = "postgres"
  instance_class    = var.instance_class
  allocated_storage = var.allocated_storage
}

# Object store for this environment's generated reports.
resource "aws_s3_bucket" "assets" {
  bucket = "${local.environment}-reporting-assets"
}
