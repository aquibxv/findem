from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
    return render(request, 'pages/signup.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')