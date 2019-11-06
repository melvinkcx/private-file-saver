from typing import Mapping

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

    def ping(self, *args):
        return "Pong"

    def is_initialized(self, *args):
        return self.config_manager.is_initialized()

    # ConfigManager
    def list_configs(self, *args):
        return self.config_manager.all()

    def set_configs(self, values: Mapping[str, str]):
        return self.config_manager.set_many(values)

    def list_configurables(self):
        """
        :return: a list of configurable parameters
        """
        return self.config_manager.list_configurables()

    # AWS
    def list_regions(self, *args):
        return self.s3_client.list_regions()

    def test_and_set_credentials(self, access_key_id, secret_access_key, region_name):
        response = test_credentials(access_key_id, secret_access_key, region_name)
        if response.get("ok"):
            self.set_configs({
                'AWS_ACCESS_KEY_ID': access_key_id,
                'AWS_SECRET_ACCESS_KEY': secret_access_key,
                'AWS_REGION': region_name,
            })

        return response

    def list_buckets(self, *args):
        return self.s3_client.list_buckets()

    def set_default_bucket(self, bucket_name):
        return self.set_configs({
            'DEFAULT_BUCKET_NAME': bucket_name
        })

    def set_target_path(self, target_path):
        return self.set_configs({
            'TARGET_PATH': target_path
        })

    # Syncer
    def scan(self, path=None):
        if path is None:
            path = self.config_manager.get("TARGET_PATH")

        return self.syncer.scan(path)

    def sync(self):
        path = self.config_manager.get("TARGET_PATH")
        return self.syncer.sync(path)
