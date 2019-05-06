from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def search(request):
    """View for implementing searching profile functionality """

    return render(request, 'profiles/search.html')

def profile(request):
    """View for returning a unique profile"""

    return render(request, 'profiles/profile.html')

def login(request):
    """View for Logging-in a user into the system"""
  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'pages/login.html')

def signup(request):
    """View for Signing-up into the system"""
    if request.method == 'POST':
        
        # Get form value
        profile_picture = request.POST.get('inputprofile')
        name = request.POST.get('inputname')
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']
        highest_degree_earned = request.POST['inputDegree']
        college_name = request.POST['CollegeName']
        graduation_year = request.POST['inputGradYear']
        skill_1 = request.POST['upload_skill1']
        skill_2 = request.POST.get('upload_skill2', '')
        skill_3 = request.POST.get('upload_skill3', '')
        skill_4 = request.POST.get('upload_skill4', '')
        skill_5 = request.POST.get('upload_skill5', '')
        skill_6 = request.POST.get('upload_skill6', '')

        # Check Username
        if UserProfile.objects.filter(name=name).exists():
            messages.error(request, "That Name already taken")
            return redirect('signup')
        # Check email
        else:
            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, "That email is being used")
                return redirect('signup')
            else:
                # Looks Good
                user = UserProfile.objects.create_user(profile_picture=profile_picture, name=name, email=email, 
                password=password, highest_degree_earned=highest_degree_earned, college_name=college_name, 
                graduation_year=graduation_year, skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4,
                skill_5=skill_5, skill_6=skill_6)

                # #Login after register
                # auth.login(request, user)

                user.save()
                messages.success(request, "You are now registered and can log in")
                return redirect('login')

    else:    
        return render(request, 'pages/signup.html')

def logout(request):
    """View for Logging-out a user from the system"""

    return redirect('pages/index.html')

@login_required
def dashboard(request):
    """View for directing a user to the dashboard"""
    return render(request, 'pages/dashboard.html')
