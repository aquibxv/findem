from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from .documents import ProfileIndex

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model.""" 

    def create_user(self, email, name, profile_picture, highest_degree_earned, 
                    college_name ,graduation_year, skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, join_date, password=None):
        """Creates a new user profile object."""
        if not email:  
            raise ValueError("Uers must have an email address")

        # turns the email to lower case and saves it in user object
        email = self.normalize_email(email)

        # if profile_picture is set as none
        if profile_picture == None:
            profile_picture = 'photos/user.gif'


        user = self.model(email=email, name=name, profile_picture=profile_picture, highest_degree_earned=highest_degree_earned,
                college_name=college_name, graduation_year=graduation_year, skill_1=skill_1, skill_2=skill_2,
                skill_3=skill_3, skill_4=skill_4, skill_5=skill_5, skill_6=skill_6, join_date=join_date)

        # hashes the given password and then saves it
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given details"""
        
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
  
        user.save(using=self._db)

        return user
        
# sertting up a default profile picture
profile_pic = 'photos/user.gif'

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user profile inside our system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default=profile_pic)
    profile_picture = models.ImageField(upload_to='photos/profile_pictures/', default='photos/profile_pictures/user.gif', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    highest_degree_earned = models.CharField(max_length=255, blank=False)
    college_name = models.CharField(max_length=255, blank=False)
    graduation_year = models.IntegerField(default=2020, blank=False)
    skill_1 = models.CharField(max_length=20, blank=False)
    skill_2 = models.CharField(max_length=20, blank=True, null=True)
    skill_3 = models.CharField(max_length=20, blank=True, null=True)
    skill_4 = models.CharField(max_length=20, blank=True, null=True)
    skill_5 = models.CharField(max_length=20, blank=True, null=True)
    skill_6 = models.CharField(max_length=20, blank=True, null=True)
    project_count = models.IntegerField(blank=True, default=0, null=True)
    notification = models.IntegerField(blank=True, default=0, null=True)
    join_date = models.DateTimeField(default = datetime.now)
    

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.email

    def indexing(self):
        obj = ProfileIndex(
            college_name=self.college_name,
            name=self.name,
            skill_1=self.skill_1,
            skill_2=self.skill_2,
            skill_3=self.skill_3,
            skill_4=self.skill_4,
            skill_5=self.skill_5,
            skill_6=self.skill_6,
        )

        obj.save()
        return obj.to_dict(include_meta=True)



class PersonalInformation(models.Model):
    """Represents a user's personal Infromation inside our system"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10 ,blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    language_1 = models.CharField(max_length=100, blank=True, null=True)
    language_2 = models.CharField(max_length=100, blank=True, null=True)
    language_3 = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    college_university = models.CharField(max_length=500, blank=True, null=True)
    

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.user.name

class SocialPlatform(models.Model):
    """ Attaches all the Social Platform to a user """

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    website = models.URLField(blank=True, default='', null=True)
    linkedIn = models.URLField(blank=True, default='', null=True)
    facebook = models.URLField(blank=True, default='', null=True)
    twitter = models.URLField(blank=True, default='', null=True)
    instagram = models.URLField(blank=True, default='', null=True)
    youtube = models.URLField(blank=True, default='', null=True)
    github = models.URLField(blank=True, default='', null=True)
    hackerRank = models.URLField(blank=True, default='', null=True)
    medium = models.URLField(blank=True, default='', null=True)
    quora = models.URLField(blank=True, default='', null=True)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.facebook

class Accomplishments(models.Model):
    """Represent's a users accomplishment's inside our system"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    # test_score = models.CharField(max_length=100, blank=True)
    # test_description = models.TextField(blank=True)
    # test_date = models.DateField(blank=True)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.project_title

class WorkExperience(models.Model):
    """Represents a users work experience details in out system"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    description = models.TextField(max_length=500)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.title

class Location(models.Model):
    """Reperesents a users location details in our system"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    country = models.CharField(max_length=200, blank=True, null=True)
    State = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """Django uses this to convert an object to a string"""
        return self.city
