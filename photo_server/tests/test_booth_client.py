import json
import pytest
import os
from emu_photomaton.sync_photo import BoothClient


@pytest.mark.django_db
def test_connect_without_first(live_server, init_db):
    if os.path.exists("setting"):
        os.remove("photobooth/json/key")
    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    assert False is res


@pytest.mark.django_db
def test_first_connect(live_server, init_db_new_photobooth):
    url = live_server.url
    client = BoothClient(url)
    client.first_connect()
    assert "device_code" in client.req


@pytest.mark.django_db
def test_first_validate_connect(live_server, init_db_validate_photobooth):
    url = live_server.url
    client = BoothClient(url)
    client.first_connect()
    client.client_id = "superdevice"
    client.req['device_code'] = "azertyui"
    client.req["grant_type"] = ""
    val = client.ask_first_connect()

    assert val == False


@pytest.mark.django_db
def test_connect(live_server, init_db):
    setting = {"client_id": "superdevice",
               "token" :{
                        "access_token": "supersecret123",
                        "refresh_token": "youpipyi",
                        "token_type": "bearer",
                        "expires": 3600
    } }
    with open('photobooth/json/key', 'w') as f1:
        json.dump(setting, f1)
    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    assert "valid" in res


@pytest.mark.django_db
def test_send_file(live_server, init_db):
    setting = {"client_id": "superdevice",
               "token" :{
                        "access_token": "supersecret123",
                        "refresh_token": "youpipyi",
                        "token_type": "bearer",
                        "expires": 3600
    } }
    with open('photobooth/json/key', 'w') as f1:
        json.dump(setting, f1)

    url = live_server.url
    client = BoothClient(url)
    res = client.connect()
    res = client.upload("photo_server/emu_photomaton/photo1.jpg")

    assert "id" in res

# TO DO def test_setup_photomaton(live_server, init_db):
