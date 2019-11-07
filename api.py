from typing import Mapping

import webview

from core.aws import test_credentials
from core.aws.s3 import S3Client
from core.configs.manager import ConfigManager
from core.syncer import Syncer


class JsApi:
    """
    JsAPI is the JS correspondent to PythonAPI in view/api.js
    This is the interface Python communicates to our View layer (Frontend, Vue.js)

    Caveat:
    - JS will send at least 1 positional argument.(None,)
    """

    def __init__(self):
        self.config_manager = ConfigManager()
        self.s3_client = S3Client()
        self.syncer = Syncer()

    # Window / Dialogs
    def open_folder_dialog(self):
        window = webview.windows[0]
        return window.create_file_dialog(webview.FOLDER_DIALOG)


    def ping(self, kwargs):
        return "Pong"

    def is_initialized(self, kwargs):
        return self.config_manager.is_initialized()

    # ConfigManager
    def list_configs(self, kwargs):
        return self.config_manager.all()

    def set_configs(self, values: Mapping[str, str]):
        return self.config_manager.set_many(values)

    def list_configurables(self, kwargs):
        """
        :return: a list of configurable parameters
        """
        return self.config_manager.list_configurables()

    # AWS
    def list_regions(self, kwargs):
        return self.s3_client.list_regions()

    def test_and_set_credentials(self, kwargs):
        try:
            response = test_credentials(kwargs["access_key_id"], kwargs["secret_access_key"], kwargs["region_name"])
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

    def select_target_path(self, kwargs):
        try:
            (path, ) = self.open_folder_dialog()
            return self.set_configs({
                'TARGET_PATH': path
            })
        except TypeError as e:
            return False

    # Syncer
    def scan(self, kwargs):
        if kwargs.get("path") is None:
            path = self.config_manager.get("TARGET_PATH")

        return self.syncer.scan(path)

    def sync(self, kwargs):
        path = self.config_manager.get("TARGET_PATH")
        return self.syncer.sync(path)
