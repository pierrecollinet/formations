from django.shortcuts import render

# import models
from cours.models import Categorie, SousCategorie, Cours, SousCategorieCours

def detail_cours(request, pk):
    cours = Cours.objects.get(pk=pk)
    return render(request, 'cours/detail_cours.html', {"cours":cours})

def courses_grid(request):
    cours = Cours.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'cours/courses-grid-sidebar.html', {"cours":cours, "categories":categories})

def courses_list(request):
    cours = Cours.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'cours/courses-list-sidebar.html', {"cours":cours, "categories":categories})

def detail_categorie_grid(request, pk):
    categorie = Categorie.objects.get(pk=pk)
    return render(request, 'cours/detail_categorie_grid.html', {"categorie":categorie})

def detail_categorie_list(request, pk):
    categorie = Categorie.objects.get(pk=pk)
    return render(request, 'cours/detail_categorie_list.html', {"categorie":categorie})

def detail_sous_categorie_grid(request, pk):
    sous_categorie = SousCategorie.objects.get(pk=pk)
    return render(request, 'cours/detail_sous_categorie_grid.html', {"sous_categorie":sous_categorie})

def detail_sous_categorie_list(request, pk):
    sous_categorie = SousCategorie.objects.get(pk=pk)
    return render(request, 'cours/detail_sous_categorie_list.html', {"sous_categorie":sous_categorie})







