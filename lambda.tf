resource "aws_lambda_function" "image_moderation" {
  function_name = "image-moderation-function"

  role          = "arn:aws:iam::393060838514:role/service-role/image-moderation-function-role-nlids9oc"
  runtime       = "python3.13"
  handler       = "lambda_function.lambda_handler"
  architectures = ["x86_64"]

  filename         = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")
}