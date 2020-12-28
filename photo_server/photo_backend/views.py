import datetime

from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponse
)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import UploadForm, ValidateBooth, PhotoBoothForm
from .models import Photo, PhotoBooth, Authorization, Token, Profile
from .utils import get_access_token, get_random_string

from django.contrib.auth import logout as log_out
from django.conf import settings
from urllib.parse import urlencode


# Create your views here.


def first(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'index.html')

@login_required
def photobooth_view(request):
    user = request.user
    identity = user.social_auth.get(provider='auth0')

    userdata = {
        'user_id': identity.uid,
        'name': user.first_name,
        'picture': identity.extra_data['picture'],
        'email': user.email,
    }
    photobooths = PhotoBooth.objects.all()
    return render(request, 'photobooth.html', {'userdata': userdata,
                                               'user': user,
                                               'photobooths': photobooths})

@login_required
def dashboard(request):
    user = request.user
    identity = user.social_auth.get(provider='auth0')

    userdata = {
        'user_id': identity.uid,
        'name': user.first_name,
        'picture': identity.extra_data['picture'],
        'email': user.email,
    }
    photos = Photo.objects.all()
    return render(request, 'index.html', {
        'userdata': userdata,
        'user': user,
        "photos": photos
    })


def logout(request):
    qs = urlencode(
        {
            "client_id": settings.SOCIAL_AUTH_AUTH0_KEY,
            "returnTo": request.build_absolute_uri('/')
        }
    )
    base_url = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}"
    logout_url = f"{base_url}/v2/logout?{qs}"
    log_out(request)
    return HttpResponseRedirect(logout_url)


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
        "verification_uri": "http://localhost:8000/photobooth/validate/",
        "interval": auth_for_photomaton.interval,
        "expires_in": auth_for_photomaton.expires_in
    })
    response.status_code = 200
    return response


@login_required
def validate_photobooth(request):
    if request.method == 'POST':
        form = ValidateBooth(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            auth_for_photomaton = get_object_or_404(
                Authorization,
                user_code=form.cleaned_data['user_code']
                )
            auth_for_photomaton.is_validate = True

            photobooth = PhotoBooth(
                nom="nouveau_photbooth",
                client=profile.client
            )
            photobooth.save()
            auth_for_photomaton.photobooth = photobooth
            auth_for_photomaton.save()
            form = PhotoBoothForm()
            return render(request, 'form_photobooth.html', {'form': form,
                                                            'id_photobooth': photobooth.pk})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, 'form.html', {'form': form})
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

        photo = Photo(
            photo=fp,
            date_create=created_at,
            photobooth=photomaton,
        )
        photo.save()

        response = JsonResponse({"id": photo.id})
        response.status_code = 201  # Created
        return response
    else:
        return HttpResponseBadRequest(form.errors)


@login_required
def modify_photobooth(request):
    if request.method == 'POST':
        form = PhotoBoothForm(request.POST)
        if form.is_valid():
            photobooth = get_object_or_404(
                PhotoBooth,
                pk=request.POST["id_photobooth"]
                )
            photobooth.nom = form.cleaned_data["nom"]
            photobooth.save()
            return HttpResponse(status=200)
        else:
            render(request, 'form_photobooth.html', {'form': form})

    else:
        form = PhotoBoothForm(request.POST)
        return render(request, 'form_photobooth.html', {'form': form})