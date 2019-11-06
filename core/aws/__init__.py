import boto3
from botocore.exceptions import ClientError


def test_credentials(access_key_id, secret_access_key, region_name):
    """
    test if credential has proper access

    Caveat:
    - this only tests if key pair has access to s3:listBucket
    """
    client = boto3.resource('s3', **{
        "aws_access_key_id": access_key_id,
        "aws_secret_access_key": secret_access_key,
        "region_name": region_name
    })
    try:
        client.buckets.all()
    except ClientError as e:
        if e.response["Error"]["Code"] == 'AccessDenied':
            return e.response  # dict<Type, Code, Message>
    else:
        return {
            "ok": True
        }
