from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Feedback
from profiles.models import UserProfile

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'profile/dashboard.html')
    else:
        return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
    return render(request, 'pages/signup.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

@login_required
def feedback(request):
    """defines a view for fetching a feedback"""
    if request.method == 'POST':

        # get form values
        title = request.POST.get('title')
        feedback = request.POST.get('feedback')
        author = request.user.name

        feed = Feedback.objects.create(title=title, feedback=feedback, author=author)
        feed.save()

        messages.success(request, "Thanks for your valuable feedback")
        return redirect('dashboard')
    
    return render(request, 'pages/feedback.html')

@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'profile/dashbaord.html')
    else:
        return render(request, 'pages/home.html')

def forgotPassword(request):
    """ method to change password when forgotten by the user """

    if request.method == 'POST':

        # fetch the details and validate if correct
        email = request.POST.get('email')
        collage = request.POST.get('collage_name')
        grad_year = request.POST.get('grad_year')
        grad_year = int(grad_year)
        new_pwd = request.POST.get('new_password')
        confirm_pwd = request.POST.get('confirm_password')

        try:
            user = UserProfile.objects.get(email=email)
        except ObjectDoesNotExist:
            user = None

        # if no user object is present
        if user == None:
            messages.error(request, "No such profile exists!")
            return redirect('reset_password')
        else:
            if user.college_name != collage:
                messages.error(request, "The collage/ university data is incorrect!")
                return redirect('reset_password')
            elif user.graduation_year != grad_year:
                messages.error(request, "The graduation year data is incorrect!")
                return redirect('reset_password')
        
            # if all the feilds are correct
            # check if the two passwords are correct
            if new_pwd != confirm_pwd:
                messages.error(request, "The passwords did not match!")
                return redirect('reset_password')
            else:
                user.set_password(new_pwd)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('reset_password')
            
    return render(request, 'pages/forgot_password.html')