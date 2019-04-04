# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'welcome.html', {})

def contact(request):
    return render(request, 'contact.html', {})
