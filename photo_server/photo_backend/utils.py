import hashlib
import os


def calculate_checksum(path,filenames):
    hash = hashlib.md5()
    for fn in filenames:
        fn = os.path.join(path,fn)

        if os.path.isfile(fn):
            hash.update(open(fn, "rb").read())
    return hash.hexdigest()
