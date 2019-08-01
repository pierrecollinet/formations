from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cours.forms import CoursModelForm, LeconModelForm, OptionModelForm, SkillModelForm, IntroductionForm, ConfirmationForm, SousCategorieForm

from cours.forms import CoursModelForm, LeconModelForm, OptionModelForm, SkillModelForm, IntroductionForm, ConfirmationForm, SousCategorieForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formtools.wizard.views import WizardView, SessionWizardView
from django.core.files.storage import FileSystemStorage

from django.forms import formset_factory
from django.forms.formsets import BaseFormSet

from apprenants.forms import CategorieUserForm

from allauth.account.forms import SignupForm

@login_required
def complete_profile(request):
    return render(request, 'apprenants/complete-profile.html', {})

@login_required
def dashboard_student(request):
    return render(request, 'apprenants/dashboard-student.html', {})

@login_required
def premier_pas(request):
    return render(request, 'apprenants/premier-pas/etape-1.html', {})

LeconFormSet = formset_factory(LeconModelForm,
                                 formset=BaseFormSet,
                                 max_num=20,
                                 )

FORMS = [("signup", SignupForm),
         ("categorie_user", CategorieUserForm),
         ("etude_user", ConfirmationForm)]

TEMPLATES = {"signup" : "apprenants/premier-pas/etape-1.html",
             "categorie_user" : "apprenants/premier-pas/etape-2.html",
             "etude_user": "apprenants/premier-pas/etape-3.html"}

class PremierPasWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.DEFAULT_FILE_STORAGE)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(PremierPasWizard, self).get_context_data(form=form, **kwargs)
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
