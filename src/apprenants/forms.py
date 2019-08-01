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

CHOICES_CATEGORIES = (
                      ('secondaire', 'Etudiant du secondaire'),
                      ('universitaire', 'Etudiant universitaire'),
                      ('adulte', 'Adulte')
)

class CategorieUserForm(forms.Form):
    categories      = forms.ChoiceField(choices = CHOICES_CATEGORIES)

    def __init__(self, *args, **kwargs):
        super(CategorieUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False

