import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(request, "index.html", {"now": now})
