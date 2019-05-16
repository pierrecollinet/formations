from django.conf.urls import url, include
from django.contrib import admin

from cours.views import detail_cours, courses_list, courses_grid, detail_categorie_grid, detail_categorie_list, detail_sous_categorie_grid, detail_sous_categorie_list



urlpatterns = [
    url('^(?P<pk>\d+)/$', detail_cours, name='detail-cours'),
  #  url('^$', courses_grid, name='courses-grid'),
    url('^grid/$', courses_grid, name='courses-grid'),
    url('^liste/$', courses_list, name='courses-list'),
    url('^categorie-grid/(?P<pk>\d+)$', detail_categorie_grid, name='categorie-grid'),
    url('^categorie-list/(?P<pk>\d+)$', detail_categorie_list, name='categorie-list'),
    url('^sous-categorie-grid/(?P<pk>\d+)$', detail_sous_categorie_grid, name='sous-categorie-grid'),
    url('^sous-categorie-list/(?P<pk>\d+)$', detail_sous_categorie_list, name='sous-categorie-list')
]
