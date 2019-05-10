# -*- coding: utf-8 -*-

# import models
from cours.models import Categorie, SousCategorie, Cours, CategorieCours, SkillCours, Lecon
from django.contrib import admin


admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(Cours)
admin.site.register(CategorieCours)
admin.site.register(SkillCours)
admin.site.register(Lecon)
