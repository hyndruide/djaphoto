from datetime import datetime, timezone
import pytest
from photo_backend import models


@pytest.mark.django_db
def test_photo_str():

    date = datetime(2021, 1, 6, 17, 7, 00, tzinfo=timezone.utc)

    c = models.Client(nom="client")
    pb = models.PhotoBooth(nom="pb", client=c)


    c.save()
    pb.save()


    photo = models.Photo(
        photo="media/photo/PHOTO_04-01-2021_092334.jpg",
        date_create=date,
        photobooth=pb,
    )
    photo.save()

    assert "media/photo/PHOTO_04-01-2021_092334.jpg 06/01/2021, 18:07:00 CET" == str(photo)
