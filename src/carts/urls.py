from django.conf.urls import url, include
from django.contrib import admin

from carts.views import show_panier, checkout, checkout_done, cart_update

urlpatterns = [
  #  url('^$', courses_grid, name='courses-grid'),
    url('^inscription/(?P<pk>\d+)/$', show_panier, name='show-panier'),
    url('^reserver/(?P<pk>\d+)/$', checkout, name='checkout'),
    url('^confirmation$', checkout_done, name='checkout-done'),
    url(r'^update/$', cart_update, name='update'),
]
