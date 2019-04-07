from django.conf.urls import url, include
from django.contrib import admin
from formations.views import welcome, contact
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', welcome, name='welcome'),
    url(r'^contact$', contact, name='contact'),

    url(r'^cours/', include('cours.urls')),
    url(r'^formateurs/', include('formateurs.urls')),
    url(r'^apprenants/', include('apprenants.urls')),

    url(r'^accounts/', include('allauth.urls'))
]
