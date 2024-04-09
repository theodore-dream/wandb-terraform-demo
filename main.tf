provider "google" {
  project = "bionic-region-419521"
  region = "us-east1"
  zone = "us-east1-b"
}

provider "google-beta" {
  project = "bionic-region-419521"
  region  = "us-east1"
  zone    = "us-east1-b"
}

data "google_client_config" "current" {}

provider "kubernetes" {
  host                   = "https://${module.wandb.cluster_endpoint}"
  cluster_ca_certificate = base64decode(module.wandb.cluster_ca_certificate)
  token                  = data.google_client_config.current.access_token
}

provider "helm" {
  kubernetes {
    host                   = "https://${module.wandb.cluster_endpoint}"
    token                  = data.google_client_config.current.access_token
    cluster_ca_certificate = base64decode(module.wandb.cluster_ca_certificate)
  }
}


module "wandb" {
  source    = "./modules/terraform-google-wandb"
  namespace = "theodore-unique"
  allowed_inbound_cidrs = ["0.0.0.0/0"]
  license               = var.license
  domain_name           = var.domain_name
  subdomain             = var.subdomain
  gke_machine_type = var.gke_machine_type

  wandb_version = var.wandb_version
  wandb_image   = var.wandb_image

  create_redis       = var.create_redis
  use_internal_queue = true
  force_ssl          = var.force_ssl

  deletion_protection = false

  database_sort_buffer_size = var.database_sort_buffer_size
  database_machine_type     = var.database_machine_type

  disable_code_saving = var.disable_code_saving
  size                = var.size
}

# Previous note - You'll want to update your DNS with the provisioned IP address

# Outputs
output "url" {
  value = module.wandb.url
}

output "address" {
  value = module.wandb.address
}

output "bucket_name" {
  value = module.wandb.bucket_name
}

output "standardized_size" {
  value = var.size
}

output "gke_node_count" {
  value = module.wandb.gke_node_count
}

output "gke_node_instance_type" {
  value = module.wandb.gke_node_instance_type
}

output "database_instance_type" {
  value = module.wandb.database_instance_type
}
