from django.conf.urls import url, include
from django.contrib import admin

from .views import complete_profile, dashboard_student, premier_pas
from .views import PremierPasWizard, FORMS



urlpatterns = [
    url('^dashboard_student/$', dashboard_student, name='dashboard-student'),
    url('^complete-profile/$', complete_profile, name='complete-profile'),
 #   url('^premier-pas/$', premier_pas, name='premier-pas'),

    url('^premier-pas/$', PremierPasWizard.as_view(FORMS), name="premier-pas"),
]
