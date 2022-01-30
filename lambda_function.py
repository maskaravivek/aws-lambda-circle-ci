import boto3
import os
import json
from botocore.exceptions import NoCredentialsError

def lambda_handler(event, context):
    s3_url = upload_to_aws('/tmp/file.jpg', 'uploads/hello.jpg')
    return {
            "statusCode": 200,
            'headers': {'Content-Type': 'application/json'},
            "body": json.dumps({
                "output": s3_url,
                "outputType": "image"
            })
        }

def upload_to_aws(local_file, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, os.environ['BUCKET_NAME'], s3_file)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': s3_file
            },
            ExpiresIn=24 * 3600
        )

        print("Upload Successful", url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None