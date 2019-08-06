from cours.models import Categorie, Cours
from formations.models import Encouragement
import random

def categories_processor(request):
   categories = Categorie.objects.all()
   return {'categories': categories}

def best_courses_processor(request):
    best_courses = Cours.objects.all()[:5]
    print(best_courses)
    return {'best_courses': best_courses}

def encouragement_processor(request):
   encouragements = Encouragement.objects.all()
   return {'encouragement': random.choice(encouragements)}
