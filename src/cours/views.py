from django.shortcuts import render, redirect

# import models
from cours.models import Categorie, SousCategorie, Cours, SousCategorieCours, FormateurCours, Lecon, Option
from formateurs.models import Formateur
from formateurs.forms import FormateurForm
from cours.forms import CoursModelForm, LeconModelForm, OptionModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
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

@formateur_required
def edit_cours(request, pk):
    cours = Cours.objects.get(pk=pk)
    form = CoursModelForm(request.POST or None, request.FILES or None, instance=cours)
    if form.is_valid():
        cours = form.save()
        return redirect('detail-cours-formateur', pk=cours.pk)
    return render(request, 'cours/mes-cours/creer-cours.html', {"form":form})


@formateur_required
def creer_lecon(request, pk):
    form = LeconModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        cours = Cours.objects.get(pk=pk)
        lecon = form.save(commit=False)
        lecon.cours = cours
        lecon.save()
        return redirect('detail-cours-formateur', pk=cours.pk)
    return render(request, 'cours/mes-lecons/creer-lecon.html', {"form":form})

@formateur_required
def edit_lecon(request, pk):
    lecon = Lecon.objects.get(pk=pk)
    form = LeconModelForm(request.POST or None, instance=lecon)
    if form.is_valid():
        lecon = form.save()
        return redirect('detail-cours-formateur', pk=lecon.cours.pk)
    return render(request, 'cours/mes-lecons/edit-lecon.html', {"form":form})

@formateur_required
def creer_option(request, pk):
    form = OptionModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        heure_debut = request.POST['heure_debut']
        date_debut = request.POST['date_debut']
        date_time_debut = datetime.strptime(date_debut + " " + heure_debut, '%d/%m/%Y %H:%M')
        heure_fin = request.POST['heure_fin']
        date_fin = request.POST['date_fin']
        date_time_fin = datetime.strptime(date_fin + " " + heure_fin, '%d/%m/%Y %H:%M')

        lecon = Lecon.objects.get(pk=pk)
        option = form.save(commit=False)
        option.lecon = lecon
        option.debut = date_time_debut
        option.fin = date_time_fin
        option.save()
        return redirect('detail-cours-formateur', pk=lecon.cours.pk)
    return render(request, 'cours/mes-options/creer-option.html', {"form":form})

@formateur_required
def edit_option(request, pk):
    option = Option.objects.get(pk=pk)
    form = OptionModelForm(request.POST or None, instance=option)
    if form.is_valid():
        option = form.save()
        return redirect('detail-cours-formateur', pk=option.lecon.cours.pk)
    return render(request, 'cours/mes-options/edit-option.html', {"form":form})






