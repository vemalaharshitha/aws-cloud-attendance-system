import json, boto3, logging
from boto3.dynamodb.conditions import Key, Attr

logging.basicConfig(level=logging.INFO)
table = boto3.resource('dynamodb').Table('Attendance')

def resp(code, body):
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        sid = params.get("studentId","").strip()
        from_d = params.get("from","")
        to_d = params.get("to","")
        items = []
        if sid:
            # Query by studentId, then filter on date range if provided
            res = table.query(KeyConditionExpression=Key("studentId").eq(sid))
            items = res.get("Items", [])
        else:
            # Scan all (demo)
            res = table.scan()
            items = res.get("Items", [])
        # Optional date filtering
        if from_d:
            items = [r for r in items if r.get("date_time","") >= from_d]
        if to_d:
            items = [r for r in items if r.get("date_time","") <= to_d+"~"]
        return resp(200, items)
    except Exception as e:
        logging.exception("history error")
        return resp(500, [])
