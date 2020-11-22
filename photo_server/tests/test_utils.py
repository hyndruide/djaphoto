import io

from photo_backend import utils


def test_verify_checkum():
    fp = io.BytesIO(b"lalala some bits like a JPG")
    pos = fp.tell()
    expected = "sha1:559548d6c9dedb8e6e8696590911d1f64d633aa5"

    assert utils.verify_checksum(expected, fp)
    assert pos == fp.tell()


def test_verify_checkum_unknown_algo():
    fp = io.BytesIO(b"lalala some bits like a JPG")
    pos = fp.tell()
    expected = "toto:qsdklm"

    assert not utils.verify_checksum(expected, fp)
    assert pos == fp.tell()


def test_verify_checkum_bad_inputs():
    fp = io.BytesIO(b"lalala some bits like a JPG")
    pos = fp.tell()
    expected = "jkqlsdjkqlsd"

    assert not utils.verify_checksum(expected, fp)
    assert pos == fp.tell()
