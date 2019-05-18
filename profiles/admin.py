from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, PersonalInformation, SocialPlatform, Accomplishments, Location, WorkExperience

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'highest_degree_earned', 'college_name', 'graduation_year']
    list_display_links = ['email', 'name']
    list_filter = ['college_name', 'skill_1']
    search_fields = ['email', 'name', 'college_name']
    list_per_page = 20

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PersonalInformation)
admin.site.register(SocialPlatform)
admin.site.register(Accomplishments)
admin.site.register(Location)
admin.site.register(WorkExperience)