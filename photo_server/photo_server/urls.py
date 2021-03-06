"""photo_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from photo_backend.views import (
    welcome,

    logout,
    dashboard,
    photobooth_view,
    validate_photobooth,
    modify_photobooth,
    maintenance_photobooth,
    maintenance_photobooth_change
)


urlpatterns = [
    path("", welcome),
    path("api/", include('photo_backend.api.urls')),
    path('dashboard/', dashboard,name='dashboard'),
    path("photobooth/", photobooth_view, name='photobooth_view'),
    path("photobooth/validate/", validate_photobooth, name='validpb'),
    path("photobooth/modify/", modify_photobooth, name='modifypb'),
    path("photobooth/maintenance/<int:idbooth>/<int:active>", maintenance_photobooth_change),
    path("photobooth/maintenance/", maintenance_photobooth, name='maintenance'),
    path('logout/', logout),
    path("admin/", admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
