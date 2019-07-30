from django.conf.urls import url, include
from django.contrib import admin
from formations.views import welcome, contact, about, faq, terms_and_conditions, search, newsletter

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', welcome, name='welcome'),
    url(r'^contact$', contact, name='contact'),
    url(r'^a-propos$', about, name='about'),
    url(r'^faq$', faq, name='faq'),
    url(r'^terms-and-conditions$', terms_and_conditions, name='terms-and-conditions'),
    url(r'^search/$', search, name='search'),
    url(r'^newsletter/$', newsletter, name='newsletter'),

    url(r'^cours/', include('cours.urls')),
    url(r'^formateurs/', include('formateurs.urls')),
    url(r'^apprenants/', include('apprenants.urls')),
    url(r'^partenaires/', include('partenaires.urls')),
    url(r'^panier/', include('carts.urls')),
    url(r'^billing/', include('billing.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

from formations.views import custom404, custom500
handler404 = custom404
handler500 = custom500




