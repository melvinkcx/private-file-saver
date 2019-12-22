import glob
import os
import multiprocessing
from os.path import isfile, isdir

from botocore.exceptions import ClientError

from core.configs import configs
from core.logging import logger
from core.aws.s3 import S3Client
from core.utils import calc_md5sum


class Syncer:
    def __init__(self, bucket_name=None, target_path=None, max_workers=None, s3_client=None):
        self._target_path = target_path or configs.TARGET_PATH
        self._bucket_name = bucket_name or configs.DEFAULT_BUCKET_NAME

        assert max_workers is None or max_workers > 0, "max_workers must not be less than 1"
        self._max_workers = max_workers or configs.MAX_CONCURRENCY

        self._client = s3_client or S3Client(self._bucket_name)

        self._dry_run = False

        self._upload_queue = multiprocessing.JoinableQueue()  # Files to be uploaded
        self._files_to_be_uploaded = multiprocessing.Semaphore(value=0)

    def scan(self, path=None, recursive=False, file_pattern="**"):
        if path is None:
            path = self._target_path

        target_directory = os.path.abspath(path)
        logger.info(f"Target directory: {target_directory}")
        os.chdir(target_directory)

        # Derive object name by diffing current_directory and root_path
        object_prefix = os.path.relpath(target_directory, self._target_path)
        object_prefix = f"{object_prefix}/" if object_prefix is not "." else ""

        files_iter = glob.iglob(file_pattern, recursive=recursive)
        files = []
        for file in files_iter:
            if isdir(file):
                files.append((file, 'DIRECTORY'))

            if isfile(file):
                md5sum_local = calc_md5sum(file)

                if not self._is_object_exists(f"{object_prefix}{file}"):
                    # File not in Bucket
                    files.append((file, 'FILE', 'NOT_UPLOADED'))
                else:
                    # File is in Bucket
                    metadata_remote = self._get_object_metadata(f"{object_prefix}{file}")
                    md5sum_remote = metadata_remote.get('md5sum', None)

                    if md5sum_local != md5sum_remote:
                        # File is not synced
                        files.append((file, 'FILE', 'NOT_SYNCED'))
                    else:
                        # File is synced
                        files.append((file, 'FILE', 'SYNCED'))

        return files

    def sync(self, path=None, dry_run=False, recursive=True, file_pattern="**"):
        """
        Scan the directory of interest
        """
        self._dry_run = dry_run
        logger.info("Dry run is {}".format("on" if dry_run else "off"))

        # Set path
        if path is None:
            path = self._target_path

        # Navigate to target directory
        target_directory = os.path.abspath(path)
        logger.info(f"Target directory: {target_directory}")
        os.chdir(target_directory)

        # Create uploaded worker
        _upload_workers = [multiprocessing.Process(target=self._upload_file) for _ in range(self._max_workers)]
        [p.start() for p in _upload_workers]

        # Scan directories
        files_iter = glob.iglob(file_pattern, recursive=recursive)
        for file in files_iter:
            if isfile(file):
                md5sum_local = calc_md5sum(file)

                # File not in Bucket
                if not self._is_object_exists(file):
                    logger.debug("File doesn't exist, queuing file.. ({})".format(file))
                    self._upload_queue.put((file, md5sum_local))
                    self._files_to_be_uploaded.release()
                else:
                    # File is in Bucket
                    metadata_remote = self._get_object_metadata(file)
                    md5sum_remote = metadata_remote.get('md5sum', None)
                    if md5sum_local != md5sum_remote:  # Upload file if sync required
                        logger.info("Etags mismatched. File is being queued ({})".format(file))
                        self._upload_queue.put((file, md5sum_local))
                        self._files_to_be_uploaded.release()

        # Joining queues and upload workers
        for _ in range(self._max_workers):
            self._upload_queue.put(None)
            self._files_to_be_uploaded.release()

        [p.join() for p in _upload_workers]

    def _is_object_exists(self, rel_file_path) -> bool:
        try:
            self._get_object_metadata(rel_file_path=rel_file_path)
        except ClientError as e:
            if e.response["Error"]["Code"] == '404':
                return False
            raise e
        else:
            return True

    def _upload_file(self):
        while self._files_to_be_uploaded.acquire():
            queue_item = self._upload_queue.get()
            if queue_item is None:
                break  # A sentinel value to quit the loop

            file, md5sum = queue_item

            if self._dry_run:
                return

            logger.info(f"Uploading file... ({file})")
            self._client.put_object(object_key=file,
                                    file_path=self._get_abs_file_path(file),
                                    metadata={'md5sum': md5sum})
            logger.info(f"File is uploaded! ({file})")
            self._upload_queue.task_done()

    def _get_object_metadata(self, rel_file_path):
        return self._client.get_object(object_key=rel_file_path).metadata

    def _get_abs_file_path(self, file_name):
        if os.path.isabs(file_name):
            return file_name
        return os.path.join(self._target_path, file_name)

    def set_bucket_name(self, bucket_name):
        logger.debug("Setting bucket name to {}".format(bucket_name))
        self._bucket_name = bucket_name
        self._reinitialize_client()

    def has_bucket_name(self):
        return bool(self._bucket_name)

    def _reinitialize_client(self):
        logger.debug("Reinitializing S3Client, probably due to new bucket_name")
        self._client = S3Client(self._bucket_name)
