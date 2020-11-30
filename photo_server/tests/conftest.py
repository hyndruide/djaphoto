import pytest

from photo_backend import models


@pytest.fixture
def init_db(django_db_setup, django_db_blocker):
    key = "supersecret123"

    client1 = models.Client(nom="Super Client 1")
    client1.save()
    pb1 = models.PhotoBooth(client=client1, nom="Photomaton Salon", sessionkey=key)
    pb1.save()

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
    patient1 = models.Paillasson(
        ip="127.0.0.1",
        code_connexion="azertyui",
        is_valid=True,
        client=client1,
    )
    patient1.save()

    yield
