import boto3
import urllib.parse
from datetime import datetime, timezone
from decimal import Decimal

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = "ImageModeration"

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:393060838514:image-moderation-alerts"

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    print("Received event:", event)

    # Get bucket name and object name from S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"]
    )

    print("Bucket:", bucket)
    print("Image:", key)

    # Send image to Amazon Rekognition
    response = rekognition.detect_moderation_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        },
        MinConfidence=80
    )

    labels = response["ModerationLabels"]

    # Determine whether image is safe
    if labels:
        status = "UNSAFE"
    else:
        status = "SAFE"

    print("Moderation status:", status)
    print("Labels:", labels)

    # Prepare labels for DynamoDB
    moderation_labels = []

    for label in labels:
        moderation_labels.append({
            "name": label["Name"],
            "parent_name": label.get("ParentName", ""),
            "confidence": Decimal(str(label["Confidence"]))
        })

    # Store image result in DynamoDB
    table.put_item(
        Item={
            "image_key": key,
            "bucket": bucket,
            "status": status,
            "moderation_labels": moderation_labels,
            "uploaded_at": datetime.now(timezone.utc).isoformat()
        }
    )

    print("Result stored in DynamoDB")

    # Send SNS notification if image is unsafe
    if status == "UNSAFE":

        detected_labels = "\n".join(
            f"{label['Name']} - {label['Confidence']:.2f}%"
            for label in labels
        )

        message = f"""
Unsafe Image Detected

File: {key}
Bucket: {bucket}
Status: {status}

Detected moderation labels:

{detected_labels}
"""

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Unsafe Image Detected",
            Message=message
        )

        print("SNS notification sent")

    return {
        "statusCode": 200,
        "body": f"{key} processed successfully. Status: {status}"
    }