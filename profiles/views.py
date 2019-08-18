from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from profiles.models import UserProfile, PersonalInformation, Location
from django.contrib.auth.decorators import login_required
from .models import UserProfile, PersonalInformation, SocialPlatform, Accomplishments, Location, WorkExperience
from projects.models import Project
from contact.models import UserContact, ProjectContact, AcceptedProject, AcceptedUser
from contact.models import SentUserRequest, SentProjectRequest
from django.contrib.auth.hashers import check_password
from profiles.choices import course_choices, grad_year_choices, branch_choices

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

    # if user is authencticated then remove him from the result
    if request.user.is_authenticated:
        profiles = profiles.exclude(id=request.user.id)

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
    accomplishments = Accomplishments.objects.all().filter(user_id=profile_id)

    # fetching location
    try:
        location = Location.objects.get(user_id=profile_id)
    except ObjectDoesNotExist:
        location = None

    # fetching WorkExperience
    work_exp = WorkExperience.objects.all().filter(user_id=profile_id)

    context = {
        'profile' : profile,
        'socialhandle' : socialhandle,
        'personal_info' : personal_info, 
        'accomplishments': accomplishments, 
        'location' : location,
        'work_exps' : work_exp,
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
        profile_picture = request.FILES.get('inputprofile') or None
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
        join_date = datetime.now()

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

                # if profile_picture != None:
                #     user = UserProfile.objects.create_user(profile_picture=profile_picture, name=name, email=email, 
                #         password=password, highest_degree_earned=highest_degree_earned, college_name=college_name, 
                #         graduation_year=graduation_year, skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4,
                #         skill_5=skill_5, skill_6=skill_6, join_date=join_date)
                # else:
                #     user = UserProfile.objects.create_user(name=name, email=email, 
                #         password=password, highest_degree_earned=highest_degree_earned, college_name=college_name, 
                #         graduation_year=graduation_year, skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4,
                #         skill_5=skill_5, skill_6=skill_6, join_date=join_date)

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

    # if request.user.is_authenticated():
    # fetching presonal-Information
    try:
        personal_info = PersonalInformation.objects.get(user_id=request.user.id)
    except ObjectDoesNotExist:
        personal_info = None

    # fetching projects
    projects = Project.objects.filter(college__icontains=request.user.college_name
                                     ).exclude(user_id=request.user.id
                                     ).filter(live__contains="on")[:2]

    context = {
        'personal_info' : personal_info,
        'projects' : projects,
    }

    return render(request, 'profile/dashboard.html', context)

@login_required
def notifications(request):
    """ view for displaying all the notifications a user has received in the system"""

    user_requests = AcceptedUser.objects.all().filter(user_id=request.user.id)
    project_requests = AcceptedProject.objects.all().filter(user_id=request.user.id)
    received_user_requests = SentUserRequest.objects.all().filter(receiver_id=request.user.id)
    received_project_requests = SentProjectRequest.objects.all().filter(receiver_id=request.user.id)

    # also update the notfications count of the user to 0
    request.user.notification = 0
    request.user.save()

    context = {
        'user_requests' : user_requests,
        'project_requests' : project_requests,
        'received_user_requests' :  received_user_requests,
        'received_project_requests' : received_project_requests,
    }

    return render(request, 'profile/notifications.html', context)

@login_required
def settings(request):
    """functiont to update and set user settings """

    try:
        info = PersonalInformation.objects.get(user=request.user)
    except ObjectDoesNotExist:
        info = None

    try:
        location = Location.objects.get(user=request.user)
    except ObjectDoesNotExist:
        location = None

    # If user has entered a data
    if request.method == 'POST':

        general_val = request.POST.get('general')
        general_val = str(general_val)

        password_val = request.POST.get('password')
        password_val = str(password_val)

        location_val = request.POST.get('location')
        location_val = str(location_val)

        if general_val == '1':
            name = request.POST.get('name')
            email = request.POST.get('mail')
            mobile = request.POST.get('mobile')

            if name:
                if name != request.user.name:
                    request.user.name = name
                    request.user.save()
            if email:
                if email != request.user.email:
                    request.user.email = email
                    request.user.save()
            if mobile:
                if info:
                    if info.mobile:
                        if info.mobile != mobile:
                            info.mobile = mobile
                    else:
                        info.mobile = mobile
                else:
                    # if personal Information for this user doest not exists
                    personal_info = PersonalInformation.objects.create(user=request.user, mobile=mobile)
                    personal_info.save()
                
        elif password_val == '1':
            curr_password = request.POST.get('curr_password')
            curr_password = str(curr_password)

            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            new_password = str(new_password)
            confirm_password = str(confirm_password)

            # if password matches the users password
            if check_password(curr_password, request.user.password):
                # check if the newpassowrd and confirm password matches
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, "Password changed successfully")
                else:
                    messages.error(request, "New password and Confirm password do not match")
                    return redirect('settings')
            else:
                messages.error(request, "Incorrect Password entered!")
                return redirect('settings')

        elif location_val == '1':
            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')

            # if location object already exists
            if location:
                if country: 
                    if location.country != country:
                        location.country = country
                        location.save()
                        # messages.success(request, 'Location updated successfully')
                if state:
                    if location.State != state:
                        location.State = state
                        location.save()
                        # messages.success(request, 'Location updated successfully')
                if city:
                    if location.city != city:
                        location.city = city
                        location.save()
                        # messages.success(request, 'Location updated successfully')
            else:
                # create a new location object
                loc = Location.objects.create(user=request.user, country=country, State=state, city=city)
                loc.save()
                

    context = {
        'info' : info, 
        'location' : location,
    }

    return render(request, 'profile/settings.html', context)

@login_required
def account(request):
    """ Function to update and set user accounts setting """

    # fetch perssonal information of the user
    try:
        personal_info = PersonalInformation.objects.get(user=request.user)
    except ObjectDoesNotExist:
        personal_info = None

    # fetch social platforms of the user
    try:
        Social_Object = SocialPlatform.objects.get(user=request.user)
    except ObjectDoesNotExist:
        Social_Object = None
    

    if request.method == 'POST':
        personal_val = request.POST.get('personal')
        personal_val = str(personal_val)

        skill_val = request.POST.get('skill')
        skill_val = str(skill_val)

        social_val = request.POST.get('social')
        social_val = str(social_val)

        work_val = request.POST.get('work')
        work_val = str(work_val)

        accomplishment_val = request.POST.get('accomplishment')
        accomplishment_val = str(accomplishment_val)

        education_val = request.POST.get('education')
        education_val = str(education_val)

        if personal_val == '1':
            profile_pic = request.FILES.get('profile_pic', None)
            bio = request.POST.get('bio')
            lang1 = request.POST.get('language1')
            lang2 = request.POST.get('language2')
            lang3 = request.POST.get('language3')

            if profile_pic != None:
                request.user.profile_picture = profile_pic
                request.user.save()
                messages.success(request, "Profile picture update successfully")
            if bio:
                if personal_info:
                    if bio != personal_info.bio:
                        personal_info.bio = bio
                        personal_info.save()
                        messages.success(request, "Bio updated successfully")  
                else:
                    info = PersonalInformation.objects.create(user=request.user, bio=bio)
                    info.save()
                    messages.success(request, "Bio updated successfully")
            else:
                if personal_info.bio:
                    personal_info.bio = ' '
                    personal_info.save()
                    messages.success(request, "Bio removed successfully")

            if lang1:
                if personal_info:
                    if lang1 != personal_info.language_1:
                        personal_info.language_1 = lang1
                        personal_info.save()
                        messages.success(request, "Language updated successfully")
                else:
                    info = PersonalInformation.objects.create(user=request.user, language_1 = lang1)
                    info.save()
                    messages.success(request, "Language updated successfully")
            else:
                if personal_info.language_1:
                    personal_info.language_1 = ''
                    personal_info.save()
                    messages.success(request, "Language removed successfully")

            if lang2:
                if personal_info:
                    if personal_info.language_2 != lang2:
                        personal_info.language_2 = lang2
                        personal_info.save()
                        messages.success(request, "Language updated successfully")
                else:
                    info = PersonalInformation.objects.create(user=request.user, language_2 = lang2)
                    info.save()
                    messages.success(request, "Language updated successfully")
            else:
                if personal_info.language_2:
                    personal_info.language_2 = ''
                    personal_info.save()
                    messages.success(request, "Language removed successfully")

            if lang3:
                if personal_info:
                    if personal_info.language_3 != lang3:
                        personal_info.language_3 = lang3
                        personal_info.save()
                        messages.success(request, "Language updated successfully")
                else:
                    info = PersonalInformation.objects.create(user=request.user, language_3 = lang3)
                    info.save()
                    messages.success(request, "Language updated successfully")
            else:
                if personal_info.language_3:
                    personal_info.language_3 = ''
                    personal_info.save()
                    messages.success(request, "Language removed successfully")

        if skill_val == '1':
            skill_1 = request.POST.get('skill1')
            skill_2 = request.POST.get('skill2')
            skill_3 = request.POST.get('skill3')
            skill_4 = request.POST.get('skill4')
            skill_5 = request.POST.get('skill5')
            skill_6 = request.POST.get('skill6')

            if skill_1:
                if request.user.skill_1:
                    if request.user.skill_1 != skill_1:
                        request.user.skill_1 = skill_1
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_1 = skill_1
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            if skill_2:
                if request.user.skill_2:
                    if request.user.skill_2 != skill_2:
                        request.user.skill_2 = skill_2
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_2 = skill_2
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            else:
                if request.user.skill_2:
                    request.user.skill_2 = ''
                    request.user.save()
                    messages.success(request, "Skill removed successfully")

            if skill_3:
                if request.user.skill_3:
                    if request.user.skill_3 != skill_3:
                        request.user.skill_3 = skill_3
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_3 = skill_3
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            else:
                if request.user.skill_3:
                    request.user.skill_3 = ''
                    request.user.save()
                    messages.success(request, "Skill removed successfully")

            if skill_4:
                if request.user.skill_4:
                    if request.user.skill_4 != skill_4:
                        request.user.skill_4 = skill_4
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_4 = skill_4
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            else:
                if request.user.skill_4:
                    request.user.skill_4 = ''
                    request.user.save()
                    messages.success(request, "Skill removed successfully")

            if skill_5:
                if request.user.skill_5:
                    if request.user.skill_5 != skill_5:
                        request.user.skill_5 = skill_5
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_5 = skill_5
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            else:
                if request.user.skill_5:
                    request.user.skill_5 = ''
                    request.user.save()
                    messages.success(request, "Skill removed successfully")

            if skill_6:
                if request.user.skill_6:
                    if request.user.skill_6 != skill_6:
                        request.user.skill_6 = skill_6
                        request.user.save()
                        messages.success(request, "Skill uploaded successfully")
                else:
                    request.user.skill_6 = skill_6
                    request.user.save()
                    messages.success(request, "Skill uploaded successfully")
            else:
                if request.user.skill_6:
                    request.user.skill_6 = ''
                    request.user.save()
                    messages.success(request, "Skill removed successfully")
            
        if social_val == '1':
            
            website = request.POST.get('website')
            linkedin = request.POST.get('linkedin')
            facebook = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            instagram = request.POST.get('instagram')
            youtube = request.POST.get('youtube')
            github = request.POST.get('github')
            hackerRank = request.POST.get('hackerrank')
            medium = request.POST.get('medium')
            quora = request.POST.get('quora')

            if website:
                if Social_Object:
                    if Social_Object.website:
                        if Social_Object.website != website:
                            Social_Object.website = website
                            Social_Object.save()
                            messages.success(request, 'Website information updated successfully')
                    else:
                        Social_Object.website = website
                        Social_Object.save()
                        messages.success(request, 'Website information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, website=website)
                    social.save()
                    messages.success(request, 'Website information updated successfully')
            else:
                if Social_Object.website:
                    Social_Object.website = ''
                    Social_Object.save()
                    messages.success(request, 'Website information removed successfully')

            if linkedin:
                if Social_Object:
                    if Social_Object.linkedIn:
                        if Social_Object.linkedIn != linkedin:
                            Social_Object.linkedIn = linkedin
                            Social_Object.save()
                            messages.success(request, 'linkedin information updated successfully')
                    else:
                        Social_Object.linkedIn = linkedin
                        Social_Object.save()
                        messages.success(request, 'linkedin information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, linkedIn=linkedin)
                    social.save()
                    messages.success(request, 'linkedin information updated successfully')
            else:
                if Social_Object.linkedIn:
                    Social_Object.linkedIn = ''
                    Social_Object.save()
                    messages.success(request, 'linkedin information removed successfully')
            
            if facebook:
                if Social_Object:
                    if Social_Object.facebook:
                        if Social_Object.facebook != facebook:
                            Social_Object.facebook = facebook
                            Social_Object.save()
                            messages.success(request, 'Website information updated successfully')
                    else:
                        Social_Object.facebook = facebook
                        Social_Object.save()
                        messages.success(request, 'Facebook information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, facebook=facebook)
                    social.save()
                    messages.success(request, 'Facebook information updated successfully')
            else:
                if Social_Object.facebook:
                    Social_Object.facebook = ''
                    Social_Object.save()
                    messages.success(request, 'Facebook information removed successfully')

            if twitter:
                if Social_Object:
                    if Social_Object.twitter:
                        if Social_Object.twitter != twitter:
                            Social_Object.twitter = twitter
                            Social_Object.save()
                            messages.success(request, 'twitter information updated successfully')
                    else:
                        Social_Object.twitter = twitter
                        Social_Object.save()
                        messages.success(request, 'twitter information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, twitter=twitter)
                    social.save()
                    messages.success(request, 'twitter information updated successfully')
            else:
                if Social_Object.twitter:
                    Social_Object.twitter = ''
                    Social_Object.save()
                    messages.success(request, 'twitter information removed successfully')

            if instagram:
                if Social_Object:
                    if Social_Object.instagram:
                        if Social_Object.instagram != instagram:
                            Social_Object.instagram = instagram
                            Social_Object.save()
                            messages.success(request, 'instagram information updated successfully')
                    else:
                        Social_Object.instagram = instagram
                        Social_Object.save()
                        messages.success(request, 'instagram information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, instagram=instagram)
                    social.save()
                    messages.success(request, 'instagram information updated successfully')
            else:
                if Social_Object.instagram:
                    Social_Object.instagram = ''
                    Social_Object.save()
                    messages.success(request, 'instagram information removed successfully')

            if instagram:
                if Social_Object:
                    if Social_Object.instagram:
                        if Social_Object.instagram != instagram:
                            Social_Object.instagram = instagram
                            Social_Object.save()
                            messages.success(request, 'instagram information updated successfully')
                    else:
                        Social_Object.instagram = instagram
                        Social_Object.save()
                        messages.success(request, 'instagram information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, instagram=instagram)
                    social.save()
                    messages.success(request, 'instagram information updated successfully')
            else:
                if Social_Object.instagram:
                    Social_Object.instagram = ''
                    Social_Object.save()
                    messages.success(request, 'instagram information removed successfully')

            if youtube:
                if Social_Object:
                    if Social_Object.youtube:
                        if Social_Object.youtube != youtube:
                            Social_Object.youtube = youtube
                            Social_Object.save()
                            messages.success(request, 'youtube information updated successfully')
                    else:
                        Social_Object.youtube = youtube
                        Social_Object.save()
                        messages.success(request, 'youtube information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, youtube=youtube)
                    social.save()
                    messages.success(request, 'youtube information updated successfully')
            else:
                if Social_Object.youtube:
                    Social_Object.youtube = ''
                    Social_Object.save()
                    messages.success(request, 'youtube information removed successfully')

            if github:
                if Social_Object:
                    if Social_Object.github:
                        if Social_Object.github != github:
                            Social_Object.github = github
                            Social_Object.save()
                            messages.success(request, 'github information updated successfully')
                    else:
                        Social_Object.github = github
                        Social_Object.save()
                        messages.success(request, 'github information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, github=github)
                    social.save()
                    messages.success(request, 'github information updated successfully')
            else:
                if Social_Object.github:
                    Social_Object.github = ''
                    Social_Object.save()
                    messages.success(request, 'github information removed successfully')

            if hackerRank:
                if Social_Object:
                    if Social_Object.hackerRank:
                        if Social_Object.hackerRank != hackerRank:
                            Social_Object.hackerRank = hackerRank
                            Social_Object.save()
                            messages.success(request, 'hackerRank information updated successfully')
                    else:
                        Social_Object.hackerRank = hackerRank
                        Social_Object.save()
                        messages.success(request, 'hackerRank information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, hackerRank=hackerRank)
                    social.save()
                    messages.success(request, 'hackerRank information updated successfully')
            else:
                if Social_Object.hackerRank:
                    Social_Object.hackerRank = ''
                    Social_Object.save()
                    messages.success(request, 'hackerRank information removed successfully')

            if medium:
                if Social_Object:
                    if Social_Object.medium:
                        if Social_Object.medium != medium:
                            Social_Object.medium = medium
                            Social_Object.save()
                            messages.success(request, 'medium information updated successfully')
                    else:
                        Social_Object.medium = medium
                        Social_Object.save()
                        messages.success(request, 'medium information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, medium=medium)
                    social.save()
                    messages.success(request, 'medium information updated successfully')
            else:
                if Social_Object.medium:
                    Social_Object.medium = ''
                    Social_Object.save()
                    messages.success(request, 'medium information removed successfully')

            if quora:
                if Social_Object:
                    if Social_Object.quora:
                        if Social_Object.quora != quora:
                            Social_Object.quora = quora
                            Social_Object.save()
                            messages.success(request, 'quora information updated successfully')
                    else:
                        Social_Object.quora = quora
                        Social_Object.save()
                        messages.success(request, 'quora information updated successfully')
                else:
                    social = SocialPlatform.objects.create(user=request.user, quora=quora)
                    social.save()
                    messages.success(request, 'quora information updated successfully')
            else:
                if Social_Object.quora:
                    Social_Object.quora = ''
                    Social_Object.save()
                    messages.success(request, 'quora information removed successfully')

        if accomplishment_val == '1':
            title = request.POST.get('title')
            description = request.POST.get('description')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')

            accomplishment_obj = Accomplishments.objects.create(user=request.user, project_title=title,
                                project_description=description, from_date=from_date, to_date=to_date)
            accomplishment_obj.save()
            messages.success(request, 'Project details uploaded successfully')

        if work_val == '1':
            title = request.POST.get('title')
            company = request.POST.get('company')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            description = request.POST.get('description')

            work_obj = WorkExperience.objects.create(user=request.user, title=title, company=company,
                        from_date=from_date, to_date=to_date, description=description)
            work_obj.save()
            messages.success(request, 'Work experience details added successfully')

        if education_val == '1':
            collage = request.POST.get('collage')
            course  = request.POST.get('course')
            branch  = request.POST.get('branch')
            grad_year = request.POST.get('grad_year')

            if collage:
                if request.user.college_name != collage:
                    request.user.college_name = collage
                    request.user.save()
                    messages.success(request, 'Collage name updated successfully')
                
            if course:
                if request.user.highest_degree_earned != course:
                    request.user.highest_degree_earned = course
                    request.user.save()
                    messages.success(request, 'Course detail updated successfully')

            if branch:
                if personal_info:
                    if personal_info.branch:
                        if personal_info.branch != branch:
                            personal_info.branch = branch
                            personal_info.save()
                            messages.success(request, 'Branch detail updated successfully')
                    else:
                        personal_info.branch = branch
                        personal_info.save()
                        messages.success(request, 'Branch detail updated successfully')
                else:
                    info = PersonalInformation.objects.create(user=request.user, branch=branch)
                    info.save()
                    messages.success(request, 'Branch detail updated successfully')

            if grad_year:
                if request.user.graduation_year != grad_year:
                    request.user.graduation_year = grad_year
                    request.user.save()
                    messages.success(request, 'Graduation year detail updated successfully')



    context = {
            'personal_info' : personal_info,
            'social_info' : Social_Object,
            'courses_choices' : course_choices, 
            'grad_year_choices' : grad_year_choices,
            'branch_choices' : branch_choices,
        }

    return render(request, 'profile/account.html', context)

@login_required
def myProjects(request):
    """View for displaying a users projects in the system"""

    projects = Project.objects.order_by('-upload_date')
    projects = projects.filter(user_id=request.user.id)

    context = {
        'projects' : projects
    }

    return render(request, 'profile/my_project.html', context)

@login_required
def requests(request):
    """View for displaying user's sent requests in the system"""
    
    user_requests = UserContact.objects.all().filter(sending_user_id=request.user.id).filter(response=False)
    project_requests = ProjectContact.objects.all().filter(sending_user_id=request.user.id).filter(response=False)

    context = {
        'user_requests' : user_requests,
        'project_requests' : project_requests, 
    }

    return render(request, 'profile/request.html', context)

@login_required
def requests_recv(request):
    """View for displaying user's received requests in the system"""

    user_requests = UserContact.objects.all().filter(receiving_user_id=request.user.id).filter(response=False)
    project_requests = ProjectContact.objects.all().filter(receiving_user_id=request.user.id).filter(response=False)

    context = {
        'user_requests' : user_requests,
        'project_requests' : project_requests, 
    }

    return render(request, 'profile/request_recv.html', context)

@login_required
def message(request):
    """View for displaying user messages"""
    
    return render(request, 'profile/messages.html') 

@login_required
def browseProject(request):
    """View for Browsing and Seraching projects inside out system"""

    return render(request, 'profile/browse_project.html')