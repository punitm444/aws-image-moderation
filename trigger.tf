# Allow S3 to invoke the Lambda function
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_moderation.function_name
  principal     = "s3.amazonaws.com"

  source_arn = aws_s3_bucket.image_moderation_bucket.arn
}

# S3 Trigger
resource "aws_s3_bucket_notification" "lambda_trigger" {
  bucket = aws_s3_bucket.image_moderation_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.image_moderation.arn
    events              = ["s3:ObjectCreated:*"]

    filter_prefix = "uploads/"
  }

  depends_on = [
    aws_lambda_permission.allow_s3
  ]
}