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

from cours.models import Cours, Lecon, Option, SkillCours, Categorie, SousCategorie, Matiere
from apprenants.models import Faculte, University

class IntroductionForm(forms.Form):
    title = 'introduction'

class ConfirmationForm(forms.Form):
    title = 'confirmation'

class CoursModelForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ('titre','courte_description','long_description','prerequis','image',)

    def __init__(self, *args, **kwargs):
        super(CoursModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Field('titre', placeholder="Titre du cours"),
                                Field('courte_description', placeholder="Description en quelques lignes..."),
                                Field('long_description', placeholder='Description plus détaillée...'),
                                Field('prerequis', placeholder="Quel(s) sont les prérequis pour assister au cours ?"),
                                Field('image'),
        )

class LeconModelForm(forms.ModelForm):
    date_debut  = forms.DateField(initial=date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))
    heure_debut = forms.TimeField(initial='09:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Début du cours"}), input_formats=('%H:%M',))
    date_fin    = forms.DateField(initial=date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))
    heure_fin   = forms.TimeField(initial='09:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Début du cours"}), input_formats=('%H:%M',))
    tarif       = forms.CharField()
    capacite    = forms.IntegerField(initial=3)
    ordre       = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':1}))
    class Meta:
        model = Lecon
        fields = ('titre','contenu','ordre',)

    def __init__(self, *args, **kwargs):
        super(LeconModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.empty_permitted = False
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Field('titre', placeholder="Titre du cours",css_class="col-xs-12"),
                                Field('contenu', placeholder="Décris le contenu du cours..."),
                                Field('ordre'),
                                Div(
                                    Div('date_debut',css_class='col-md-6',placeholder="Date de début"),
                                    Div('heure_debut',css_class='col-md-6',placeholder="Heure de début"),
                                    css_class='row',
                                ),
                                Div(
                                    Div('date_fin',css_class='col-md-6',placeholder="Date de fin"),
                                    Div('heure_fin',css_class='col-md-6',placeholder="Heure de fin"),
                                    css_class='row',
                                ),
                                Div(
                                    Div('tarif',css_class='col-md-6',placeholder="Tarif par personne"),
                                    Div('capacite',css_class='col-md-6',placeholder="Combien d'élèves maximum?"),
                                    css_class='row',
                                )
        )
    #    self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))


    def clean(self):
        cleaned_data = super().clean()
        titre = cleaned_data.get("titre")
        contenu = cleaned_data.get("contenu")

        if not titre or not contenu:
            msg = "Tous les champs sont obligatoires ! "
            raise forms.ValidationError(msg)

class OptionModelForm(forms.ModelForm):
    date_debut  = forms.DateField(initial=date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))
    heure_debut = forms.TimeField(initial='09:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Début du cours"}), input_formats=('%H:%M',))
    date_fin    = forms.DateField(initial=date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))
    heure_fin   = forms.TimeField(initial='09:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Début du cours"}), input_formats=('%H:%M',))

    class Meta:
        model = Option
        fields = ('tarif','capacite',)

    def __init__(self, *args, **kwargs):
        super(OptionModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Div(
                                    Div('date_debut',css_class='col-md-6',placeholder="Date de début"),
                                    Div('heure_debut',css_class='col-md-6',placeholder="Heure de début"),
                                    css_class='row',
                                ),
                                Div(
                                    Div('date_fin',css_class='col-md-6',placeholder="Date de fin"),
                                    Div('heure_fin',css_class='col-md-6',placeholder="Heure de fin"),
                                    css_class='row',
                                ),
                                Div(
                                    Div('tarif',css_class='col-md-6',placeholder="Tarif par personne"),
                                    Div('capacite',css_class='col-md-6',placeholder="Combien d'élèves maximum?"),
                                    css_class='row',
                                ),
        )
#        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

    def clean(self):
        cleaned_data = super().clean()

        heure_debut = cleaned_data.get("heure_debut")
        heure_debut = heure_debut.strftime("%H:%M")
        date_debut  = cleaned_data.get("date_debut")
        date_debut  = date_debut.strftime("%d/%m/%Y")
        heure_fin   = cleaned_data.get("heure_fin")
        heure_fin   = heure_fin.strftime("%H:%M")
        date_fin    = cleaned_data.get("date_fin")
        date_fin    = date_fin.strftime("%d/%m/%Y")

        if heure_debut and date_debut and heure_fin and date_fin:
            date_time_debut = datetime.strptime(date_debut + " " + heure_debut, '%d/%m/%Y %H:%M')

            date_time_fin   = datetime.strptime(date_fin + " " + heure_fin, '%d/%m/%Y %H:%M')

            if date_time_fin <= date_time_debut:
                msg = "Ton cours ne peut pas se terminer avant d'avoir commencé. "
                raise forms.ValidationError(msg)

class SkillModelForm(forms.ModelForm):
    class Meta:
        model = SkillCours
        fields = ('skill',)

    def __init__(self, *args, **kwargs):
        super(SkillModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Field('Skill', placeholder="Décris la compétence"),
        )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

class SousCategorieForm(forms.Form):
    categorie      = forms.ModelChoiceField(queryset=Categorie.objects.all())
    sous_categorie = forms.ModelMultipleChoiceField(queryset=SousCategorie.objects.all(), widget=forms.CheckboxSelectMultiple)

ANNEES = (
          ('ba1', 'BA1'),
          ('ba2', 'BA2'),
          ('ba3', 'BA3'),
          ('ma1', 'MA1'),
          ('ma2', 'MA2'),
)

class SearchForm(forms.Form):
    universite = forms.ModelChoiceField(queryset=University.objects.all(), required = False)
    faculte    = forms.ModelChoiceField(queryset=Faculte.objects.all(), required = False)
    annee      = forms.ChoiceField(choices = ANNEES, required = False)
    matiere    = forms.ModelChoiceField(queryset=Matiere.objects.all(), required = False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Chercher', css_class='btn btn-default btn-lg'))

