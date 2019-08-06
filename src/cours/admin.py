# -*- coding: utf-8 -*-

# import models
from cours.models import Categorie, SousCategorie, Cours, SousCategorieCours, SkillCours, Lecon, Option, FormateurCours, ReviewCours, Cible, CibleCours, Matiere, MatiereCours
from django.contrib import admin


admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(Cours)
admin.site.register(SousCategorieCours)
admin.site.register(SkillCours)
admin.site.register(Lecon)
admin.site.register(Option)
admin.site.register(FormateurCours)
admin.site.register(ReviewCours)
admin.site.register(Cible)
admin.site.register(CibleCours)
admin.site.register(Matiere)
admin.site.register(MatiereCours)
