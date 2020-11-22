import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Photo, PhotoBooth
from .utils import verify_checksum

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})


@csrf_exempt
@require_http_methods(["POST"])
def photo_upload(request):
    session_key = request.headers["Authorization"]  # TODO: check if authorization is here
    photomaton = get_object_or_404(PhotoBooth, sessionkey=session_key)

    # TODO: should use a Django Form to validate inputs
    checksum = request.POST["checksum"]
    fp = request.FILES["file"]

    print(f"size = {fp.size}")

    if not verify_checksum(checksum, fp):
        return HttpResponseBadRequest("invalid checksum")

    fs = FileSystemStorage()
    filename = fs.save(request.POST["name"], fp)

    photo = Photo(
        lien=filename,
        date_create=request.POST["created_at"],
        photobooth=photomaton,
    )
    photo.save()

    response = JsonResponse({"id": photo.id})
    response.status_code = 201  # Created
    return response
