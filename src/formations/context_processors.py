from cours.models import Categorie, Cours

def categories_processor(request):
   categories = Categorie.objects.all()
   return {'categories': categories}

def best_courses_processor(request):
    best_courses = Cours.objects.all()[:5]
    print(best_courses)
    return {'best_courses': best_courses}
