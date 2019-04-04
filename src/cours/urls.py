from django.conf.urls import url, include
from django.contrib import admin

from cours.views import detail_cours, liste_cours



urlpatterns = [
    url('^(?P<pk>\d+)/$', detail_cours, name='detail-cours'),
    url('^$', liste_cours, name='liste-cours'),
    url('^liste/$', liste_cours, name='liste-cours')
]
