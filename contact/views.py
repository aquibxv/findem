from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserContact, ProjectContact
from profiles.models import UserProfile
from projects.models import Project
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def contact_profile(request, receiver_id, sender_id):

    # check if user has already made a request
    has_contacted = UserContact.objects.all().filter(sending_user_id=sender_id,
                      receiving_user_id=receiver_id)
    if has_contacted:
        messages.error(request, 'You have already sent a request to this user')
        return redirect('search')

    User = UserProfile.objects.get(id=receiver_id)
    name = User.name
    profile_contact = UserContact(name=name, sending_user_id=sender_id,
                      receiving_user_id=receiver_id)

    profile_contact.save()
    messages.success(request, 'Your request has been sent successfully')  
    return redirect('search')

@login_required
def contact_project(request, project_id):

    project = get_object_or_404(Project, pk=project_id)
    project_name = project.title
    receiver_id = project.user_id
    sender_id = request.user.id

    # check if user has already made a request
    has_contacted = ProjectContact.objects.all().filter(sending_user_id=sender_id,
                    receiving_user_id=receiver_id, project_id=project_id)
    if has_contacted:
        messages.error(request, "You have already made joining request to this project")
        return redirect('dashboard')


    print(str(project_id) + " " + str(receiver_id) + " " + str(sender_id))

    project_contact = ProjectContact(name=project_name, sending_user_id=sender_id,
                        receiving_user_id=receiver_id, project_id=project_id)
    project_contact.save()
    messages.success(request, "Your request has been sent successfully")
    return redirect('dashboard')



    
