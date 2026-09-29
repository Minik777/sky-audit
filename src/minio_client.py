import json
import os
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')
BUCKET = os.getenv('MINIO_BUCKET', "sky-audit")

def get_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name='us-east-1',
    )

def ensure_bucket(client, bucket=BUCKET):
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        client.create_bucket(Bucket=bucket)

def build_key(run_dt):
    return f"raw/open-meteo/date={run_dt:%Y-%m-%d}/hour={run_dt:%H}.json"


def put_json(client,key, data, bucket=BUCKET):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    client.put_object(Bucket=bucket,
                      Key=key,
                      Body=body,
                      ContentType='application/json'
    )

def get_json(client, key, bucket=BUCKET):
    response = client.get_object(Bucket=bucket, Key=key)
    pprint(response)
    return json.loads(response['Body'].read())

if __name__ == '__main__':
    s3 = get_client()
    ensure_bucket(s3)
    put_json(s3, 'test/hello.json', {"hello": "minio"})
    print(get_json(s3, 'test/hello.json'))
