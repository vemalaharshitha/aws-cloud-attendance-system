import json, boto3, logging
logging.basicConfig(level=logging.INFO)
table = boto3.resource('dynamodb').Table('Attendance')

def resp(code, body):
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    try:
        res = table.scan()
        items = res.get("Items", [])
        present = sum(1 for r in items if r.get("status")=="Present")
        absent  = sum(1 for r in items if r.get("status")=="Absent")
        return resp(200, {{"present": present, "absent": absent}})
    except Exception as e:
        logging.exception("stats error")
        return resp(500, {{"present":0,"absent":0}})
