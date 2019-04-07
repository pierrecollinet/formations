# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'welcome.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def faq(request):
    return render(request, 'faq.html', {})

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html', {})
