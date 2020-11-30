import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import UploadForm, ValidateBooth
from .models import Client, Photo, PhotoBooth, Paillasson
from .utils import get_session_key, verify_checksum, get_client_ip, get_random_string

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})


@csrf_exempt
def connexion(request):
    session_key = get_session_key(request)
    get_object_or_404(PhotoBooth, sessionkey=session_key)
    response = JsonResponse({"valid": True})
    response.status_code = 200  # Created
    return response


def new_connexion(request):
    ip_remote = get_client_ip(request)
    new_code_connexion = get_random_string(8)
    patient = Paillasson(
        ip=ip_remote,
        code_connexion=new_code_connexion,
        is_valid=False,
    )
    patient.save()
    response = JsonResponse({"code_connexion": patient.code_connexion})
    response.status_code = 201  # Created
    return response


def validate_connexion(request):
    if request.method == 'POST':
        form = ValidateBooth(request.POST)
        if form.is_valid():
            patient = get_object_or_404(Paillasson, code_connexion=form.cleaned_data['Code'])
            patient.is_valid = True
            patient.save()

            return HttpResponseRedirect('/')
    else:
        form = ValidateBooth()

    return render(request, 'form.html', {'form': form})

@csrf_exempt
def wait_connexion(request):
    ip_remote = get_client_ip(request)
    code_connexion = get_session_key(request)
    patient = get_object_or_404(Paillasson, code_connexion=code_connexion, ip=ip_remote)
    if not patient.is_valid:
        return HttpResponseForbidden()

    new_session_key = get_random_string(64)
    photomaton = PhotoBooth(
        nom="nouveau_photomaton",
        sessionkey=new_session_key,
        client=Client.objects.get(pk=1),
    )
    photomaton.save()
    patient.delete()
    response = JsonResponse({"is_valid": True, "session_key": photomaton.sessionkey})
    response.status_code = 201  # Created
    return response


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
