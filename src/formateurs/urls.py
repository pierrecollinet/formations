from django.conf.urls import url, include
from django.contrib import admin

from .views import dashboard_formateurs



urlpatterns = [
    url('^dashboard_formateurs/$', dashboard_formateurs, name='dashboard-formateurs')
]
