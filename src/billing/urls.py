from django.conf.urls import url, include
from django.contrib import admin

from billing.views import payment_method_view, payment_method_createview
urlpatterns = [
    url('^payment-method/$', payment_method_view, name='billing-payment-method'),
    url('^payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),

]
