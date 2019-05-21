from django.conf.urls import url, include
from django.contrib import admin

from cours.views import detail_cours, courses_list, courses_grid, detail_categorie_grid, detail_categorie_list, detail_sous_categorie_grid, detail_sous_categorie_list
from cours.views import cours_list_formateur, detail_cours_formateur, creer_cours, creer_lecon, edit_lecon, edit_cours, creer_option, edit_option, creer_competence, edit_competence


urlpatterns = [
    url('^(?P<pk>\d+)/$', detail_cours, name='detail-cours'),
  #  url('^$', courses_grid, name='courses-grid'),
    url('^grid/$', courses_grid, name='courses-grid'),
    url('^liste/$', courses_list, name='courses-list'),
    url('^categorie-grid/(?P<pk>\d+)$', detail_categorie_grid, name='categorie-grid'),
    url('^categorie-list/(?P<pk>\d+)$', detail_categorie_list, name='categorie-list'),
    url('^sous-categorie-grid/(?P<pk>\d+)$', detail_sous_categorie_grid, name='sous-categorie-grid'),
    url('^sous-categorie-list/(?P<pk>\d+)$', detail_sous_categorie_list, name='sous-categorie-list'),

    # pour le formateur
    url('^liste-cours-formateur/$', cours_list_formateur, name='cours-liste-formateur'),
    url('^cours-formateur/(?P<pk>\d+)/$', detail_cours_formateur, name='detail-cours-formateur'),
    url('^creer-cours/$', creer_cours, name='creer-cours'),
    url('^edit-cours/(?P<pk>\d+)/$', edit_cours, name='edit-cours'),
    url('^creer-lecon/(?P<pk>\d+)/$', creer_lecon, name='creer-lecon'),
    url('^edit-lecon/(?P<pk>\d+)/$', edit_lecon, name='edit-lecon'),
    url('^creer-option/(?P<pk>\d+)/$', creer_option, name='creer-option'),
    url('^edit-option/(?P<pk>\d+)/$', edit_option, name='edit-option'),
    url('^creer-competence/(?P<pk>\d+)/$', creer_competence, name='creer-competence'),
    url('^edit-competence/(?P<pk>\d+)/$', edit_competence, name='edit-competence'),
]
