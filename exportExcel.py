import json, boto3, pandas as pd, tempfile, uuid, logging, os
logging.basicConfig(level=logging.INFO)
s3 = boto3.client('s3')
table = boto3.resource('dynamodb').Table('Attendance')
BUCKET = os.environ.get('EXPORT_BUCKET','attendance-photos-yourname')  # change or set env var

def resp(code, body):
    return {"statusCode": code, "headers":{"Access-Control-Allow-Origin":"*"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    try:
        items = table.scan().get("Items", [])
        if not items:
            return resp(200, {{"download_url": None, "msg":"No data"}})
        df = pd.DataFrame(items)
        key = f"exports/{uuid.uuid4()}.xlsx"
        tmp = tempfile.gettempdir()+"/file.xlsx"
        df.to_excel(tmp, index=False)
        s3.upload_file(tmp, BUCKET, key)
        url = s3.generate_presigned_url("get_object", Params={{"Bucket":BUCKET,"Key":key}}, ExpiresIn=3600)
        return resp(200, {{"download_url": url}})
    except Exception as e:
        logging.exception("excel error")
        return resp(500, {{"error":"export failed"}})
