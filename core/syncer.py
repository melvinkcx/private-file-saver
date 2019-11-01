import glob
import os
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import isfile, isdir

from botocore.exceptions import ClientError

from core.configs import configs
from core.log_utils import logger
from core.s3_client import S3Client
from core.utils import calc_md5sum


class Syncer:
    def __init__(self):
        self.target_path = configs.TARGET_PATH
        self.bucket_name = configs.DEFAULT_BUCKET_NAME
        self.max_workers = configs.MAX_CONCURRENCY

        self.client = S3Client(self.bucket_name)

        self.dry_run = False
        self.files_queue = []  # Files to be uploaded

    def scan(self, path, recursive=False, file_pattern="**"):
        if path is None:
            path = self.target_path

        target_directory = os.path.abspath(path)
        logger.info(f"Target directory: {target_directory}")
        os.chdir(target_directory)

        files_iter = glob.iglob(file_pattern, recursive=recursive)
        files = []
        for file in files_iter:
            if isdir(file):
                files.append((file, 'DIRECTORY'))

            if isfile(file):
                md5sum_local = calc_md5sum(file)

                if not self._is_object_exists(file):
                    # File not in Bucket
                    files.append((file, 'FILE', 'NOT_UPLOADED'))
                else:
                    # File is in Bucket
                    metadata_remote = self._get_object_metadata(file)
                    md5sum_remote = metadata_remote.get('md5sum', None)

                    if md5sum_local != md5sum_remote:
                        # File is not synced
                        files.append((file, 'FILE', 'NOT_SYNCED'))
                    else:
                        # File is synced
                        files.append((file, 'FILE', 'SYNCED'))

        return files

    def sync(self, path, dry_run=False, recursive=True, file_pattern="**"):
        """
        Scan the directory of interest
        """
        self.dry_run = dry_run
        logger.info("Dry run is {}".format("on" if dry_run else "off"))

        if path is None:
            path = self.target_path

        target_directory = os.path.abspath(path)
        logger.info(f"Target directory: {target_directory}")
        os.chdir(target_directory)

        files_iter = glob.iglob(file_pattern, recursive=recursive)
        for file in files_iter:
            if isfile(file):
                md5sum_local = calc_md5sum(file)

                # File not in Bucket
                if not self._is_object_exists(file):
                    logger.debug("File doesn't exist, queuing file.. ({})".format(file))
                    self.files_queue.append((file, md5sum_local))
                else:
                    # File is in Bucket
                    metadata_remote = self._get_object_metadata(file)
                    md5sum_remote = metadata_remote.get('md5sum', None)
                    if md5sum_local != md5sum_remote:  # Upload file if sync required
                        logger.info("Etags mismatched. File is being queued ({})".format(file))
                        self.files_queue.append((file, md5sum_local))

        logger.info("Preparing to upload all files...")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            [executor.submit(self._upload_file, file, md5sum) for file, md5sum in self.files_queue]
        logger.info("All files has been uploaded!")

    def _is_object_exists(self, rel_file_path) -> bool:
        try:
            self._get_object_metadata(rel_file_path=rel_file_path)
        except ClientError as e:
            if e.response["Error"]["Code"] == '404':
                return False
            raise e
        else:
            return True

    def _upload_file(self, file, md5sum):
        if self.dry_run:
            return

        logger.info(f"Uploading file... ({file})")
        self.client.put_object(object_key=file, file_path=file, metadata={'md5sum': md5sum})
        logger.info(f"File is uploaded! ({file})")

    def _get_object_metadata(self, rel_file_path):
        return self.client.get_object(object_key=rel_file_path).metadata

    def set_bucket_name(self, bucket_name):
        logger.debug("Setting bucket name to {}".format(bucket_name))
        self.bucket_name = bucket_name
        self._reinitialize_client()

    def _reinitialize_client(self):
        logger.debug("Reinitializing S3Client, probably due to new bucket_name")
        self.client = S3Client(self.bucket_name)
