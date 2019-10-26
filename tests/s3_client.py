from moto import mock_s3


class S3ClientTestSuite:
    def test_get_object_metadata(self):
        with mock_s3():
            pass
