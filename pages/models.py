from django.db import models
from datetime import datetime

# Create your models here.
class Feedback(models.Model):
    """ A model for collecting feedback in our system"""
    
    title = models.CharField(max_length=100)
    feedback = models.TextField(max_length=600)
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.title



