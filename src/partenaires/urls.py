from django.conf.urls import url, include
from django.contrib import admin

from partenaires.views import become_partenaire, nos_salles

urlpatterns = [
    url('^devenir-partenaire/$', become_partenaire, name='become-partenaire'),
    url('^nos-salles/$', nos_salles, name='nos-salles'),
]
