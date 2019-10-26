from unittest import TestCase

from moto import mock_s3

from core import configs
from core.s3_client import S3Client


class S3ClientTestSuite(TestCase):
    client = None

    def setUpClass(cls) -> None:
        # TODO set up environ
        pass

    def setUp(self):
        self.client = S3Client()

    def test_s3_client_properly_regards_transfer_config(self):
        c_tc = self.client.transfer_config
        assert c_tc.multipart_chunksize == configs.MULTIPART_CHUNKSIZE, "S3Client does not regard MULTIPART_CHUNKSIZE config"
        assert c_tc.max_concurrency == configs.MAX_CONCURRENCY, "S3Client does not regard MULTIPART_THRESHOLD config"

    def test_list_buckets(self):
        with mock_s3():
            buckets = self.client.list_buckets()
