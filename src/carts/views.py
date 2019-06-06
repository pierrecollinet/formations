from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def show_panier(request):
    return render(request, 'carts/cart.html', {})

@login_required
def checkout(request):
    return render(request, 'carts/checkout.html', {})

@login_required
def checkout_done(request):
    return render(request, 'carts/checkout_done.html', {})

