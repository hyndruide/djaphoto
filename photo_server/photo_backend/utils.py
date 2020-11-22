import hashlib
import os


def calculate_checksum(path, filenames):
    hash = hashlib.md5()
    for fn in filenames:
        fn = os.path.join(path, fn)

        if os.path.isfile(fn):
            hash.update(open(fn, "rb").read())
    return hash.hexdigest()


def verify_checksum(checksum, fp):
    try:
        kind, expected = checksum.split(":", 1)
    except ValueError:  # no ":" in checksum
        return False

    if kind != "sha1":
        return False

    pos = fp.tell()
    computed = hashlib.sha1(fp.read()).hexdigest()
    fp.seek(pos)
    return expected == computed
