from django.db import models
from datetime import datetime
from profiles.models import UserProfile

# Create your models here.
class Project(models.Model):
    """Represents a Project Model inside our system"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    author = models.CharField(max_length=40, blank=False)
    title = models.CharField(max_length=40, blank=False)
    description = models.TextField(blank=False)
    college = models.CharField(max_length=255, blank=True)
    skill_1 = models.CharField(max_length=40, blank=False)
    skill_2 = models.CharField(max_length=40, blank=True)
    skill_3 = models.CharField(max_length=40, blank=True)
    skill_4 = models.CharField(max_length=40, blank=True)
    photo_1 = models.ImageField(upload_to='', blank=True) 
    photo_2 = models.ImageField(upload_to='', blank=True) 
    photo_3 = models.ImageField(upload_to='', blank=True) 
    link_1 = models.URLField(blank=True)
    link_2 = models.URLField(blank=True)
    link_3 = models.URLField(blank=True)
    domain = models.CharField(max_length=40, blank=False)
    project_type = models.CharField(max_length=40, blank=False)
    resume_inclusion = models.CharField(max_length=10, blank=True)
    live = models.CharField(max_length=10, blank=True)
    deadline = models.DateField(blank=True)
    upload_date = models.DateField(default=datetime.now)
    
    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.author

