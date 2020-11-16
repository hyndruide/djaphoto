from django.db import models
from django.contrib import admin



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
    #users = models.ManyToManyField(User)

    def __str__(self):
        return '%s' % (self.nom)
        
admin.site.register(Client)



class PhotoBoothAdmin(admin.ModelAdmin):
    pass
    


class PhotoBooth(models.Model):
    nom = models.CharField(max_length=50)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Photo Booth"

admin.site.register(PhotoBooth)

class Photo(models.Model):
    lien = models.CharField(max_length=255)
    date_create = models.DateField(auto_now_add=True)
    photobooth = models.ForeignKey(PhotoBooth,on_delete=models.CASCADE)
admin.site.register(Photo)