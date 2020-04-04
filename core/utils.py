import hashlib

from core.configs import configs
from core.logging import logger


def calc_md5sum(file):
    """
    Calculate md5sum
    Read chunk by chunk to reduce memory
    """
    logger.debug("Calculating md5sum for `{}`".format(file))
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(configs.READ_CHUNK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(configs.READ_CHUNK_SIZE)
    return '{}'.format(hasher.hexdigest())


def get_last_modified(file):
    """
    TODO
    get last modified timestamp of file
    """
    pass
