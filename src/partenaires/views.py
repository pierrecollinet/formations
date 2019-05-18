from django.shortcuts import render

# import models
# from partenaires.models import

def become_partenaire(request):
    return render(request, 'partenaires/become_partenaire.html', {})
