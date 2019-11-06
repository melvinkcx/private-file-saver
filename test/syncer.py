import os
import tempfile

import boto3
import pytest
from moto import mock_s3

from core.aws.s3 import S3Client
from core.syncer import Syncer
from core.utils import calc_md5sum
from test.constants import REGION_NAME, BUCKET_NAME


@mock_s3
def test_scan_files():
    s3 = boto3.resource('s3', region_name=REGION_NAME)
    s3.create_bucket(Bucket=BUCKET_NAME)
    client = S3Client(BUCKET_NAME)
    syncer = Syncer(BUCKET_NAME)

    files_uploaded = []

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        num_of_file_uploaded = 0

        for i in range(1, 11):
            object_key = f"{i}{i}{i}.txt"
            test_file = f"./{object_key}"
            with open(test_file, "w") as f:
                f.write("XXXXXXXXXXX")

            if i % 2 == 0:
                num_of_file_uploaded += 1
                files_uploaded.append(object_key)
                client.put_object(object_key=object_key, file_path=test_file,
                                  metadata={'md5sum': calc_md5sum(test_file)})

            if i == 6:
                # Modify file `666.txt`
                with open(test_file, "w") as f:
                    f.write("yyyyyyyyyyyy")

        assert len(list(client.list_objects())) == 5 == num_of_file_uploaded

        files = syncer.scan(tmpdirname)

        for file in files:
            assert file[1] == 'FILE'

            if file[0] == "666.txt":
                assert file[2] == 'NOT_SYNCED'
            elif file[0] in files_uploaded:
                assert file[2] == 'SYNCED'
            else:
                assert file[2] == 'NOT_UPLOADED'

        num_of_file_synced = len(list(filter(lambda x: x[2] == 'SYNCED', files)))
        assert num_of_file_synced == 4


@pytest.mark.skip(reason="TODO: to be done later")
@mock_s3
def test_sync():
    pass
