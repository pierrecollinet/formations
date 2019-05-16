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

class ContactForm(forms.Form):
    nom          = forms.CharField(label="Nom",error_messages={'required': 'Introduisez votre nom SVP'})
    prenom       = forms.CharField(label="Prénom",error_messages={'required': 'Introduisez votre prénom SVP'})
    email        = forms.EmailField(label="Email",error_messages={'required': 'Introduisez votre adresse Email SVP'})
    gsm          = forms.CharField(label="GSM",error_messages={'required': 'Introduisez un numéro de téléphone SVP'})
    message      = forms.CharField()
    check_human  = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        check_human = cleaned_data.get("check_human")

        if check_human:
            if check_human != str(4):
                print('ROOOOOBOOOOOTT')
                msg = "Nous avons à faire à un robot !"
                self.add_error('check_human', msg)
                raise forms.ValidationError(
                    "Nous avons à faire à un robot !"
                )



