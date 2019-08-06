from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
import json as simplejson

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formtools.wizard.views import WizardView, SessionWizardView
from django.core.files.storage import FileSystemStorage

from django.forms import formset_factory
from django.forms.formsets import BaseFormSet

from cours.models import Cours
from apprenants.forms import CategorieUserForm, UniversitaireForm, AdulteForm, SecondaireForm, ConfirmationForm
from apprenants.models import University, Faculte

from allauth.account.forms import SignupForm

@login_required
def complete_profile(request):
    return render(request, 'apprenants/complete-profile.html', {})

@login_required
def dashboard_student(request):
    return render(request, 'apprenants/dashboard-student.html', {})

FORMS = [
         ("categorie_user", CategorieUserForm),
         ("etude_user",     UniversitaireForm),
         ("confirmation",   ConfirmationForm)
         ]

TEMPLATES = {
             "categorie_user" : "apprenants/premier-pas/etape-2.html",
             "etude_user"     : "apprenants/premier-pas/etape-3.html",
             "confirmation"   : "apprenants/premier-pas/etape-4.html"
             }
from django.forms.widgets import HiddenInput
class PremierPasWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.DEFAULT_FILE_STORAGE)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        form = super(PremierPasWizard, self).get_form(step, data, files)
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "etude_user":
            prev_data = self.get_cleaned_data_for_step("categorie_user")
            categorie_user = prev_data["categories"]
            if categorie_user == "universitaire":
                form.fields['universite'].required = True
                form.fields['faculte'].required = True
                form.fields['annee_univ'].required = True
                form.fields['profession'].widget = HiddenInput()
                form.fields['salarie'].widget = HiddenInput()
                form.fields['etablissement_scolaire'].widget = HiddenInput()
                form.fields['annee_sec'].widget = HiddenInput()
            elif categorie_user == "adulte":
                form.fields['salarie'].required = True
                form.fields['profession'].required = True
                form.fields['universite'].widget = HiddenInput()
                form.fields['faculte'].widget = HiddenInput()
                form.fields['annee_univ'].widget = HiddenInput()
                form.fields['etablissement_scolaire'].widget = HiddenInput()
                form.fields['annee_sec'].widget = HiddenInput()
            elif categorie_user == "secondaire":
                form.fields['etablissement_scolaire'].required = True
                form.fields['annee_sec'].required = True
                form.fields['profession'].widget = HiddenInput()
                form.fields['salarie'].widget = HiddenInput()
                form.fields['universite'].widget = HiddenInput()
                form.fields['faculte'].widget = HiddenInput()
                form.fields['annee_univ'].widget = HiddenInput()
        return form

    def get_context_data(self, form, **kwargs):
        context = super(PremierPasWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'categorie_user':
            if self.request.method == "POST":
                form = SignupForm(self.request.POST)
                form.save(self.request)
         #   form = self.get_form('signup')
         #   form.save()
        elif self.steps.current == 'confirmation':
            categorie_user = self.get_cleaned_data_for_step('categorie_user')
            etude_user = self.get_cleaned_data_for_step('etude_user')
            faculte = etude_user['faculte']
            universite = etude_user['universite']
            cours = Cours.objects.filter(faculte = faculte)
            context.update({'cours':cours})
        return context

    def done(self, form_list, **kwargs):
        return redirect('welcome')

def ajax_get_faculte(request, pk):
    universite = University.objects.get(pk=pk)
    faculte = Faculte.objects.filter(universite=universite)
    faculte_dict=[]
    [faculte_dict.append((each_faculte.pk,each_faculte.nom_complet)) for each_faculte in faculte]
    return HttpResponse(simplejson.dumps(faculte_dict), content_type="application/json")
