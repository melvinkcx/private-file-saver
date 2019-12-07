import multiprocessing

from core.configs import configs
from core.log_utils import logger


class BucketDownloader:
    """
    Downloader
    A service that fetch list of objects from S3 and orchestrates download of files
    """

    def __init__(self, target_path):
        self._target_path = target_path
        self._max_workers = configs.MAX_CONCURRENCY
        self._dry_run = True

        self._download_queue = multiprocessing.JoinableQueue()  # Objects to be downloaded
        self._files_to_be_downloaded = multiprocessing.Semaphore(value=0)

    def dump_bucket(self, bucket_name, dry_run=False):
        """
        TODO
        Create download workers
        Fetch and organize a list of Objects to be downloaded
        pass to workers
        """
        self._dry_run = dry_run
        _download_workers = [multiprocessing.Process(target=self._download_file) for _ in range(self._max_workers)]

        # TODO list objects in bucket, then scan local for it

    def _download_file(self):
        while self._files_to_be_downloaded.acquire():
            queue_item = self._download_queue.get()
            if queue_item is None:
                break  # A sentinel value to quit the loop

            if self._dry_run:
                return

            logger.info(f"Downloading file... ({queue_item})")
            # TODO Download file here
            self._download_queue.task_done()
