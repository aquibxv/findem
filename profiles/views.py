from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from .models import UserProfile, PersonalInformation, SocialPlatform, Accomplishments, Location, WorkExperience


# Create your views here.
def search(request):
    """View for implementing searching profile functionality """

    profiles = UserProfile.objects.order_by('-join_date')

    # Skill
    if 'skill' in request.GET:
        skill = request.GET['skill']
        if skill:
            profiles = UserProfile.objects.filter(Q(skill_1__icontains=skill) | Q(skill_2__icontains=skill) |
            Q(skill_3__icontains=skill) | Q(skill_4__icontains=skill) | Q(skill_5__icontains=skill) |
            Q(skill_6__icontains=skill))

    # College
    if 'college' in request.GET:
        college = request.GET['college']
        if college:
            profiles = profiles.filter(college_name__icontains=college)

    # Name
    if 'name' in request.GET:
        name = request.GET['name']
        if name:
            profiles = profiles.filter(name__icontains=name)

    # Pagination
    paginator = Paginator(profiles, 6)
    page = request.GET.get('page')
    paged_profiles = paginator.get_page(page)

    # context dictionary
    context = {
        'profiles' : paged_profiles,
        'values' : request.GET
    }

    return render(request, 'profiles/search.html', context)

def profile(request, profile_id):
    """View for returning a unique profile"""
    
    # fetching profile
    profile = get_object_or_404(UserProfile, pk=profile_id)   

    # fetching social handle
    try:
        socialhandle = SocialPlatform.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        socialhandle = None

    # fetching presonal-Information
    try:
        personal_info = PersonalInformation.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        personal_info = None


    # fetching accomplisments
    try:
        accomplishment = Accomplishments.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        accomplishment = None

    # fetching location
    try:
        location = Location.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        location = None

     # fetching WorkExperience
    try:
        work_exp = WorkExperience.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        work_exp = None

    context = {
        'profile' : profile,
        'socialhandle' : socialhandle,
        'personal_info' : personal_info, 
        'accomplishment': accomplishment, 
        'location' : location,
        'work_exp' : work_exp,
    }

    return render(request, 'profiles/profile.html', context)

def login(request):
    """View for Logging-in a user into the system"""
  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        # if user exists
        if user is not None:
            # authenticate the user
            auth.login(request, user)

            # Fetch additional information about the user
            # fetching presonal-Information
            try:
                personal_info = PersonalInformation.objects.get(user_id=user.id)
            except ObjectDoesNotExist:
                personal_info = None

            request.session['bio'] = personal_info.bio
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
        join_date = datetime.now

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
                skill_5=skill_5, skill_6=skill_6, join_date=join_date)

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
    return render(request, 'profile/dashboard.html')
