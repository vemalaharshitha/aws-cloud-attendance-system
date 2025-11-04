import json, boto3, os, logging
logging.basicConfig(level=logging.INFO)
s3 = boto3.client('s3')
BUCKET = os.environ.get('PHOTO_BUCKET','attendance-photos-yourname')  # set env var or change

def resp(code, body):
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body","{}"))
        filename = body.get("filename")
        if not filename:
            return resp(400, "filename required")
        key = f"{filename}.jpg"
        url = s3.generate_presigned_url("put_object",
            Params={{"Bucket": BUCKET, "Key": key, "ContentType": "image/jpeg"}},
            ExpiresIn=300)
        return resp(200, url)
    except Exception as e:
        logging.exception("signed url error")
        return resp(500, "server error")
