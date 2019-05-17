# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from cours.models import Cours, Categorie, Lecon, SousCategorie
from formations.models import Prospect
from formations.forms import ContactForm

def welcome(request):
    return render(request, 'welcome.html', {})

def contact(request):
    form = ContactForm(request.POST or None)
    c = {'form':form}
    if form.is_valid():
        nom     = request.POST['nom']
        prenom  = request.POST['prenom']
        email   = request.POST['email']
        gsm     = request.POST['gsm']
        message = request.POST['message']
        # envoi de l'email
        plaintext = get_template('../templates/emails/contactform.txt')
        htmly     = get_template('../templates/emails/contactform.html')
        subject, from_email = 'Formulaire de Contact - ' + nom + ' ' + prenom, email
        to = ['pi.collinet@gmail.com']
        d = { 'nom': nom, 'prenom':prenom, 'gsm':gsm, 'message':message, 'email':email}
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Nous avons bien reçu votre message. Un membre de l'équipe va prendre contact avec vous dans les plus brefs délais")
        return redirect('welcome')
    if form.errors :
        c.update({"anchor":'form'})
    return render(request, 'contact.html', c)

def about(request):
    return render(request, 'about.html', {})

def faq(request):
    return render(request, 'faq.html', {})

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html', {})

def search(request):
    all_cours = set()
    if 'q' in request.GET :
        query = request.GET['q']
        cours = Cours.objects.filter(
                                  Q(titre__icontains=query)|
                                  Q(courte_description__icontains=query)|
                                  Q(long_description__icontains=query)
                                  )
        all_cours.update(cours)
        categories = Categorie.objects.filter(nom__icontains=query)
        for c in categories :
            all_cours.update(c.get_cours())
        sous_categories = SousCategorie.objects.filter(nom__icontains=query)
        for ss in sous_categories :
            all_cours.update(ss.get_cours())
        lecons = Lecon.objects.filter(
                                  Q(titre__icontains=query)|
                                  Q(contenu__icontains=query)
                                    )
        for l in lecons :
            all_cours.update(l.cours)
    return render(request, 'cours/courses-grid-sidebar.html', {"cours":all_cours, "anchor":"courses"})

def newsletter(request):
    if 'email_newsletter' in request.POST:
        email_newsletter = request.POST['email_newsletter']
        prospect, created = Prospect.objects.get_or_create(email = email_newsletter)
        prospect.reason = "newsletter"
        prospect.save()
        messages.success(request, "Félicitations, vous aurez bientôt de nos nouvelles !")
    return redirect(request.META['HTTP_REFERER'])






