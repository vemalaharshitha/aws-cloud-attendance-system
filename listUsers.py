import json, boto3, logging
logging.basicConfig(level=logging.INFO)
db = boto3.resource('dynamodb').Table('Users')

def resp(code, body):
    return {{ "statusCode": code, "headers": {{"Access-Control-Allow-Origin":"*"}}, "body": json.dumps(body) }}

def lambda_handler(event, context):
    try:
        role = (event.get("headers") or {{}}).get("role","")
        if role != "admin":
            return resp(403, [])
        res = db.scan()
        # mask passwords
        items = res.get("Items",[])
        for it in items:
            it["password"] = "*****"
        return resp(200, items)
    except Exception as e:
        logging.exception("list users error")
        return resp(500, [])
