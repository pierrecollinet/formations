from django.db import models

# Create your models here.

class Cours(models.Model):
    short_description = models.TextField()

    def __str__(self):
        return self.short_description[:10]
