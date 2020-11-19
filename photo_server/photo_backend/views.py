
import datetime
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Photo, PhotoBooth
from .utils import calculate_checksum



# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})


@csrf_exempt
def photo_sync(request):
    filenames = []
    if request.method == "POST":
        photomaton_id = request.POST.get("photomatonId")
        session_key = request.POST.get("sessionKey")
        creates_time = request.POST.getlist("creates_time")
        print(creates_time)
        photomaton = PhotoBooth.objects.get(pk=photomaton_id)
        if photomaton.sessionkey != session_key:
            return HttpResponseForbidden()

        crchash_remote = request.POST.get("crcFiles")

        fs = FileSystemStorage()
        for file in request.FILES:
            upfile = request.FILES[file]
            fs = FileSystemStorage()
            filename = fs.save(upfile.name, upfile)
            filenames.append(filename)
        crchash_local = calculate_checksum(settings.MEDIA_ROOT, filenames)

        if crchash_remote == crchash_local:
            for filename, date in zip(filenames, creates_time):
                print(date)
                photo = Photo(
                    lien=filename,
                    date_create=datetime.datetime.fromtimestamp(float(date)),
                    photobooth=PhotoBooth.objects.get(pk=photomaton_id),
                )
                photo.save()
            return HttpResponse()
        else:
            for filename in filenames:
                os.remove(os.path.join(settings.MEDIA_ROOT, filename))
            return HttpResponseBadRequest()
