from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import datetime

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(request,"index.html", {"now": now})

@csrf_exempt
def photo_sync(request):
    if request.method == "POST" :
        fs = FileSystemStorage()
        for file in request.FILES:
            upfile = request.FILES[file]
            fs = FileSystemStorage()
            filename = fs.save(upfile.name, upfile)
    return HttpResponse()