# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes, FieldWithButtons, StrictButton

import datetime

class PartenaireForm(forms.Form):
    nom     = forms.CharField(label="Nom")
    email   = forms.EmailField(label="Email")
    gsm     = forms.CharField(label="GSM")
    sujet   = forms.CharField(label="Sujet")
    content = forms.CharField(label="Message",required=True,widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(PartenaireForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
                                Field('nom', placeholder="Votre nom"),
                                Field('email', placeholder="Votre email"),
                                Field('gsm', placeholder='Votre gsm'),
                                Field('sujet', placeholder='Sujet'),
                                Field('content', placeholder='Message...'),
        )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))
