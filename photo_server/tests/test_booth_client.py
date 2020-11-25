import pytest

from emu_photomaton.sync_photo import BoothClient


@pytest.mark.django_db
def test_send_file(live_server, init_db):
    url = live_server.url
    session_key = "supersecret123"

    client = BoothClient(url, session_key)
    res = client.upload("photo_server/emu_photomaton/photo1.jpg")

    assert "id" in res


# TO DO def test_setup_photomaton(live_server, init_db):

