resource "aws_sns_topic" "image_moderation_alerts" {
  name = "image-moderation-alerts"
}

resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.image_moderation_alerts.arn
  protocol  = "email"
  endpoint  = "punitm2004@gmail.com"
}