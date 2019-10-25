import glob
import logging
from os.path import isfile

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from configs import *
from utils import calc_etag_part, calc_etag_whole

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(filename='debug.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class S3Client:
    def __init__(self, bucket_name):
        _credentials = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "region_name": AWS_REGION
        }
        self.bucket_name = bucket_name
        self.transfer_config = TransferConfig(multipart_threshold=MULTIPART_THRESHOLD, max_concurrency=MAX_CONCURRENCY)
        self.s3 = boto3.resource('s3', **_credentials)

    def list_buckets(self):
        return self.s3.buckets.all()

    def list_objects(self):
        return self.s3.Bucket(self.bucket_name).objects.all()

    def get_object(self, object_key):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key)

    def put_object(self, object_key, file_path):
        return self.s3.Object(bucket_name=self.bucket_name, key=object_key).upload_file(file_path,
                                                                                        Config=self.transfer_config)


class Syncer:
    def __init__(self):
        self.bucket_name = DEFAULT_BUCKET_NAME
        self.client = S3Client(self.bucket_name)
        self.CHUNK_SIZE = 4 * 1024 * 1024
        self.dry_run = False

    def sync(self, dry_run=True, recursive=True):
        """
        Scan the directory of interest
        """
        self.dry_run = dry_run
        logger.info("Dry run is {}".format("on" if dry_run else "off"))

        if not self.bucket_name:
            raise AssertionError("Bucket name is missing.")

        files_iter = glob.iglob("*.py", recursive=recursive)
        for file in files_iter:
            if isfile(file):
                etag_local = self.calc_etag(file)

                # File not in Bucket
                if not self.is_object_exists(file):
                    logger.debug("File doesn't exist ({})".format(file))
                    self.upload_file(file)
                else:
                    # File is in Bucket
                    etag_remote = self.get_object(file).e_tag
                    if etag_local != etag_remote:  # Upload file if sync required
                        logger.info("Etags mismatched. File is being uploaded ({})".format(file))
                        self.upload_file(file)

    def is_object_exists(self, rel_file_path) -> bool:
        try:
            self.get_object(rel_file_path=rel_file_path).metadata
        except ClientError as e:
            if e.response["Error"]["Code"] == '404':
                return False
            raise e
        else:
            return True

    def upload_file(self, file):
        if self.dry_run:
            return

        self.client.put_object(object_key=file, file_path=file)

    def get_object(self, rel_file_path):
        return self.client.get_object(object_key=rel_file_path)

    def calc_etag(self, rel_file_path):
        file_size = os.stat(rel_file_path).st_size
        if file_size > MULTIPART_THRESHOLD:
            return calc_etag_part(rel_file_path, file_size)
        else:
            return calc_etag_whole(rel_file_path)

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name
        self._initialize_client()

    def _initialize_client(self):
        self.client = S3Client(self.bucket_name)
