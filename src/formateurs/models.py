from django.db import models
from fontawesome.fields import IconField
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User

class Formateur(models.Model):
    # general info
    user   = models.OneToOneField(User, on_delete=models.CASCADE,)
    prenom = models.CharField(max_length=200)
    nom    = models.CharField(max_length=200)
    gsm    = models.CharField(max_length=200, blank=True, null=True)
    email  = models.EmailField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)
    experience   = models.TextField(blank=True, null=True)
    niveau_etude = models.CharField(choices=(('secondaire', 'Secondaire'), ('universitaire', 'Universitaire'), ('professionnel', 'Professionnel'), ), default='secondaire', max_length=200)
    etablissement_scolaire = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    # social info
    facebook_link   = models.URLField(max_length=1000, blank=True, null=True)
    linkdin_link    = models.URLField(max_length=1000, blank=True, null=True)
    twitter_link    = models.URLField(max_length=1000, blank=True, null=True)
    googleplus_link = models.URLField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=False)
    # pédagogie info
    motivation   = models.TextField(blank=True, null=True)
    methodologie = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.prenom + " " + self.nom

def active_change_pre_save(sender, instance, *args, **kwargs):
    old_instance = Formateur.objects.get(pk=instance.pk)
    old_is_active = old_instance.active
    new_is_active = instance.active
    if not old_is_active and new_is_active :
        "envoyer un email"
        print("envoi email...")

pre_save.connect(active_change_pre_save, sender = Formateur)

