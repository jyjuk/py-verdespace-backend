import boto3
from django.conf import settings


def generate_presigned_url(file_key):
    """
    Генерує Pre-signed URL для доступу до файлу в S3.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": file_key},
            ExpiresIn=3600,
        )
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None
