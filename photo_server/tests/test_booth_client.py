import json
import pytest
import os
from emu_photomaton.sync_photo import BoothClient


@pytest.mark.django_db
def test_connect_without_first(live_server, init_db):
    if os.path.exists("setting"):
        os.remove("setting")
    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    assert False is res


@pytest.mark.django_db
def test_first_connect(live_server, init_db_new_photobooth):
    url = live_server.url
    client = BoothClient(url)
    r = client._first_connect()
    assert "device_code" in r


@pytest.mark.django_db
def test_first_validate_connect(live_server, init_db_validate_photobooth):
    setting = {"client_id": "superdevice"}
    with open('setting', 'w') as f1:
        json.dump(setting, f1)
    url = live_server.url
    client = BoothClient(url)
    dt = {
        "device_code": "azertyui",
        "user_code": "qsdf-ghjk",
        "verification_uri": "http://127.0.0.1/photobooth/validate/",
        "interval": 0,
        "expires_in": 1800
    }
    val = client.wait_first_connect(dt)

    assert val == False


@pytest.mark.django_db
def test_connect(live_server, init_db):
    setting = {"client_id": "superdevice"}
    setting['token'] = {
        "access_token": "supersecret123",
        "refresh_token": "youpipyi",
        "token_type": "bearer",
        "expires": 3600,
    }
    with open('setting', 'w') as f1:
        json.dump(setting, f1)

    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    assert "valid" in res


@pytest.mark.django_db
def test_send_file(live_server, init_db):
    setting = {"client_id": "superdevice"}
    setting['token'] = {
        "access_token": "supersecret123",
        "refresh_token": "youpipyi",
        "token_type": "bearer",
        "expires": 3600,
    }
    with open('setting', 'w') as f1:
        json.dump(setting, f1)

    url = live_server.url
    client = BoothClient(url)
    res = client.upload("photo_server/emu_photomaton/photo1.jpg")

    assert "id" in res

# TO DO def test_setup_photomaton(live_server, init_db):
