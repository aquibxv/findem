from django.contrib import admin
from .models import UserContact, ProjectContact, AcceptedUser, AcceptedProject
from .models import SentProjectRequest, SentUserRequest

# Register your models here.
class UserContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_date', 'response']
    list_display_links = ['name', 'contact_date']
    list_per_page = 20

class ProjectContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_date', 'response']
    list_display_links = ['name', 'contact_date']
    list_per_page = 20

class AcceptedUserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'receiver_name', 'contact_date']
    list_display_links = ['user_name', 'receiver_name', 'contact_date']
    list_per_page = 20

class AcceptedProjectAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'receiver_name', 'project_name', 'contact_date']
    list_display_links = ['user_name', 'receiver_name', 'project_name', 'contact_date']
    list_per_page = 20

class SentUserRequestAdmin(admin.ModelAdmin):
    list_display = ['receiver_name', 'sender_name', 'contact_date']
    list_display_links = ['receiver_name', 'sender_name', 'contact_date']
    list_per_page = 20

class SentProjectRequestAdmin(admin.ModelAdmin):
    list_display = ['receiver_name', 'sender_name', 'project_name', 'contact_date']
    list_display_links = ['receiver_name', 'sender_name', 'project_name', 'contact_date']
    list_per_page = 20

admin.site.register(UserContact,  UserContactAdmin)
admin.site.register(ProjectContact, ProjectContactAdmin)
admin.site.register(AcceptedUser, AcceptedUserAdmin)
admin.site.register(AcceptedProject, AcceptedProjectAdmin)
admin.site.register(SentUserRequest, SentUserRequestAdmin)
admin.site.register(SentProjectRequest, SentProjectRequestAdmin)


