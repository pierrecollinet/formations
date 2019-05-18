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

from cours.models import Cours

class CoursModelForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ('titre','courte_description','long_description','image',)

    def __init__(self, *args, **kwargs):
        super(CoursModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Field('titre', placeholder="Titre du cours"),
                                Field('courte_description', placeholder="Description en quelques lignes..."),
                                Field('long_description', placeholder='Description plus détaillée...'),
                                Field('image'),
        )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))
