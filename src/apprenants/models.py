from django.db import models
from fontawesome.fields import IconField
from django.contrib.auth.models import User

class University(models.Model):
    nom_complet = models.CharField(max_length = 200)
    abreviation = models.CharField(max_length = 200, blank=True, null=True)
    icon        = IconField(blank=True, null=True)
    logo        = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

    def __str__(self):
        return self.nom_complet

class Faculte(models.Model):
    nom_complet = models.CharField(max_length = 200)
    abreviation = models.CharField(max_length = 200, blank=True, null=True)
    universite   = models.ForeignKey(University, on_delete=models.CASCADE,)
    icon        = IconField(blank=True, null=True)
    logo        = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

    def __str__(self):
        return self.nom_complet

ANNEES = (
          ('ba1', 'BA1'),
          ('ba2', 'BA2'),
          ('ba3', 'BA3'),
          ('ma1', 'MA1'),
          ('ma2', 'MA2'),
)
class Apprenant(models.Model):
    # general info
    user   = models.OneToOneField(User, on_delete=models.CASCADE,)
    prenom = models.CharField(max_length=200)
    nom    = models.CharField(max_length=200)
    gsm    = models.CharField(max_length=200, blank=True, null=True)
    email  = models.EmailField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)
    # etablissement
    categorie  = models.CharField(max_length=200)
    universite = models.ForeignKey(University, on_delete=models.CASCADE,)
    faculte    = models.ForeignKey(Faculte, on_delete=models.CASCADE,)
    annee      = models.CharField(max_length=30, choices = ANNEES)

    def __str__(self):
        if self.prenom and self.nom:
            return self.prenom + " " + self.nom
        else:
            return self.user.username
