# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes, FieldWithButtons, StrictButton

import datetime

from formateurs.models import Formateur

class FormateurForm(forms.ModelForm):

    class Meta:
        model = Formateur
        fields = ('prenom','nom','gsm','email','photo_profil','experience','photo_profil', 'niveau_etude', 'etablissement_scolaire', 'profession',
                  'facebook_link','linkdin_link','twitter_link','googleplus_link', 'motivation', 'methodologie'
                  )



