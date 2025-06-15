import boto3
import os
import tempfile
from botocore.exceptions import ClientError
from fastapi import HTTPException
from botocore.config import Config

def get_s3_client():
    """Initialize and return an S3 client with timeout configuration."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            config=Config(connect_timeout=30, read_timeout=30)
        )
        return s3_client
    except Exception as e:
        print(f"❌ Failed to initialize S3 client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize S3 client: {str(e)}")

def download_file_from_s3(bucket_name: str, s3_key: str):
    """Download a file from S3 to a temporary file and return the file path."""
    try:
        s3_client = get_s3_client()
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as temp_file:
            temp_file_path = temp_file.name
        # Download the file with timeout
        print(f"📥 Starting download of {s3_key} from bucket {bucket_name}")
        s3_client.download_file(bucket_name, s3_key, temp_file_path)
        print(f"✅ Successfully downloaded {s3_key} to {temp_file_path}")
        return temp_file_path
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ S3 Error: {error_code} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"S3 Error: {error_code} - {str(e)}")
    except Exception as e:
        print(f"❌ Error downloading {s3_key} from S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download file from S3: {str(e)}")

def get_s3_file_metadata(bucket_name: str, s3_key: str):
    """Retrieve metadata (e.g., file size) for an S3 object."""
    try:
        s3_client = get_s3_client()
        response = s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        print(f"✅ Retrieved metadata for {s3_key} from bucket {bucket_name}")
        return response
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ S3 Metadata Error: {error_code} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"S3 Metadata Error: {error_code} - {str(e)}")