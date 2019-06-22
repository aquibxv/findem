from django.contrib import admin
from .models import UserContact, ProjectContact

# Register your models here.
class UserContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_date', 'response']
    list_display_links = ['name', 'contact_date']
    list_per_page = 20

class ProjectContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_date', 'response']
    list_display_links = ['name', 'contact_date']
    list_per_page = 20

admin.site.register(UserContact,  UserContactAdmin)
admin.site.register(ProjectContact, ProjectContactAdmin)


