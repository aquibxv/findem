from django.urls import path, include
from . import views

# url - 'contact/'
urlpatterns = [
    path('contact_profile/<int:receiver_id><int:sender_id>', views.contact_profile, name="profile_contact"),
    path('contact_project/<int:project_id>', views.contact_project, name="project_contact"),
]