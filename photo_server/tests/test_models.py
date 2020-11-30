from datetime import datetime, timezone
import pytest
from photo_backend import models


@pytest.mark.django_db
def test_photo_str():

    date = datetime(2020, 11, 23, 21, 16, 00, tzinfo=timezone.utc)

    c = models.Client(nom="client")
    pb = models.PhotoBooth(nom="pb", client=c, sessionkey="kqslmqsk")

    c.save()
    pb.save()

    photo = models.Photo(
        lien="blabla",
        date_create=date,
        photobooth=pb,
    )
    photo.save()

    assert "blabla 23/11/2020, 22:16:00 CET" == str(photo)
