import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("StudentFeedback")

def lambda_handler(event, context):
    try:
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)

        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
        feedback = body.get("feedback", "").strip()

        if not name or not email or not feedback:
            return response(400, {"message": "All fields are required"})

        table.put_item(Item={
            "feedbackId": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "feedback": feedback,
            "createdAt": datetime.now(timezone.utc).isoformat()
        })

        return response(200, {
            "message": "Feedback submitted successfully!"
        })

    except Exception as e:
        print("Error:", str(e))
        return response(500, {"message": "Internal server error"})

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }
