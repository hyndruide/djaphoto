import datetime

from django.shortcuts import render

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})
