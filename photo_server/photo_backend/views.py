from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(request,"index.html", {"now": now})