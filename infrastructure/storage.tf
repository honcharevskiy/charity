resource "aws_s3_bucket" "pictures" {
  bucket   = "charity-pictures"
  provider = aws.storage

  tags = {
    Name = "charity"
  }
}

resource "aws_s3_bucket_ownership_controls" "pictures" {
  bucket   = aws_s3_bucket.pictures.id
  provider = aws.storage
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "pictures" {
  bucket   = aws_s3_bucket.pictures.id
  provider = aws.storage

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "example" {
  provider = aws.storage
  depends_on = [
    aws_s3_bucket_ownership_controls.pictures,
    aws_s3_bucket_public_access_block.pictures,
  ]

  bucket = aws_s3_bucket.pictures.id
  acl    = "public-read"
}