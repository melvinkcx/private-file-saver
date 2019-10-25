import hashlib
import math

from configs import MULTIPART_THRESHOLD, CHUNK_SIZE


def calc_etag_whole(file):
    """
    Read chunk by chunk to reduce memory
    """
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(CHUNK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(CHUNK_SIZE)
    return '"{}"'.format(hasher.hexdigest())


def calc_etag_part(file, total_file_size):
    """
    References:
    - https://stackoverflow.com/a/43819225/10955067
    """
    acc_hasher = []
    number_of_parts = math.ceil(total_file_size / MULTIPART_THRESHOLD)

    # Calculate md5sum for each part
    for part in range(1, number_of_parts):
        hasher = hashlib.md5()
        if part == number_of_parts:  # Last part
            part_size = total_file_size % MULTIPART_THRESHOLD
        else:
            part_size = MULTIPART_THRESHOLD

        with open(file, 'rb') as afile:
            while max(part_size, 0) >= 0:
                buf = afile.read(CHUNK_SIZE)
                part_size -= CHUNK_SIZE
                hasher.update(buf)

        acc_hasher.append(hasher)

    hashsum = b''.join(h.digest() for h in acc_hasher)
    hashsum = hashlib.md5(hashsum)
    return '"{}-{}"'.format(hashsum.hexdigest(), number_of_parts)
