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
