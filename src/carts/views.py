from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from cours.models import Cours, Lecon, Option
from billing.models import BillingProfile
from .models import Cart
from reservation.models import Reservation

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_IjIi2cQwhiXCOqqnX7sjZNML")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_fpPhnmP0kFV0uzcMHMW0ED68')
EMAILS = getattr(settings, "EMAILS", 'pi.collinet@gmail.com')
stripe.api_key = STRIPE_SECRET_KEY

@login_required
def show_panier(request, pk):
    cours = Cours.objects.get(pk=pk)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.cours != cours:
        cart_obj.options.clear()
        cart_obj.cours = cours
        lecons = cours.lecon_set.all()
        for lecon in lecons:
            if len(lecon.option_set.all())>0:
                cart_obj.options.add(lecon.option_set.all().first())
    cart_options_ids = cart_obj.options.all().values_list('id', flat=True)
    cart_obj.save()
    return render(request, 'carts/cart.html', {"cours":cours, "cart_options_ids":cart_options_ids, "cart_obj":cart_obj})

@login_required
def checkout(request, pk):
    cours = Cours.objects.get(pk=pk)
    lecons = cours.lecon_set.all()
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    reservation_obj = None
    if cart_created or cart_obj.options.count() == 0:
        return redirect("show-panier", pk=cart_obj.pk)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    reservation_obj, reservation_obj_created = Reservation.objects.new_or_get(billing_profile, cart_obj)
    has_card = False
    if billing_profile is not None:
        has_card = billing_profile.has_card

    if request.method == "POST":
        is_prepared = reservation_obj.check_done()
        if is_prepared:
        #    did_charge, crg_msg = billing_profile.charge(reservation_obj)
            if True : #did_charge:
                reservation_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                # envoi de l'email de confirmation
                cours_related = reservation_obj.cart.cours.get_related();
                plaintext = get_template('../templates/carts/emails/confirmation-inscription.txt')
                htmly     = get_template('../templates/carts/emails/confirmation-inscription.html')
                subject, from_email = reservation_obj.billing_profile.user.username + ', bienvenue dans ' + reservation_obj.cart.cours.titre, 'info@kairos.be'
                to = EMAILS
                d = { 'reservation': reservation_obj, 'cours_related':cours_related[:3], 'host':request.get_host()}
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect("checkout-done")
            else:
                print(crg_msg)
                return redirect("show-panier", pk=cart_obj.pk)
    context = {"cours":cours, "cart_obj":cart_obj, "has_card":has_card, "billing_profile":billing_profile, "publish_key": STRIPE_PUB_KEY,}
    return render(request, 'carts/checkout.html', context)

@login_required
def checkout_done(request):
    return render(request, 'carts/checkout_done.html', {})


def cart_update(request):
    options = request.POST.getlist('option')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_obj.options.clear()
    lecons = []
    warning = None
    for option_id in options :
        option = Option.objects.get(id=option_id)
        if option.lecon not in lecons:
            lecons.append(option.lecon)
        else:
            warning = "Vous avez sélectionné 2 fois le même module (contenu du cours identique). C'est votre droit, mais on préfère vous prévenir :-)"
        cart_obj.options.add(option)
    request.session['cart_items'] = cart_obj.options.count()
    if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
        json_data = {
            "total": cart_obj.total,
            "warning": warning
        }
        return JsonResponse(json_data, status=200)

    # if options is not None:
    #     try:
    #         product_obj = Product.objects.get(id=product_id)
    #     except Product.DoesNotExist:
    #         print("Show message to user, product is gone?")
    #         return redirect("cart:home")
    #     cart_obj, new_obj = Cart.objects.new_or_get(request)
    #     if product_obj in cart_obj.products.all():
    #         cart_obj.products.remove(product_obj)
    #         added = False
    #     else:
    #         cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
    #         added = True
    #     request.session['cart_items'] = cart_obj.products.count()
    #     # return redirect(product_obj.get_absolute_url())
    #     if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
    #         print("Ajax request")
    #         json_data = {
    #             "added": added,
    #             "removed": not added,
    #             "cartItemCount": cart_obj.products.count()
    #         }
    #         return JsonResponse(json_data, status=200) # HttpResponse
    #         # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    # return redirect("cart:home")
