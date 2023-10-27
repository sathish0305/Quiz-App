from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class user_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.IntegerField()

class questions(models.Model):  
    question = models.CharField(max_length=200)
    option_one= models.CharField(max_length=200)
    option_two = models.CharField(max_length=200)
    option_three = models.CharField(max_length=200)
    option_four = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.question