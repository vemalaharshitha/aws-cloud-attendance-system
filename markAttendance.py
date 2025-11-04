import json, boto3, datetime, logging
from boto3.dynamodb.conditions import Key

logging.basicConfig(level=logging.INFO)
table = boto3.resource('dynamodb').Table('Attendance')

def resp(code, body):
    if not isinstance(body, str):
        body = json.dumps(body)
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": body}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body","{}"))
        sid = body.get("studentId"); status = body.get("status")
        markedBy = (event.get("headers") or {}).get("x-user", "faculty1")
        if not sid or status not in ("Present","Absent"):
            return resp(400, "studentId & valid status required")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table.put_item(Item={
            "studentId": sid,
            "date_time": now,
            "status": status,
            "markedBy": markedBy
        })
        logging.info("marked %s %s", sid, status)
        return resp(200, f"✅ {sid} marked {status} at {now}")
    except Exception as e:
        logging.exception("mark error")
        return resp(500, "server error")
