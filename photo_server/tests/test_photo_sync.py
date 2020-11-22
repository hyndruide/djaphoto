import hashlib

import pytest


@pytest.mark.django_db
def test_sync_photo(client, init_db):

    key = "supersecret123"
    auth = f"bearer {key}"

    filename = "photo_server/emu_photomaton/photo1.jpg"
    with open(filename, "rb") as fp:
        checksum = hashlib.sha1(fp.read()).hexdigest()

    with open(filename, "rb") as fp:
        data = {
            "name": "ma-photo1.jpg",
            "created_at": "2020-11-22T17:44:49+00:00",
            "checksum": f"sha1:{checksum}",
            "file": fp,
        }

        response = client.post("/photo/upload", data, HTTP_AUTHORIZATION=auth)
        assert 201 == response.status_code
