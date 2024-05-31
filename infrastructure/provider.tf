provider "aws" {
  region  = var.region
  profile = "charity"
}

provider "aws" {
  alias   = "storage"
  profile = "charity"
  region  = "us-east-1"
}