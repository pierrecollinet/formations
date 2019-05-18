from django.shortcuts import render, redirect

# import models
from cours.models import Categorie, SousCategorie, Cours, SousCategorieCours, FormateurCours
from formateurs.models import Formateur
from formateurs.forms import FormateurForm
from cours.forms import CoursModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def formateur_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated :
            return decorated_view_func(request)  # return redirect to signin
        if len(Formateur.objects.filter(user=request.user, active=True))==1:
            formateur = Formateur.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        elif len(Formateur.objects.filter(user=request.user, active=False))==1:
            return redirect('wait-to-be-validated')
        else:
            return redirect('become-teacher')
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

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



# POUR LE FORMATEUR
@formateur_required
def detail_cours_formateur(request, pk):
    cours = Cours.objects.get(pk=pk)
    return render(request, 'cours/mes-cours/cours-detail.html', {"cours":cours})

@formateur_required
def cours_list_formateur(request):
    return render(request, 'cours/mes-cours/cours-list.html', {})

@formateur_required
def creer_cours(request):
    form = CoursModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        cours = form.save()
        formateur = Formateur.objects.get(user = request.user)
        formateurcours = FormateurCours(cours = cours, formateur = formateur)
        formateurcours.save()
        return redirect('dashboard-formateurs')
    return render(request, 'cours/mes-cours/creer-cours.html', {"form":form})





