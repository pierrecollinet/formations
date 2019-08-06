# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes, FieldWithButtons, StrictButton

from datetime import datetime, date
from .models import University, Faculte

CHOICES_CATEGORIES = (
                      ('universitaire', 'Etudiant universitaire'),
                      ('secondaire', 'Etudiant du secondaire'),
                      ('adulte', 'Adulte')
)

class CategorieUserForm(forms.Form):
    categories      = forms.ChoiceField(choices = CHOICES_CATEGORIES)

    def __init__(self, *args, **kwargs):
        super(CategorieUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False

ANNEES = (
          ('ba1', 'BA1'),
          ('ba2', 'BA2'),
          ('ba3', 'BA3'),
          ('ma1', 'MA1'),
          ('ma2', 'MA2'),
)

ANNEES_SEC = (
          ('1', '1ère année'),
          ('2', '2ème année'),
          ('3', '3ème année'),
          ('4', '4ème année'),
          ('5', '5ème année'),
          ('6', '6ème année'),
)
class UniversitaireForm(forms.Form):
    universite = forms.ModelChoiceField(queryset=University.objects.all(), required = False)
    faculte    = forms.ModelChoiceField(queryset=Faculte.objects.all(), required = False)
    annee_univ = forms.ChoiceField(choices = ANNEES, required = False)
    profession = forms.CharField(required = False)
    salarie    = forms.ChoiceField(choices = (('salarie','Salarié'),('independant', 'Indépendant')), required = False)
    etablissement_scolaire = forms.CharField(required = False)
    annee_sec  = forms.ChoiceField(choices = ANNEES_SEC, required = False)

    def __init__(self, *args, **kwargs):
        super(UniversitaireForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

class AdulteForm(forms.Form):
    profession = forms.CharField()
    salarie    = forms.ChoiceField(choices = (('salarie','Salarié'),('independant', 'Indépendant')))

class SecondaireForm(forms.Form):
    etablissement_scolaire = forms.CharField()
    annee = forms.ChoiceField(choices = ANNEES)

class ConfirmationForm(forms.Form):
    title = 'confirmation'
