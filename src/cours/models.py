from django.db import models
from fontawesome.fields import IconField

class Categorie(models.Model):
    nom  = models.CharField(max_length = 200)
    icon = IconField()

    def __str__(self):
        return self.nom

class SousCategorie(models.Model):
    nom       = models.CharField(max_length = 200)
    icon      = IconField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,)

    def __str__(self):
        return self.nom

class Cours(models.Model):
    titre              = models.CharField(max_length = 500)
    courte_description = models.TextField()
    long_description   = models.TextField()
    image              = models.ImageField()
    active             = models.BooleanField(default = True)

    def __str__(self):
        return self.titre

class CategorieCours(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,)
    cours     = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.categorie.nom + ' - ' + self.cours.titre

class SkillCours(models.Model):
    skill = models.TextField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.skill[:15] + ' - ' + self.cours.titre

class Lecon(models.Model):
    titre     = models.CharField(max_length = 500, blank = True, null = True)
    cours     = models.ForeignKey(Cours, on_delete=models.CASCADE,)
    contenu   = models.TextField()
    prerequis = models.TextField()
    ordre     = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.cours.titre + ' - ' + self.contenu[:30]






