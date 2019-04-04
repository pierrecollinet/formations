from django.shortcuts import render

# import models
from cours.models import Cours

def detail_cours(request, pk):
    cours = Cours.objects.get(pk=pk)
    return render(request, 'detail_cours.html', {"cours":cours})

def liste_cours(request):
    cours = Cours.objects.all()
    return render(request, 'liste_cours.html', {"cours":cours})
