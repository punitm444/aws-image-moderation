resource "aws_dynamodb_table" "image_moderation" {
  name         = "ImageModeration"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "image_key"

  attribute {
    name = "image_key"
    type = "S"
  }

  tags = {
    Name    = "ImageModeration"
    Project = "Image Moderation"
  }
}