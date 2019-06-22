from django.db import models
from datetime import datetime

# Create your models here.
class UserContact(models.Model):
    """Represents a User Contact Model inside our system"""

    name = models.CharField(max_length=40)
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
    sending_user_id = models.IntegerField()
    receiving_user_id = models.IntegerField()
    project_id = models.IntegerField()
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    response = models.BooleanField(default=False)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.name


    