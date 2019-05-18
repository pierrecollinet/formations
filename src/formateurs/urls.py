from django.conf.urls import url, include
from django.contrib import admin

from .views import dashboard_formateurs, become_teacher, wait_to_be_validated



urlpatterns = [
    url('^dashboard-formateur/$', dashboard_formateurs, name='dashboard-formateurs'),
    url('^become-teacher/$', become_teacher, name='become-teacher'),
    url('^wait-to-be-validated/$', wait_to_be_validated, name='wait-to-be-validated'),
]

