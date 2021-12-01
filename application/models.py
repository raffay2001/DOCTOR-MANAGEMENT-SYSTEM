# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
import json


# MODEL FOR USER 
class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    NURSE = 'nurse'
    USER_TYPES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
        (NURSE, 'Nurse'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=PATIENT)
    profile_picture = models.ImageField(upload_to = "profile-pictures", null = True, blank = True, default = None)
    phone = models.IntegerField(default = 456465465656)

    def get_profile_picture(self):
        if not self.profile_picture:
            image_file = os.path.join('profile-pictures', f'{self.user_type}-image.jpg')
            return image_file
        return self.profile_picture

    def get_profile(self):
        if self.user_type == "doctor":
            return Doctor.objects.get(user = self)
        elif self.user_type == "patient":
            return Patient.objects.get(user = self)
        else:
            return Nurse.objects.get(user = self)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Day(models.Model):
    key = models.CharField(max_length = 3)
    value = models.CharField(max_length = 10)

    def __str__(self):
        return self.value


class Availability(models.Model):
    duration = models.IntegerField()
    days = models.ManyToManyField(Day)
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

    def split_time(self, value):
        my_list = str(value).split(":")
        my_list.pop()
        new_string = ":".join(my_list)
        return new_string

    def get_start_time(self):
        return self.split_time(self.start_time)

    def get_end_time(self):
        return self.split_time(self.end_time)

    def get_days_list(self):
        day_list = self.days.values_list('key', flat=True)
        day_list = list(day_list)
        return json.dumps(day_list)
    
    def get_days_list_py(self):
        day_list = self.days.values_list('key', flat=True)
        day_list = list(day_list)
        return day_list


# MODEL FOR CLINIC 
class Clinic(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    address = models.CharField(max_length=50)
    website_url = models.URLField()

# MODEL FOR SOCIAL LINKS 
class Social(models.Model):
    facebook_url = models.URLField(null = True, blank = True)
    linkedin_url = models.URLField(null = True, blank = True)
    instagram_url = models.URLField(null = True, blank = True)
    twitter_url = models.URLField(null = True, blank = True)

    def get_list(self):
        my_list = []
        if self.facebook_url:
            my_list.append(('bi bi-facebook', self.facebook_url))
        
        if self.linkedin_url:
            my_list.append(('bi bi-linkedin', self.linkedin_url))
        
        if self.instagram_url:
            my_list.append(('bi bi-instagram', self.instagram_url))
        
        if self.twitter_url:
            my_list.append(('bi bi-twitter', self.twitter_url))

        return my_list
        
        

# MODEL FOR DOCTOR 
class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    tagline = models.CharField(max_length=30)
    specialization = models.CharField(max_length=30)
    description = models.TextField()
    experience= models.IntegerField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    social_links = models.ForeignKey(Social, on_delete=models.CASCADE, null = True, blank = True)


    def parameters(self):
        return [
            ('Email', self.user.email),
            ('Phone', f'+{self.user.phone}'),
            ('Specialization', self.specialization),
            ('Experience', f'{self.experience} years'),
        ]


# MODEL FOR PATIENT 
class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# MODEL FOR NURSE
class Nurse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    works_under = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
