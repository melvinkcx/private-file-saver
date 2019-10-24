"""
Configurations
"""
import os

try:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_REGION = os.environ['AWS_DEFAULT_REGION']
except KeyError as e:
    raise RuntimeError("AWS credentials are not found")

