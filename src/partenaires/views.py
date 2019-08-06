from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
# from partenaires.models import
from partenaires.forms import PartenaireForm

def become_partenaire(request):
    form = PartenaireForm(request.POST or None)
    print('----------------')
    if form.is_valid():
        print('BBBB')
        nom     = request.POST['nom']
        email   = request.POST['email']
        gsm     = request.POST['gsm']
        sujet   = request.POST['sujet']
        content = request.POST['content']
        # envoi de l'email
        plaintext = get_template('../templates/partenaires/emails/contact-partenaire.txt')
        htmly     = get_template('../templates/partenaires/emails/contact-partenaire.html')
        subject, from_email = 'Demande de partenariat - ' + nom, email
        to = ['pi.collinet@gmail.com']
        d = { 'nom': nom, 'gsm':gsm, 'content':content,'sujet':sujet, 'email':email}
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Nous avons bien reçu votre message. Un membre de l'équipe va prendre contact avec vous dans les plus brefs délais")
        return redirect('welcome')
    else :
        print(form.errors)
        print('error')
    return render(request, 'partenaires/become_partenaire.html', {'form':form})

def nos_salles(request):

    return render(request, 'partenaires/nos_salles.html', {})
