resource "aws_s3_bucket" "image_moderation_bucket" {
  bucket = "punit-image-moderation-bucket1"

  tags = {
    Name    = "Image Moderation Bucket"
    Project = "Image Moderation"
  }
}

resource "aws_s3_object" "uploads_folder" {
  bucket = aws_s3_bucket.image_moderation_bucket.id
  key    = "uploads/"
}