import webbrowser
from typing import Mapping

import webview

from core.configs import configs
from core.aws import test_credentials
from core.aws.s3 import S3Client
from core.downloader import BucketDownloader
from core.syncer import Syncer
from core.logging import logger


class FileApiMixin:
    # Window / Dialogs
    def open_folder_dialog(self):
        window = webview.windows[0]
        return window.create_file_dialog(webview.FOLDER_DIALOG)

    def open_file(self, kwargs):
        webbrowser.open(kwargs["file"])


class CommonApiMixin:
    def ping(self, kwargs):
        return "Pong"

    def is_initialized(self, kwargs):
        return self.config_manager.is_initialized()


class ConfigManagerApiMixin:
    # ConfigManager
    def list_configs(self, kwargs):
        return self.config_manager.all()

    def set_configs(self, values: Mapping[str, str]):
        configs = self.config_manager.set_many(values)
        self._reinitialize_clients()  # FIXME: Ugly
        return configs

    def list_configurables(self, kwargs):
        """
        :return: a list of configurable parameters
        """
        return self.config_manager.list_configurables()

    def select_target_path(self, kwargs):
        try:
            (path,) = self.open_folder_dialog()
            return self.set_configs({
                'TARGET_PATH': path
            })
        except TypeError:
            return False

    def reset_application(self, kwargs):
        logger.warning("Reset application initialized!")
        return self.config_manager.reset_configs()


class AWSApiMixin:
    # AWS
    def list_regions(self, kwargs):
        return self.s3_client.list_regions()

    def test_and_set_credentials(self, kwargs):
        try:
            response = test_credentials(
                kwargs["access_key_id"],
                kwargs["secret_access_key"],
                kwargs["region_name"]
            )
            if response.get("ok"):
                self.set_configs({
                    'AWS_ACCESS_KEY_ID': kwargs["access_key_id"],
                    'AWS_SECRET_ACCESS_KEY': kwargs["secret_access_key"],
                    'AWS_REGION': kwargs["region_name"],
                })

            return response
        except Exception as e:
            return e

    def list_buckets(self, kwargs):
        return self.s3_client.list_buckets()

    def set_default_bucket(self, kwargs):
        return self.set_configs({
            'DEFAULT_BUCKET_NAME': kwargs["bucket_name"]
        })


class SyncerApiMixin:
    # Syncer
    def scan(self, kwargs):
        if not self.syncer.has_bucket_name():
            self.syncer.set_bucket_name(
                self.config_manager.get("DEFAULT_BUCKET_NAME")
            )

        path = self.config_manager.get("TARGET_PATH") \
            if kwargs.get("path") is None \
            else kwargs["path"]
        logger.info(f"Scanning directory: {path}")

        return self.syncer.scan(path, recursive=False)

    def get_sync_status(self, kwargs):
        files = self.syncer.scan(recursive=True)
        synced = len(
            list(
                filter(lambda f: len(f) > 2 and f[2] in ("NOT_UPLOADED", "NOT_SYNCED"), files)
            )
        ) == 0
        logger.info(f"Target path scanned. Sync status: {'all synced' if synced else 'not synced'}")

        return {"synced": synced}

    def sync(self, kwargs):
        return self.syncer.sync()


class DownloaderApiMixin:
    def download_bucket(self, _):
        self.bucket_downloader.dump_bucket()


class CurrentLogMixin:
    def __init__(self):
        self._current_log = ""

    def get_current_log(self, _):
        log = self._current_log
        self._current_log = ""
        return log

    def set_current_log(self, value):
        self._current_log = value


class PFSApi(
    CurrentLogMixin,
    DownloaderApiMixin,
    SyncerApiMixin,
    AWSApiMixin,
    ConfigManagerApiMixin,
    CommonApiMixin,
    FileApiMixin
):
    """
    Caveat:
    - JS will send at least 1 positional argument.(None,)
    """

    def __init__(self):
        self.config_manager = configs
        self.syncer = Syncer()
        self.s3_client = S3Client()
        self.bucket_downloader = BucketDownloader()
        super().__init__()

    def _reinitialize_clients(self):
        self.syncer = Syncer()
        self.s3_client = S3Client()
        self.bucket_downloader = BucketDownloader()
