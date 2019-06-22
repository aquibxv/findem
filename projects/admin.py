from django.contrib import admin
from .models import Project

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'domain', 'project_type', 'live']
    list_display_links = ['title']
    list_filter = ['title', 'domain', 'live', 'project_type']
    search_fields = ['skill_1', 'domain', 'project_type', 'live']
    list_per_page = 20

admin.site.register(Project, ProjectAdmin)