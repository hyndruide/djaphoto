import pytest
import os
from emu_photomaton.sync_photo import BoothClient


@pytest.mark.django_db
def test_connect_without_first(live_server, init_db):
    if os.path.exists("keyfile"):
        os.remove("keyfile")
    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    assert False is res


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
    res = client.connect()

    assert res == {"valid": True}
    assert res["valid"] 


@pytest.mark.django_db
def test_connect(live_server, init_db):
    url = live_server.url
    session_key = "supersecret123"
    client = BoothClient(url)
    client.store_key(session_key)
    res = client.connect()
    assert "valid" in res


@pytest.mark.django_db
def test_send_file(live_server, init_db):
    url = live_server.url
    session_key = "supersecret123"
    client = BoothClient(url)
    client.store_key(session_key)
    res = client.upload("photo_server/emu_photomaton/photo1.jpg")

    assert "id" in res

# TO DO def test_setup_photomaton(live_server, init_db):
