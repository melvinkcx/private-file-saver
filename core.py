import boto3

from .configs import *


class S3Client:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

    def create_bucket(self, bucket_name):
        bucket_configuration = {'LocationConstraint': AWS_REGION}
        return self.client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=bucket_configuration)

    def list_buckets(self):
        return self.client.list_buckets()
