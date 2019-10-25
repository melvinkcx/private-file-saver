"""
Configurations
"""
import multiprocessing
import os

from log_utils import logger

# AWS Config
try:
    logger.info("Checking for AWS configurations")
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_REGION = os.environ['AWS_DEFAULT_REGION']
except KeyError as e:
    raise RuntimeError("AWS credentials are not found")

# Transfer Config
CHUNK_SIZE = 8 * 1024  # 8KB
MULTIPART_THRESHOLD = 1 * 1024 ** 2  # 1MB
MAX_CONCURRENCY = multiprocessing.cpu_count()
logger.info("Thread count: {}".format(MAX_CONCURRENCY))

# Default Bucket Name
DEFAULT_BUCKET_NAME = 'dev-purpose-only-25529f3cw53v'

# Target Path, should be an absolute path
TARGET_PATH = '/home/melvin/Project/secret-bucket/target_folder'
