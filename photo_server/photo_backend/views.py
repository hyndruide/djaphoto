import datetime

from django.core.files.storage import FileSystemStorage
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import UploadForm, ValidateBooth
from .models import Client, Photo, PhotoBooth, Authorization, Token
from .utils import get_access_token, get_random_string

# Create your views here.


def first(request):
    now = datetime.datetime.now()
    return render(request, "index.html", {"now": now})


@csrf_exempt
def connect_photobooth(request):
    access_token = get_access_token(request)
    print(access_token)
    get_object_or_404(Token, access_token=access_token)
    response = JsonResponse({"valid": True})
    response.status_code = 200
    return response

@csrf_exempt
def new_photobooth(request):
    client_id = request.POST.get('client_id')
    auth_for_photomaton = Authorization(
        client_id=client_id,
        device_code=get_random_string(39),
        user_code=get_random_string(8),
        interval=5,
        expires_in=1800
    )
    auth_for_photomaton.save()
    response = JsonResponse({
        "device_code": auth_for_photomaton.device_code,
        "user_code": auth_for_photomaton.user_code[:4] + "-" + auth_for_photomaton.user_code[4:],
        "verification_uri": "http://127.0.0.1/photobooth/validate/",
        "interval": auth_for_photomaton.interval,
        "expires_in": auth_for_photomaton.expires_in
    })
    response.status_code = 200
    return response


def validate_photobooth(request):
    if request.method == 'POST':
        form = ValidateBooth(request.POST)
        if form.is_valid():
            photobooth = PhotoBooth(
                nom="nouveau_photbooth",
                client=Client.objects.get(pk=1)
            )
            photobooth.save()
            auth_for_photomaton = get_object_or_404(
                Authorization, 
                user_code=form.cleaned_data['user_code']
                )
            auth_for_photomaton.is_validate = True
            auth_for_photomaton.photobooth = photobooth
            auth_for_photomaton.save()

            return HttpResponseRedirect('/')
    else:
        form = ValidateBooth()

    return render(request, 'form.html', {'form': form})


@csrf_exempt
def wait_photobooth(request):
    client_id = request.POST.get('client_id')
    device_code = request.POST.get('device_code')
    auth_for_photomaton = get_object_or_404(
        Authorization,
        client_id=client_id,
        device_code=device_code
    )

    ask_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

    elapsed = ask_time - auth_for_photomaton.date_ask
    if elapsed < datetime.timedelta(seconds=auth_for_photomaton.interval):
        auth_for_photomaton.save()
        response = JsonResponse({
            "error": "slow_down"
        })
        response.status_code = 400
        return response

    elapsed = ask_time - auth_for_photomaton.date_create

    if elapsed > datetime.timedelta(seconds=auth_for_photomaton.expires_in):
        auth_for_photomaton.save()
        response = JsonResponse({
            "error": "expired_token"
        })
        response.status_code = 400
        return response

    if not auth_for_photomaton.is_validate:
        auth_for_photomaton.save()
        response = JsonResponse({
            "error": "authorization_pending"
        })
        response.status_code = 400
        return response

    # https://www.oauth.com/oauth2-servers/device-flow/token-request/
    # TODO: Gestion du E"access_denied"

    token = Token(
        photobooth=auth_for_photomaton.photobooth,
        access_token=get_random_string(64),
        refresh_token=get_random_string(64),
        token_type="bearer",
        expires=3600
    )
    token.save()

    auth_for_photomaton.delete()
    response = JsonResponse({
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "token_type": token.token_type,
        "expires": token.expires
    })
    response.status_code = 200
    return response


@csrf_exempt
@require_http_methods(["POST"])
def photo_upload(request):
    access_token = get_access_token(request)
    token = get_object_or_404(Token, access_token=access_token)
    photomaton = token.photobooth

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        fp = form.cleaned_data["file"]
        created_at = form.cleaned_data["created_at"]
        name = form.cleaned_data["name"]

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
