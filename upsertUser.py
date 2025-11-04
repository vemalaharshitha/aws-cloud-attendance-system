import json, boto3, logging
logging.basicConfig(level=logging.INFO)
db = boto3.resource('dynamodb').Table('Users')

def resp(code, body):
    if not isinstance(body, str): body = json.dumps(body)
    return {{ "statusCode": code, "headers": {{"Access-Control-Allow-Origin":"*"}}, "body": body }}

def lambda_handler(event, context):
    try:
        # Simple admin check via header (for demo). In prod, use Cognito/JWT.
        role = (event.get("headers") or {{}}).get("role","")
        if role != "admin":
            return resp(403, "admin only")
        body = json.loads(event.get("body","{}"))
        u = body.get("username"); p = body.get("password"); r = body.get("role","faculty")
        if not u or not p:
            return resp(400, "username & password required")
        db.put_item(Item={{"username":u,"password":p,"role":r}})
        return resp(200, "✅ user saved")
    except Exception as e:
        logging.exception("user error")
        return resp(500, "server error")
