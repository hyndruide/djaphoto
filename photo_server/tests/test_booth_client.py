import pytest
from emu_photomaton.sync_photo import BoothClient


@pytest.mark.django_db
def test_first_connect(live_server, init_db_new_photobooth):
    url = live_server.url
    client = BoothClient(url)
    r = client._first_connect()
    assert "code_connexion" in r


@pytest.mark.django_db
def test_first_validate_connect(live_server, init_db_validate_photobooth):
    url = live_server.url
    client = BoothClient(url)
    client.wait_first_connect("azertyui")
    print(client.session_key)
    assert None is not client.session_key


@pytest.mark.django_db
def test_send_file(live_server, init_db):
    url = live_server.url
    session_key = "supersecret123"
    client = BoothClient(url)
    client.store_key(session_key)
    res = client.upload("photo_server/emu_photomaton/photo1.jpg")

    assert "id" in res

# TO DO def test_setup_photomaton(live_server, init_db):
