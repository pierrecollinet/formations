from django.conf.urls import url, include
from django.contrib import admin

from carts.views import show_panier, checkout, checkout_done

urlpatterns = [
  #  url('^$', courses_grid, name='courses-grid'),
    url('^$', show_panier, name='show-panier'),
    url('^reserver$', checkout, name='checkout'),
    url('^confirmation$', checkout_done, name='checkout-done'),
]
