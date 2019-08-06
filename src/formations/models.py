from django.db import models
from fontawesome.fields import IconField
from django.db.models.signals import pre_save, post_save, post_delete

class Prospect(models.Model):
    email   = models.EmailField()
    nom     = models.CharField(max_length = 200, blank=True, null=True)
    prenom  = models.CharField(max_length = 200, blank=True, null=True)
    reason  = models.CharField(max_length = 500, blank=True, null=True)

    def __str__(self):
        return self.email


class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CategorieFaq(models.Model):
    categorie = models.CharField(max_length=200,blank=True, null=True)
    icon      = IconField(blank=True, null=True)
    slug      = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.categorie

class Faq(models.Model):
    question  = models.TextField(blank=True, null=True)
    reponse   = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(CategorieFaq, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.question[:30]


class Encouragement(models.Model):
    proverbe = models.TextField()
    auteur = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.auteur + ' - ' + self.proverbe[:30]

