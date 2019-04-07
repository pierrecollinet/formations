from django.conf.urls import url, include
from django.contrib import admin

from cours.views import detail_cours, courses_list, courses_grid



urlpatterns = [
    url('^(?P<pk>\d+)/$', detail_cours, name='detail-cours'),
  #  url('^$', courses_grid, name='courses-grid'),
    url('^grid/$', courses_grid, name='courses-grid'),
    url('^liste/$', courses_list, name='courses-list')
]
