from django.db import models
from datetime import datetime

# Create your models here.
class UserContact(models.Model):
    """Represents a User Contact Model inside our system"""

    name = models.CharField(max_length=40)
    sending_user_name = models.CharField(max_length=40)
    sending_user_picture = models.ImageField()
    sending_user_id = models.IntegerField()
    receiving_user_id = models.IntegerField()
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    response = models.BooleanField(default=False)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.name

class ProjectContact(models.Model):
    """Represents a Project Contact Model inside our system"""

    name = models.CharField(max_length=40)
    sending_user_name = models.CharField(max_length=40)
    sending_user_picture = models.ImageField()
    sending_user_id = models.IntegerField()
    receiving_user_id = models.IntegerField()
    project_id = models.IntegerField()
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    response = models.BooleanField(default=False)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.name

class AcceptedUser(models.Model):
    """describes the model for accepted user requests """

    message = models.CharField(max_length=50, default="has accepted your connection request")
    receiver_id = models.IntegerField()
    receiver_name = models.CharField(max_length=30)
    receiver_picture = models.ImageField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=30)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.user_name

class AcceptedProject(models.Model):
    """describes the model for accepted user requests """

    message = models.CharField(max_length=50, default="has accepted your project request for the project")
    receiver_id = models.IntegerField()
    receiver_name = models.CharField(max_length=30)
    receiver_picture = models.ImageField()
    project_name = models.CharField(max_length=30)
    project_id = models.IntegerField(blank=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=30)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.project_name



    
    