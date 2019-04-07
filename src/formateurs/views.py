from django.shortcuts import render



def dashboard_formateurs(request):
    return render(request, 'formateurs/dashboard.html', {})
