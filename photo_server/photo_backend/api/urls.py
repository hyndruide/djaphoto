from django.urls import path

from .views import *


urlpatterns = [
    path("upload", photo_upload),
    path("connect", connect_photobooth),
    path("new", new_photobooth),
    path("wait", wait_photobooth),
]