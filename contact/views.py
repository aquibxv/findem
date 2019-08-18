from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserContact, ProjectContact, AcceptedProject, AcceptedUser
from .models import SentUserRequest, SentProjectRequest
from profiles.models import UserProfile
from projects.models import Project
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def contact_profile(request, receiver_id):
    """ function to send a profile request to a user  """

    sender_id = request.user.id
    # print("reciever id :" + str(receiver_id))
    # print("sender_id :" + str(sender_id))
    
    # check if sending_user has already made a request to receiving user
    has_contacted = UserContact.objects.all().filter(sending_user_id=sender_id,
                      receiving_user_id=receiver_id)
    if has_contacted:
        messages.error(request, 'You have already sent a request to this user')
        return redirect('search')

     # check if receiving user has already made a request to sending user
    has_contacted = UserContact.objects.all().filter(sending_user_id=receiver_id,
                      receiving_user_id=sender_id)
    if has_contacted:
        messages.error(request, 'a connection request has been already sent by this user')
        return redirect('search')

    # user to which requst has been sent
    User = UserProfile.objects.get(id=receiver_id)
    name = User.name

    # user who is sending the request
    Sending_User = UserProfile.objects.get(id=sender_id)
    sending_user_name = Sending_User.name
    sending_user_picture = Sending_User.profile_picture

    profile_contact = UserContact(name=name, sending_user_name=sending_user_name, sending_user_picture = sending_user_picture,
                      sending_user_id=sender_id, receiving_user_id=receiver_id)

    profile_contact.save()

    #fetch the User whose id = recieving user-id and pop a notification 
    user = UserProfile.objects.get(id=receiver_id)
    user.notification = user.notification + 1
    user.save()

    # create a notification object for the user to whome the request has been sent
    request_obj = SentUserRequest(receiver_id=receiver_id, receiver_name=name,
                    sender_id=sender_id, sender_name=sending_user_name, sender_picture=sending_user_picture)
    request_obj.save()

    messages.success(request, 'Your request has been sent successfully')  
    return redirect('search')

@login_required
def contact_project(request, project_id):
    """ functiont to send a project_request  """

    project = get_object_or_404(Project, pk=project_id)
    project_name = project.title
    receiver_id = project.user_id
    receiver_name = project.author
    sender_id = request.user.id

    # check if user has already made a request
    has_contacted = ProjectContact.objects.all().filter(sending_user_id=sender_id,
                    receiving_user_id=receiver_id, project_id=project_id)
    if has_contacted:
        messages.error(request, "You have already made joining request to this project")
        return redirect('dashboard')

    Sending_User = UserProfile.objects.get(id=sender_id)
    sending_user_name = Sending_User.name
    sending_user_picture = Sending_User.profile_picture
   
    project_contact = ProjectContact(name=project_name, sending_user_name=sending_user_name, sending_user_id=sender_id, 
                        sending_user_picture=sending_user_picture, receiving_user_id=receiver_id, project_id=project_id)
    project_contact.save()

    #fetch the User whose id = recieving user id and pop a notification 
    user = UserProfile.objects.get(id=receiver_id)
    user.notification = user.notification + 1
    user.save()

    #create a notification object for the request sent
    request_obj = SentProjectRequest(receiver_id=receiver_id, receiver_name=receiver_name, 
                    sender_id=sender_id, sender_name=sending_user_name, sender_picture=sending_user_picture,
                    project_name=project_name)
    request_obj.save()

    messages.success(request, "Your request has been sent successfully")
    return redirect('dashboard')

@login_required
def profile_request(request, req_code, contact_id):
    """ functiont to respond to a profile request """

    # if request has been accepted then save a request object
    if req_code == 1:
        contact = UserContact.objects.get(id=contact_id)
        contact.response = True
        user_id = contact.sending_user_id
        user_name = contact.sending_user_name

        receiver_id = contact.receiving_user_id
        receiver = UserProfile.objects.get(id=receiver_id)
        receiver_name = receiver.name
        receiver_picture = receiver.profile_picture
        request = AcceptedUser(receiver_id=receiver_id, receiver_name=receiver_name, 
                                receiver_picture=receiver_picture, user_id=user_id, user_name=user_name)
        
        contact.save()
        request.save()
        
        #fetch the User whose id = sending user id
        user = UserProfile.objects.get(id=contact.sending_user_id)
        user.notification = user.notification + 1
        user.save()

        return redirect('request_recv')
    
    # if request has been rejected then update the response and save
    elif req_code == 0:
        contact = UserContact.objects.get(id=contact_id)
        contact.response = True
        contact.save()
        return redirect('request_recv')

@login_required
def project_request(request, req_code, contact_id):
    """ function to respond to a project request """

    # if request has been accepted then save a request object
    if req_code == 1:
        contact = ProjectContact.objects.get(id=contact_id)
        contact.response = True
        user_id = contact.sending_user_id
        user_name = contact.sending_user_name

        project_name = contact.name
        project = Project.objects.get(title=project_name)
        project_id = project.id 

        receiver_id = contact.receiving_user_id
        receiver = UserProfile.objects.get(id=receiver_id)
        receiver_name = receiver.name
        receiver_picture = receiver.profile_picture
        request = AcceptedProject(receiver_id=receiver_id, project_name=project_name ,project_id=project_id, receiver_name=receiver_name, 
                                receiver_picture=receiver_picture, user_id=user_id, user_name=user_name)
        
        contact.save()
        request.save()

        #fetch the User whose id = sending user id
        user = UserProfile.objects.get(id=contact.sending_user_id)
        user.notification = user.notification + 1;
        user.save()

        return redirect('request_recv')

    # if request has been rejected then update the response and save
    elif req_code == 0:
        contact = ProjectContact.objects.get(id=contact_id)
        contact.response = True
        contact.save()
        return redirect('request_recv')

@login_required
def deleteUserRequests(request, contact_id):
    """view to remove a not-responsed sent reqeust from the system"""

    contact = get_object_or_404(UserContact, pk=contact_id)
    if contact.response == False:
        contact.delete()

    return redirect('requests') 

@login_required
def deleteProjectRequests(request, contact_id):
    """view to remove a not-responsed sent project reques from the system"""

    print("Project_code : " + str(contact_id))
    contact = get_object_or_404(ProjectContact, pk=contact_id)
    if contact.response == False:
        contact.delete()

    return redirect('requests')

@login_required
def delProfileNotification(request, contact_id):
    """ function to delete a profile notification when read"""

    contact = get_object_or_404(AcceptedUser, pk=contact_id)
    if contact:
        contact.delete()
    return redirect('notifications')

@login_required
def delProjectNotification(request, contact_id):
    """ function to read a project notification when read """

    contact = get_object_or_404(AcceptedProject, pk=contact_id)
    if contact:
        contact.delete()
    return redirect('notifications')

@login_required
def delRecvUserNotification(request, contact_id):
    """ method to delete notifcation for a recevied user request """

    contact = get_object_or_404(SentUserRequest, pk=contact_id)
    if contact:
        contact.delete()
    return redirect('notifications')

@login_required
def delRecvProjectNotification(request, contact_id):
    """ method to delete notification for a received project request """

    contact = get_object_or_404(SentProjectRequest, pk=contact_id)
    if contact:
        contact.delete()
    return redirect('notifications')