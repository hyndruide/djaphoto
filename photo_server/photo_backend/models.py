from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

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
    lien = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)
    date_create = models.DateTimeField(blank=False)
    photobooth = models.ForeignKey(PhotoBooth, on_delete=models.CASCADE)

    def __str__(self):
        import pytz

        local_tz = pytz.timezone("Europe/Paris")
        when = self.date_create.astimezone(local_tz).strftime("%d/%m/%Y, %H:%M:%S %Z")
        return self.lien + " " + when


admin.site.register(Photo)


class MyUserManager(BaseUserManager):
    def create_user(self, email, client_id, password=None):
        """
        Creates and saves a User with the given email, client name choose by su and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            client=Client.objects.get(pk=client_id)
        )
        user.set_password(password)
        user.save(using=self._db)
        # Envoyer un mail aux nouveau utilisateur pour crée sont mot de passe et l'activer
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, client name, and password.
        """
        new_client,_ = Client.objects.get_or_create(nom="nouveau client")
        new_client.save()

        user = self.create_user(
            email,
            password=password,
            client_id=new_client.pk,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def Which_client(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.client.nom
    class Meta:
        verbose_name = "Utilisateur"
