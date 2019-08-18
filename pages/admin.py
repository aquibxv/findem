from django.contrib import admin
from .models import Feedback

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_display_links = ['title', 'author']
    list_per_page = 20

admin.site.register(Feedback, FeedbackAdmin)

