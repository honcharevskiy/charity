terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "pictures" {
  bucket = "charity-pictures"

  tags = {
    Name        = "Charity"
  }
}

resource "aws_s3_bucket_ownership_controls" "pictures" {
  bucket = aws_s3_bucket.pictures.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "pictures" {
  bucket = aws_s3_bucket.pictures.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "example" {
  depends_on = [
    aws_s3_bucket_ownership_controls.pictures,
    aws_s3_bucket_public_access_block.pictures,
  ]

  bucket = aws_s3_bucket.pictures.id
  acl    = "public-read"
}