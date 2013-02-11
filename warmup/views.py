# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'warmup/index.html', context)

def login(request):
    context = {}
    return render(request, 'warmup/login.html', context)
# class LoginView(TemplateView):
#     template_name  = "login.html"

def welcome(request):
    context = {}
    return render(request, 'warmup/welcome.html', context)
# class WelcomeView(TemplateView):
#         template_name = "welcome.html"