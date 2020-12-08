from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
"""
Produit de base
photo

Client:
    Entreprise, association, famille

User:
    Utilisateur qui fait partie d'un client
    client =


PhotoBooth :
    nom :
    status :
    link Client many 2 one


Photo :
    lien
    date
    link client
    link photobooth

"""


class Client(models.Model):
    nom = models.CharField(max_length=255)
    # users = models.ManyToManyField(User)

    def __str__(self):
        return "%s" % (self.nom)


admin.site.register(Client)


class PhotoBoothAdmin(admin.ModelAdmin):
    pass


class PhotoBooth(models.Model):

    nom = models.CharField(max_length=50, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Photo Booth"


admin.site.register(PhotoBooth)


class Authorization(models.Model):
    client_id = models.CharField(max_length=255)
    device_code = models.CharField(max_length=255)
    user_code = models.CharField(max_length=255)
    interval = models.IntegerField()
    expires_in = models.IntegerField()
    is_validate = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_ask = models.DateTimeField(auto_now=True)
    photobooth = models.ForeignKey(PhotoBooth, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.client_id + str(self.is_validate)


admin.site.register(Authorization)


class Token(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    expires = models.IntegerField()
    date_create = models.DateTimeField(auto_now_add=True)
    photobooth = models.ForeignKey(PhotoBooth, null=True, on_delete=models.CASCADE)


admin.site.register(Token)


class Photo(models.Model):
    photo = models.ImageField(upload_to='photo')
    date_upload = models.DateTimeField(auto_now_add=True)
    date_create = models.DateTimeField(blank=False)
    photobooth = models.ForeignKey(PhotoBooth, on_delete=models.CASCADE)

    def __str__(self):
        import pytz

        local_tz = pytz.timezone("Europe/Paris")
        when = self.date_create.astimezone(local_tz).strftime("%d/%m/%Y, %H:%M:%S %Z")
        return self.photo.name + " " + when


admin.site.register(Photo)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

admin.site.register(Profile)
