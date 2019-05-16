from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from formateurs.models import Formateur
from formateurs.forms import FormateurForm

def formateur_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated :
            return decorated_view_func(request)  # return redirect to signin
        if len(Formateur.objects.filter(user=request.user, active=True))==1:
            formateur = Formateur.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        elif len(Formateur.objects.filter(user=request.user, active=False))==1:
            return redirect('wait-to-be-validated')
        else:
            return redirect('become-teacher')
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


@formateur_required
def dashboard_formateurs(request):
    return render(request, 'formateurs/dashboard.html', {})

@login_required
def become_teacher(request):
    user = request.user
    if len(Formateur.objects.filter(user=user))==1:
        return redirect('dashboard-formateurs')
    form = FormateurForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        formateur = form.save(commit=False)
        formateur.user = user
        formateur.save()
        return redirect('dashboard-formateurs')
    return render(request, 'formateurs/become-teacher.html', {"form":form})

@login_required
def wait_to_be_validated(request):
    user = request.user
    if len(Formateur.objects.filter(user=user,active=True))==1:
        return redirect('dashboard-formateurs')
    return render(request, 'formateurs/wait-to-be-validated.html', {})

