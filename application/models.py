# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, User

# MODEL FOR USER 
class CustomUser(AbstractUser):
    DOCTOR = 'dc'
    PATIENT = 'pt'
    NURSE = 'nu'
    USER_TYPES = [
        (DOCTOR, 'doctor'),
        (PATIENT, 'patient'),
        (NURSE, 'nurse'),
    ]
    users = models.CharField(max_length=10, choices=USER_TYPES, default=PATIENT)

# MODEL FOR CLINIC 
class Clinic(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    address = models.CharField(max_length=50)
    website_url = models.URLField()

# MODEL FOR SOCIAL LINKS 
class Social(models.Model):
    facebook_url = models.URLField()
    linkedin_url = models.URLField()
    instagram_url = models.URLField()

# MODEL FOR DOCTOR 
class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    tagline = models.CharField(max_length=30)
    specialization = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()
    experience= models.IntegerField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    social_links = models.ForeignKey(Social, on_delete=models.CASCADE)

# MODEL FOR PATIENT 
class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# MODEL FOR NURSE
class Nurse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    works_under = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
