from django.shortcuts import render, redirect

import os
from django.conf import settings
from django.http import HttpResponse
import json as simplejson
# import models
from cours.models import Categorie, SousCategorie, Cours, SousCategorieCours, FormateurCours, Lecon, Option, SkillCours
from formateurs.models import Formateur
from formateurs.forms import FormateurForm
from cours.forms import CoursModelForm, LeconModelForm, OptionModelForm, SkillModelForm, IntroductionForm, ConfirmationForm, SousCategorieForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formtools.wizard.views import WizardView, SessionWizardView
from django.core.files.storage import FileSystemStorage

from django.forms import formset_factory
from django.forms.formsets import BaseFormSet

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

LeconFormSet = formset_factory(LeconModelForm,
                                 formset=BaseFormSet,
                                 max_num=20,
                                 )

FORMS = [("introduction", IntroductionForm),
         ("creer_cours", CoursModelForm),
         ("creer_lecon", LeconFormSet),
         ("ajouter_sous_categorie", SousCategorieForm),
         ("confirmation", ConfirmationForm)]

TEMPLATES = {"introduction":"cours/cours-wizard/introduction.html",
             "creer_cours" : "cours/cours-wizard/creer-cours.html",
             "creer_lecon" : "cours/cours-wizard/creer-lecon.html",
             "ajouter_sous_categorie": "cours/cours-wizard/ajouter-sous-categorie.html",
             "confirmation": "cours/cours-wizard/confirmation.html"}

class CreateCoursWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.DEFAULT_FILE_STORAGE)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(CreateCoursWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'confirmation':
          cours_form = self.get_cleaned_data_for_step('creer_cours')
          lecon_form = self.get_cleaned_data_for_step('creer_lecon')
          categorie_form = self.get_cleaned_data_for_step('ajouter_sous_categorie')
          cours = Cours(
                        titre = cours_form['titre'],
                        courte_description = cours_form['courte_description'],
                        long_description = cours_form['long_description'],
                        image = cours_form['image']
                        )
          sous_categories = []
          for sous_categorie in categorie_form['sous_categorie']:
              sous_categories.append(sous_categorie)
          context.update({'cours':cours, 'image':cours_form['image'],'sous_categories':sous_categories})
          lecons = []
          for form in lecon_form:
              lecon = Lecon(
                          titre     = form['titre'],
                          cours     = Cours.objects.first(),
                          contenu   = form['contenu'],
                          prerequis = form['prerequis'],
                          ordre     = form['ordre']
                      )
              lecons.append(lecon)
          context.update({'lecons':lecons})
        return context
    def done(self, form_list, **kwargs):
        cours_form = self.get_cleaned_data_for_step('creer_cours')
        lecon_form = self.get_cleaned_data_for_step('creer_lecon')
        categorie_form = self.get_cleaned_data_for_step('ajouter_sous_categorie')

        # 1. On sauve le nouveau cours
        cours = Cours(
                        titre = cours_form['titre'],
                        courte_description = cours_form['courte_description'],
                        long_description = cours_form['long_description'],
                        image = cours_form['image']
                        )
        cours.save()

        # 2. On sauve les leçons du cours ET les options
        for form in lecon_form:
            lecon = Lecon(
                        titre     = form['titre'],
                        cours     = cours,
                        contenu   = form['contenu'],
                        prerequis = form['prerequis'],
                        ordre     = form['ordre']
                      )
            lecon.save()
            debut = datetime.combine(form['date_debut'], form['heure_debut'])
            fin   = datetime.combine(form['date_fin'], form['heure_fin'])
            option =  Option(
                            lecon    = lecon,
                            debut    = debut,
                            fin      = fin,
                            tarif    = form['tarif'],
                            capacite = form['capacite'],

              )
            option.save()
        # 3. On associe les sous-catégories au cours
        for sous_categorie in categorie_form['sous_categorie']:
            sous_categorie = SousCategorieCours(cours=cours, sous_categorie=sous_categorie)
            sous_categorie.save()
        # 4. On associe le cours au formateur qui l'a créé
        formateur_cours = FormateurCours(cours=cours, formateur=self.request.user.formateur)
        formateur_cours.save()
        return redirect('dashboard-formateurs')

def ajax_get_sous_categories(request, pk):
    categorie = Categorie.objects.get(pk=pk)
    sous_categories = SousCategorie.objects.filter(categorie=categorie)
    sous_categories_dict=[]
    [sous_categories_dict.append((each_sous_categorie.pk,each_sous_categorie.nom)) for each_sous_categorie in sous_categories]
    return HttpResponse(simplejson.dumps(sous_categories_dict), content_type="application/json")

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
    heure_debut = option.debut.strftime("%H:%M")
    date_debut  = option.debut.strftime("%d/%m/%Y")
    heure_fin   = option.fin.strftime("%H:%M")
    date_fin    = option.fin.strftime("%d/%m/%Y")
    form = OptionModelForm(request.POST or None, instance=option, initial={'heure_debut': heure_debut, 'heure_fin':heure_fin, "date_debut":date_debut, "date_fin":date_fin})
    if form.is_valid():
        heure_debut = request.POST['heure_debut']
        date_debut = request.POST['date_debut']
        date_time_debut = datetime.strptime(date_debut + " " + heure_debut, '%d/%m/%Y %H:%M')
        heure_fin = request.POST['heure_fin']
        date_fin = request.POST['date_fin']
        date_time_fin = datetime.strptime(date_fin + " " + heure_fin, '%d/%m/%Y %H:%M')

        option = form.save(commit=False)
        option.debut = date_time_debut
        option.fin = date_time_fin
        option.save()
        return redirect('detail-cours-formateur', pk=option.lecon.cours.pk)
    return render(request, 'cours/mes-options/edit-option.html', {"form":form})

@formateur_required
def creer_competence(request, pk):
    cours = Cours.objects.get(pk=pk)
    form = SkillModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        competence = form.save(commit=False)
        competence.cours = cours
        competence.save()
        return redirect('detail-cours-formateur', pk=cours.pk)
    return render(request, 'cours/mes-competences/creer-competence.html', {"form":form})

@formateur_required
def edit_competence(request, pk):
    competence = SkillCours.objects.get(pk=pk)
    form = SkillModelForm(request.POST or None, instance=competence)
    if form.is_valid():
        competence = form.save()
        return redirect('detail-cours-formateur', pk=competence.cours.pk)
    return render(request, 'cours/mes-competences/edit-competence.html', {"form":form})


