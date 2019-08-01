from cours.models import Categorie, Cours
import random
def categories_processor(request):
   categories = Categorie.objects.all()
   return {'categories': categories}

def best_courses_processor(request):
    best_courses = Cours.objects.all()[:5]
    print(best_courses)
    return {'best_courses': best_courses}

def encouragement_processor(request):
   encouragements = [
                  "La réussite est le fruit du travail, du courage et de l'intelligence.",
                  "You look great today !"
    ]
   return {'encouragement': random.choice(encouragements)}
