import json, boto3, logging
logging.basicConfig(level=logging.INFO)
db = boto3.resource('dynamodb').Table('Users')

def resp(code, body):
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body","{}"))
        u = body.get("username"); p = body.get("password")
        if not u or not p:
            return resp(400, {"auth": False, "msg":"username & password required"})
        res = db.get_item(Key={{"username":u}})
        item = res.get("Item")
        if not item or item.get("password") != p:
            return resp(200, {"auth": False})
        return resp(200, {"auth": True, "role": item.get("role","faculty")})
    except Exception as e:
        logging.exception("login error")
        return resp(500, {"auth": False, "msg":"server error"})
