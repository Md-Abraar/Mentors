from django.db import models
from django.contrib.auth.models import User

from mentor.models import *

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    name = models.CharField(max_length=40)
    branch = models.CharField(max_length=30,null=True)
    sem = models.CharField(max_length=20,null=True)
    section = models.CharField(max_length=10,null=True)
    
    TD = models.ForeignKey(mentor, on_delete=models.CASCADE, related_name='mentor', null=True)

    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name  

    