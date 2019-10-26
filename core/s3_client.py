import boto3
from boto3.s3.transfer import TransferConfig

from core.configs import *


class S3Client:
    def __init__(self, bucket_name):
        _credentials = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "region_name": AWS_REGION
        }
        self.bucket_name = bucket_name
        self.transfer_config = TransferConfig(multipart_threshold=MULTIPART_THRESHOLD, max_concurrency=MAX_CONCURRENCY,
                                              multipart_chunksize=MULTIPART_CHUNKSIZE)
        self.s3 = boto3.resource('s3', **_credentials)

    def list_buckets(self):
        return self.s3.buckets.all()

    def list_objects(self):
        return self.s3.Bucket(self.bucket_name).objects.all()

    def get_object(self, object_key):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key)

    def put_object(self, object_key, file_path, metadata):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key) \
            ._upload_file(file_path, Config=self.transfer_config, ExtraArgs={"Metadata": metadata})
