from django.db import models
from fontawesome.fields import IconField
from django.db.models.signals import pre_save, post_save, post_delete

class Categorie(models.Model):
    nom  = models.CharField(max_length = 200)
    icon = IconField()

    def __str__(self):
        return self.nom

    def get_number_cours(self):
        souscategorie_ids = self.souscategorie_set.all().values_list('id', flat=True)
        cours = SousCategorieCours.objects.filter(sous_categorie__id__in = souscategorie_ids).values_list('cours', flat=True)
        return len(set(cours))

    def get_cours(self):
        souscategorie_ids = self.souscategorie_set.all().values_list('id', flat=True)
        cours_ids = SousCategorieCours.objects.filter(sous_categorie__id__in = souscategorie_ids).values_list('cours', flat=True)
        cours = Cours.objects.filter(id__in = cours_ids)
        return set(cours)

class SousCategorie(models.Model):
    nom       = models.CharField(max_length = 200)
    icon      = IconField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,)

    def __str__(self):
        return self.nom

    def get_cours(self):
        cours_ids = SousCategorieCours.objects.filter(sous_categorie=self).values_list('cours', flat=True)
        cours = Cours.objects.filter(id__in = cours_ids)
        return set(cours)


class Cours(models.Model):
    titre              = models.CharField(max_length = 500)
    courte_description = models.TextField()
    long_description   = models.TextField()
    image              = models.ImageField(upload_to = 'mes_images/')
    active             = models.BooleanField(default = True)
    total              = models.CharField(max_length=20, default="0")

    def __str__(self):
        return self.titre

class FormateurCours(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,)
    formateur = models.ForeignKey('formateurs.Formateur', on_delete=models.CASCADE,)

    def __str__(self):
        return self.cours.titre + ' - ' + self.formateur.email
class SousCategorieCours(models.Model):
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE,)
    cours     = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.sous_categorie.nom + ' - ' + self.cours.titre

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

class Option(models.Model):
    lecon    = models.ForeignKey(Lecon, on_delete=models.CASCADE, blank=True, null=True)
    debut    = models.DateTimeField()
    fin      = models.DateTimeField()
    tarif    = models.CharField(max_length=10)
    capacite = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        if self.lecon:
            return self.lecon.cours.titre + " - " + self.debut.strftime("%d/%m/%Y, %H:%M")
        else :
            return "Lecon - " + self.debut.strftime("%d/%m/%Y, %H:%M")

def option_post_save(sender, instance, *args, **kwargs):
    cours = instance.lecon.cours
    lecons = cours.lecon_set.all()
    total  = 0
    for l in lecons:
        option = l.option_set.all().first()
        if option:
            total  += float(option.tarif)
    cours.total = str(total)
    cours.save()
post_save.connect(option_post_save, sender = Option)



