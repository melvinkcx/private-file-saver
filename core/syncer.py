import glob
import multiprocessing
import os
import time
from os.path import isfile, isdir

from botocore.exceptions import ClientError

from core.aws.s3 import S3Client
from core.configs import configs
from core.logging import logger
from core.meta import MetaStore
from core.utils import calc_md5sum, get_last_modified


class Syncer:
    def __init__(self, bucket_name=None, target_path=None, max_workers=None, s3_client=None):
        self._target_path = target_path or configs.TARGET_PATH
        self._bucket_name = bucket_name or configs.DEFAULT_BUCKET_NAME

        assert max_workers is None or max_workers > 0, "max_workers must not be less than 1"
        self._max_workers = max_workers or configs.MAX_CONCURRENCY

        self._client = s3_client or S3Client(self._bucket_name)
        self._meta_store = MetaStore(db_path=self._target_path,
                                     target_path=self._target_path)

        self._dry_run = False

        self._upload_queue = multiprocessing.JoinableQueue()  # Files to be uploaded
        self._files_to_be_uploaded = multiprocessing.Semaphore(value=0)

    def scan(self, path=None, recursive=False, file_pattern="**"):
        """
        Scan and determine sync status of each file in
        `path` without syncing them to S3
        """
        if path is None:
            path = self._target_path

        target_directory = os.path.abspath(path)
        logger.info(f"Target directory: {target_directory}")

        # Always start from the target path (aka the location of the bucket)
        os.chdir(self._target_path)

        # Derive object name by diffing current_directory and root_path
        object_prefix = os.path.relpath(target_directory, self._target_path)
        object_prefix = f"{object_prefix}/" if object_prefix is not "." else ""

        files_iter = glob.iglob(f"{object_prefix}{file_pattern}", recursive=recursive)
        files = []
        for rel_file_path in files_iter:
            if isdir(rel_file_path):
                files.append((os.path.basename(rel_file_path), 'DIRECTORY'))

            elif self._is_metastore(rel_file_path):
                # Ignore metastore file
                pass

            elif isfile(rel_file_path):
                # 1. Check if file is in bucket
                if not self._is_object_exists(rel_file_path):
                    # File not in Bucket
                    files.append((os.path.basename(rel_file_path), 'FILE', 'NOT_UPLOADED'))

                # 2. Check last synced
                elif self._get_last_synced(rel_file_path) >= \
                        get_last_modified(abs_file_path=os.path.abspath(rel_file_path)):
                    files.append((os.path.basename(rel_file_path), 'FILE', 'SYNCED'))

                # 3. Check if md5sum match
                else:
                    # File is in Bucket
                    md5sum_local = calc_md5sum(rel_file_path)

                    metadata_remote = self._get_object_metadata(rel_file_path)
                    md5sum_remote = metadata_remote.get('md5sum', None)

                    if md5sum_local != md5sum_remote:
                        # File is not synced
                        files.append((os.path.basename(rel_file_path), 'FILE', 'NOT_SYNCED'))
                    else:
                        # File is synced
                        # Update last_synced, since at this point,
                        # it is apparent that it has been upload
                        # but the entry is missing from metastore
                        self._set_last_synced(rel_file_path=rel_file_path)
                        files.append((os.path.basename(rel_file_path), 'FILE', 'SYNCED'))

        return files

    def sync(self, dry_run=False, recursive=True, file_pattern="**"):
        """
        Scan and upload files in `path` if md5 mismatch
        """
        self._dry_run = dry_run
        logger.info("Dry run is {}".format("on" if dry_run else "off"))

        # Navigate to target directory
        target_directory = os.path.abspath(self._target_path)
        logger.info(f"Target directory: {target_directory}")
        os.chdir(target_directory)

        # Create uploaded worker
        _upload_workers = [multiprocessing.Process(target=self._upload_file_task)
                           for _ in range(self._max_workers)]
        [p.start() for p in _upload_workers]

        # Scan directories
        files_iter = glob.iglob(file_pattern, recursive=recursive)
        for rel_file_path in files_iter:
            if self._is_metastore(rel_file_path):
                # Ignore metastore file
                pass

            elif isfile(rel_file_path):
                # 1. Get last synced
                if not self._is_object_exists(rel_file_path):
                    logger.debug("File doesn't exist, queuing file.. ({})".format(rel_file_path))
                    md5sum_local = calc_md5sum(rel_file_path)
                    self._upload_queue.put((rel_file_path, md5sum_local))
                    self._files_to_be_uploaded.release()

                # 2. File is not in bucket -> Upload and set last_synced
                elif self._get_last_synced(rel_file_path) >= \
                        get_last_modified(abs_file_path=os.path.abspath(rel_file_path)):
                    # No need to sync -> Do nothing
                    pass

                # 3. File is in the bucket -> Check if md5sum match
                else:
                    md5sum_local = calc_md5sum(rel_file_path)
                    metadata_remote = self._get_object_metadata(rel_file_path)
                    md5sum_remote = metadata_remote.get('md5sum', None)

                    if md5sum_local != md5sum_remote:  # Upload file if sync required
                        logger.debug("Etags mismatched. File is being queued ({})".format(rel_file_path))
                        self._upload_queue.put((rel_file_path, md5sum_local))
                        self._files_to_be_uploaded.release()

                    else:
                        self._set_last_synced(rel_file_path=rel_file_path)

        # Joining queues and workers
        for _ in range(self._max_workers):
            self._upload_queue.put(None)
            self._files_to_be_uploaded.release()

        [p.join() for p in _upload_workers]

    def _get_last_synced(self, rel_file_path):
        """
        Get sync status from MetaStore
        """
        (_, last_synced) = self._meta_store.get_last_synced(
            rel_file_path=rel_file_path
        )
        return last_synced

    def _set_last_synced(self, rel_file_path, last_synced="CURRENT_TIME"):
        """
        Set sync status in MetaStore
        """
        if not last_synced or last_synced == "CURRENT_TIME":
            last_synced = time.time()

        return self._meta_store.set_last_synced(
            rel_file_path=rel_file_path,
            last_synced=last_synced
        )

    def _is_metastore(self, rel_file_path):
        return self._meta_store.is_metastore(
            os.path.join(self._target_path, rel_file_path)
        )

    def _is_object_exists(self, rel_file_path) -> bool:
        try:
            self._get_object_metadata(rel_file_path=rel_file_path)
        except ClientError as e:
            if e.response["Error"]["Code"] == '404':
                return False
            raise e
        else:
            return True

    def _upload_file_task(self):
        while self._files_to_be_uploaded.acquire():
            queue_item = self._upload_queue.get()
            if queue_item is None:
                break  # A sentinel value to quit the loop

            rel_file_path, md5sum = queue_item

            self._upload_file(rel_file_path=rel_file_path, md5sum=md5sum)
            self._upload_queue.task_done()

    def _upload_file(self, rel_file_path, md5sum):
        if self._dry_run:
            return

        logger.info(f"Uploading file... ({rel_file_path})")
        self._client.put_object(object_key=rel_file_path,
                                file_path=self._get_abs_file_path(rel_file_path),
                                metadata={'md5sum': md5sum})
        self._set_last_synced(rel_file_path=rel_file_path)
        logger.info(f"File is uploaded! ({rel_file_path})")

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
