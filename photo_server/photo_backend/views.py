from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import datetime
import hashlib
import os


def calculate_checksum(filenames):
    hash = hashlib.md5()
    for fn in filenames:
        print(fn)
        if os.path.isfile(fn):

            hash.update(open(fn, "rb").read())
    return hash.hexdigest()

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(request,"index.html", {"now": now})


@csrf_exempt
def photo_sync(request):
    filenames = []
    if request.method == "POST" : 
        crchash_remote = request.POST.get('crcfiles')
        fs = FileSystemStorage()
        for file in request.FILES:
            upfile = request.FILES[file]
            fs = FileSystemStorage()
            filename = fs.save(upfile.name, upfile)
            filenames.append(str(os.path.join(settings.MEDIA_ROOT,filename) ))
        crchash_local = calculate_checksum(filenames)
        if crchash_remote == crchash_local : 
            return HttpResponse()
        else : 
            for file in filenames : 
                os.remove(file)
            return  HttpResponseBadRequest()
