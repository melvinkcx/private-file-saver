import hashlib
import os

from core.configs import configs
from core.logging import logger


def calc_md5sum(rel_file_path):
    """
    Calculate md5sum
    Read chunk by chunk to reduce memory
    """
    logger.debug("Calculating md5sum for `{}`".format(rel_file_path))
    hasher = hashlib.md5()
    with open(rel_file_path, 'rb') as afile:
        buf = afile.read(configs.READ_CHUNK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(configs.READ_CHUNK_SIZE)
    return '{}'.format(hasher.hexdigest())


def get_last_modified(abs_file_path):
    """
    get last modified timestamp of file
    """
    return os.path.getmtime(abs_file_path)
