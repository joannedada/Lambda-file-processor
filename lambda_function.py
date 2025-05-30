import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        print("Event received:", json.dumps(event, indent=2))
        
        # Handle S3 file upload
        if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:s3':
            record = event['Records'][0]
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            s3 = boto3.client('s3')
            metadata = s3.head_object(Bucket=bucket, Key=key)
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "File processed!",
                    "file": key,
                    "size": metadata['ContentLength'],
                    "last_modified": str(metadata['LastModified'])
                })
            }
        
        # Handle API Gateway request
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Send a file to S3 to trigger Lambda!"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }