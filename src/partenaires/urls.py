from django.conf.urls import url, include
from django.contrib import admin

from partenaires.views import become_partenaire

urlpatterns = [
    url('^become-partenaire/$', become_partenaire, name='become-partenaire'),
]
