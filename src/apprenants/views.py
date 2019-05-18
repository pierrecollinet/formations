from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def complete_profile(request):
    return render(request, 'apprenants/complete-profile.html', {})

@login_required
def dashboard_student(request):
    return render(request, 'apprenants/dashboard-student.html', {})

