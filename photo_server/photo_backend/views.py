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

from .forms import ValidateBooth, PhotoBoothForm
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