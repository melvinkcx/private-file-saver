import hashlib

from core.configs import CHUNK_SIZE
from core.log_utils import logger


def calc_md5sum(file):
    """
    Read chunk by chunk to reduce memory
    """
    logger.debug("Calculating md5sum for `{}`".format(file))
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(CHUNK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(CHUNK_SIZE)
    return '{}'.format(hasher.hexdigest())
