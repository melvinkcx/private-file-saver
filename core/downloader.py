import multiprocessing
import os

from core.aws.s3 import S3Client
from core.configs import configs
from core.log_utils import logger


class BucketDownloader:
    """
    Downloader
    A service that fetch list of objects from S3 and orchestrates download of files
    """

    def __init__(self, bucket_name=None):
        """
        FIXME This is not a good design,
        let's make passing config explicit
        instead of reading during instantiation
        """
        self._target_path = configs.TARGET_PATH
        self._max_workers = configs.MAX_CONCURRENCY
        self._bucket_name = bucket_name or configs.DEFAULT_BUCKET_NAME
        self._s3_client = S3Client(bucket_name=self._bucket_name)

        self._dry_run = True

        self._download_queue = multiprocessing.JoinableQueue()  # Objects to be downloaded
        self._files_to_be_downloaded = multiprocessing.Semaphore(value=0)

    def dump_bucket(self, dry_run=False):
        """
        Create download workers
        Fetch and organize a list of Objects to be downloaded
        pass to workers
        """
        self._dry_run = dry_run
        _download_workers = [multiprocessing.Process(target=self._download_file) for _ in range(self._max_workers)]
        [w.start() for w in _download_workers]

        _objects = self._s3_client.list_objects()
        for _obj in _objects:
            if not self._is_file_exists(_obj.key):
                self._download_queue.put(_obj.key)
                self._files_to_be_downloaded.release()

        # Telling workers to stop
        for _ in self._max_workers:
            self._download_queue.put(None)
            self._files_to_be_downloaded.release()

        # Joining workers
        [w.join() for w in _download_workers]

    def _download_file(self):
        while self._files_to_be_downloaded.acquire():
            object_key = self._download_queue.get()
            if object_key is None:
                break  # A sentinel value to quit the loop

            if self._dry_run:
                return

            logger.info(f"Downloading file... ({object_key})")

            _file_path = os.path.abspath(os.path.join(self._target_path, object_key))
            _dir_name = os.path.dirname(_file_path)
            os.makedirs(_dir_name, exist_ok=True)

            self._s3_client.download_object(object_key=object_key, file_path=_file_path)

            self._download_queue.task_done()

    def _is_file_exists(self, file_path):
        file_path = os.path.join(self._target_path, file_path)
        return os.path.exists(file_path)
