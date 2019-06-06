from django.db import models
from fontawesome.fields import IconField
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom  = models.CharField(max_length = 200)
    icon = IconField()
    image = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

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

class CoursQuerySet(models.query.QuerySet):
    def validated(self):
        return self.filter(validated=True)

class CoursManager(models.Manager):

    def get_queryset(self):
        return CoursQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().validated()

class Cours(models.Model):
    titre              = models.CharField(max_length = 500)
    courte_description = models.TextField(blank = True, null = True)
    long_description   = models.TextField(blank = True, null = True)
    prerequis          = models.TextField(blank=True, null=True)
    image              = models.ImageField(upload_to = 'mes_images/')
    active             = models.BooleanField(default = True)
    total              = models.CharField(max_length=20, default="0")
    validated          = models.BooleanField(default = False)

    objects = CoursManager()
    def __str__(self):
        return self.titre

    def get_main_teacher(self):
        main_teachers = self.formateurcours_set.filter(main=True)
        if len(main_teachers) > 0:
            main_teacher = main_teachers.first()
            teacher = main_teacher.formateur
            return teacher
        else :
            main_teachers = self.formateurcours_set.all()
            main_teacher = main_teachers.first()
            teacher = main_teacher.formateur
            return teacher

    def get_lecons(self):
        lecons = Lecon.objects.filter(cours=self)
        return lecons

    def total_time_lecons(self):
        total = 0
        for lecon in self.get_lecons():
            total += lecon.get_time_lecon()
        return total

class FormateurCours(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,)
    formateur = models.ForeignKey('formateurs.Formateur', on_delete=models.CASCADE,)
    main = models.BooleanField(default = True)
    def __str__(self):
        return self.cours.titre + ' - ' + self.formateur.email
class SousCategorieCours(models.Model):
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE,)
    cours          = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.sous_categorie.nom + ' - ' + self.cours.titre

class SkillCours(models.Model):
    skill = models.TextField(blank=True, null=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.skill[:15] + ' - ' + self.cours.titre

class Lecon(models.Model):
    titre     = models.CharField(max_length = 500, blank = True, null = True)
    cours     = models.ForeignKey(Cours, on_delete=models.CASCADE,)
    contenu   = models.TextField(blank=True, null=True)
    ordre     = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.cours.titre + ' - ' + self.contenu[:30]
    class Meta:
        ordering = ('ordre', )

    def get_time_lecon(self):
        options = Option.objects.filter(lecon=self)
        if len(options)>0:
            option = options.first()
            delta = option.fin - option.debut
            return delta.total_seconds()/3600
        else :
          return 0

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
    class Meta:
        ordering = ('debut', )
    def show_date_range(self):
        date_debut  = self.debut.strftime("%d/%m/%Y")
        date_fin    = self.fin.strftime("%d/%m/%Y")
        heure_debut = self.debut.strftime("%H:%M")
        heure_fin   = self.fin.strftime("%H:%M")
        if date_debut == date_fin:
            return "Le {} de {} à {}".format(date_debut, heure_debut, heure_fin)
        else :
            return "Du {} ({}) au {} ({})".format(date_debut, heure_debut, date_fin, heure_fin)

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


class ReviewCours(models.Model):
    cours       = models.ForeignKey(Cours, on_delete=models.CASCADE,)
    auteur      = models.ForeignKey(User, on_delete=models.CASCADE,)
    commentaire = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    rating      = models.PositiveSmallIntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),))

    def __str__(self):
        return self.auteur.username + " - " + self.commentaire[:30]

class Cible(models.Model):
    nom         = models.CharField(max_length=200)
    image       = models.ImageField(upload_to = 'mes_images/')
    description = models.TextField()
    icon        = IconField()
    ordre       = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ('ordre', )

    def get_cours(self):
        cibles_cours = CibleCours.objects.filter(cible = self)
        cours_ids = cibles_cours.values_list('cours', flat=True)
        cours = Cours.objects.filter(id__in = cours_ids)
        return set(cours)

class CibleCours(models.Model):
    cible = models.ForeignKey(Cible, on_delete=models.CASCADE,)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,)

    def __str__(self):
        return self.cours.titre + " - " + self.cible.nom



