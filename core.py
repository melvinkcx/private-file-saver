import glob
import hashlib
from os.path import isfile

import boto3
from botocore.exceptions import ClientError

from .configs import *


class S3Client:
    def __init__(self, bucket_name):
        _credentials = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "region_name": AWS_REGION
        }
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3', **_credentials)

    def list_buckets(self):
        return self.s3.buckets.all()

    def list_objects(self):
        return self.s3.Bucket(self.bucket_name).objects.all()

    def get_object(self, object_key):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key)

    def put_object(self, object_key, file_path):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key).upload_file(file_path)


class Syncer:
    def __init__(self):
        self.bucket_name = ""
        self.client = S3Client(self.bucket_name)
        self.CHUNK_SIZE = 4 * 1024 * 1024

    def sync(self):
        """
        Scan the directory of interest
        """
        files_iter = glob.iglob("**", recursive=True)
        for file in files_iter:
            if isfile(file):
                etag_local = self.calc_etag(file)

                if not self.is_object_exists(file):
                    self.upload_file(file)

                etag_remote = self.get_object_etag(file)

                if not self.compare_etags(etag_local, etag_remote):
                    self.upload_file(file)

    def is_object_exists(self, rel_file_path) -> bool:
        try:
            self.get_object(rel_file_path=rel_file_path).metadata
        except ClientError as e:
            if e.response["Error"]["Code"] == 404:
                return False
            raise e
        else:
            return True

    def upload_file(self, file):
        self.client.put_object(object_key=file, file_path=file)

    def get_object_etag(self, rel_file_path) -> str:
        return self.get_object(rel_file_path=rel_file_path).etag

    def get_object(self, rel_file_path):
        """
        Throw Object not found?
        :param rel_file_path:
        :return:
        """
        return self.client.get_object(object_key=rel_file_path)

    def calc_etag(self, rel_file_path):
        hasher = hashlib.md5()
        with open(rel_file_path, 'rb') as afile:
            buf = afile.read(self.CHUNK_SIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(self.CHUNK_SIZE)
        return hasher.hexdigest()

    def compare_etags(self, etag_local, etag_remote):
        return etag_local == etag_remote
