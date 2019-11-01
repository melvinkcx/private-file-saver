import os
import tempfile

import boto3
from moto import mock_s3

from core.s3_client import S3Client
from core.syncer import Syncer
from test.constants import REGION_NAME, BUCKET_NAME


@mock_s3
def test_scan_files():
    s3 = boto3.resource('s3', region_name=REGION_NAME)
    s3.create_bucket(Bucket=BUCKET_NAME)
    client = S3Client(BUCKET_NAME)
    syncer = Syncer()

    files_uploaded = []

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        num_of_file_uploaded = 0

        for i in range(1, 11):
            object_key = f"{i}{i}{i}"
            test_file = f"./{object_key}.txt"
            with open(test_file, "w") as f:
                f.write("XXXXXXXXXXX")

            if i % 2 == 0:
                num_of_file_uploaded += 1
                files_uploaded.append(object_key)
                client.put_object(object_key=object_key, file_path=test_file,
                                  metadata={'md5sum': 'xxxxxxxxxx'})

        # FIXME
        files = syncer.scan(tmpdirname)
        for file in files:
            if file[0] in files_uploaded:
                assert file[1] == 'FILE'
                assert file[2] == 'SYNCED'

        num_of_file_synced = len(list(filter(lambda x: x[2] == 'SYNCED', files)))
        assert num_of_file_synced == num_of_file_uploaded
