import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import UploadForm
from .models import Photo, PhotoBooth
from .utils import get_session_key, verify_checksum

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})


@csrf_exempt
@require_http_methods(["POST"])
def photo_upload(request):
    session_key = get_session_key(request)
    photomaton = get_object_or_404(PhotoBooth, sessionkey=session_key)

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        fp = form.cleaned_data["file"]
        checksum = form.cleaned_data["checksum"]
        created_at = form.cleaned_data["created_at"]
        name = form.cleaned_data["name"]

    # TODO: should use a Django Form to validate inputs
        if not verify_checksum(checksum, fp):
            return HttpResponseBadRequest("invalid checksum")

        fs = FileSystemStorage(name)
        filename = fs.save(name, fp)

        photo = Photo(
            lien=filename,
            date_create=created_at,
            photobooth=photomaton,
        )
        photo.save()

        response = JsonResponse({"id": photo.id})
        response.status_code = 201  # Created
        return response
    else:
        return HttpResponseBadRequest(form.errors)
