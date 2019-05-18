from django.db import models
from fontawesome.fields import IconField
from django.db.models.signals import pre_save, post_save, post_delete

class SalleCours(models.Model):
    nom               = models.CharField(max_length=200)
    nom_abreviation   = models.CharField(max_length=200, blank=True, null=True)
    adresse           = models.CharField(max_length=200)
    telephone         = models.CharField(max_length=200)
    capacite_maximale = models.SmallIntegerField(blank=True, null=True)

    lat  = models.CharField(max_length=200, blank=True, null=True)
    long = models.CharField(max_length=200, blank=True, null=True)

    rue         = models.CharField(max_length=200, blank=True, null=True)
    numero      = models.CharField(max_length=200, blank=True, null=True)
    code_postal = models.CharField(max_length=200, blank=True, null=True)
    ville       = models.CharField(max_length=200, blank=True, null=True)

    plan_acces  = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)


    def __str__(self):
        return self.nom

    def get_image_url(self):
        img = self.sallecoursimage_set.first()
        if img:
            return img.image.url
        return img #None

    def get_images(self):
        imgs = self.sallecoursimage_set.all()
        return imgs

def image_upload_to(instance, filename):
    title = instance.salle_cours.nom
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "salle-de-cours/%s/%s" %(slug, new_filename)


class SalleCoursImage(models.Model):
    salle_cours = models.ForeignKey(SalleCours, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.salle_cours.nom




