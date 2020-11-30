import hashlib
import random
import string
import os

from django.core.exceptions import PermissionDenied


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


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


def get_session_key(request):
    authorization = request.headers.get("authorization", "")
    if authorization.startswith("bearer "):
        return authorization.split(" ", 1)[1]
    else:
        raise PermissionDenied


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
