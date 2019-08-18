from django.urls import path, include
from . import views

# url - 'contact/'
urlpatterns = [
    path('contact_profile/<int:receiver_id>', views.contact_profile, name="profile_contact"),
    path('contact_project/<int:project_id>', views.contact_project, name="project_contact"),
    path('request_profile/<int:req_code> <int:contact_id>', views.profile_request, name="profile_request"),
    path('request_project/<int:req_code> <int:contact_id>', views.project_request, name="project_request"),
    path('delete_profile_request/<int:contact_id>', views.deleteUserRequests, name='delete_user_request'),
    path('delete_project_request/<int:contact_id>', views.deleteProjectRequests, name='delete_project_request'),
    path('delete_profile_notif/<int:contact_id>', views.delProfileNotification, name='delete_profile_notif'),
    path('delete_project_notif/<int:contact_id>', views.delProjectNotification, name='delete_project_notif'),
    path('delete_rec_profile_notif/<int:contact_id>', views.delRecvUserNotification, name='delete_recev_profile_notification'),
    path('delete_rec_project_notif/<int:contact_id>', views.delRecvProjectNotification, name='delete_recev_project_notification'),
]