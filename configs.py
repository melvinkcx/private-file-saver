"""
Configurations
"""
import os
import multiprocessing

# AWS Config
try:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_REGION = os.environ['AWS_DEFAULT_REGION']
except KeyError as e:
    raise RuntimeError("AWS credentials are not found")

# Transfer Config
CHUNK_SIZE = 8 * 1024
MULTIPART_THRESHOLD = 1 * 1024 ** 3  # 1GB
MAX_CONCURRENCY = multiprocessing.cpu_count()

# Default Bucket Name
DEFAULT_BUCKET_NAME = 'dev-purpose-only-25529f3cw53v'
