import pytest

from photo_backend import models


@pytest.fixture
def init_db(django_db_setup, django_db_blocker):
    key = "supersecret123"

    client1 = models.Client(nom="Super Client 1")
    client1.save()
    pb1 = models.PhotoBooth(client=client1, nom="Photomaton Salon")
    pb1.save()
    token1 = models.Token(
        access_token=key,
        refresh_token="youpipyi",
        token_type="bearer",
        expires=3600,
        photobooth=pb1
    )
    token1.save()

    yield


@pytest.fixture
def init_db_new_photobooth(django_db_setup, django_db_blocker):
    client1 = models.Client(nom="Super Client 1")
    client1.save()

    yield


@pytest.fixture
def init_db_validate_photobooth(django_db_setup, django_db_blocker):
    client1 = models.Client(nom="Super Client 1")
    client1.save()
    pb1 = models.PhotoBooth(client=client1, nom="Photomaton Salon")
    pb1.save()
    autorization1 = models.Authorization(
        client_id="superdevice",
        device_code="azertyui",
        user_code="qsdfghjk",
        is_validate=True,
        interval=0,
        expires_in=1800,
        photobooth=pb1,
    )
    autorization1.save()

    yield
