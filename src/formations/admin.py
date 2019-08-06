# -*- coding: utf-8 -*-

# import models
from formations.models import Prospect, Faq, CategorieFaq, Encouragement
from django.contrib import admin


admin.site.register(Prospect)
admin.site.register(CategorieFaq)
admin.site.register(Faq)
admin.site.register(Encouragement)
