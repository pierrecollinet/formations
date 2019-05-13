from django.shortcuts import render

# import models
from cours.models import Categorie, SousCategorie, Cours, CategorieCours

def detail_cours(request, pk):
    cours = Cours.objects.get(pk=pk)
    print(cours)
    return render(request, 'cours/detail_cours.html', {"cours":cours})

def courses_grid(request):
    cours = Cours.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'cours/courses-grid-sidebar.html', {"cours":cours, "categories":categories})

def courses_list(request):
    cours = Cours.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'cours/courses-list-sidebar.html', {"cours":cours, "categories":categories})
