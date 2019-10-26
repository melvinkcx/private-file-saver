from moto import mock_s3


class SyncerTestSuite:
    def test_get_object_metadata(self):
        with mock_s3():
            pass
