from django.db import models
from django.contrib.auth.models import User
import student.models as model
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    emp_id = models.CharField(max_length=40)
    name = models.CharField(max_length=20,null=True)
    status= models.BooleanField(default=False)
    department=models.CharField(max_length=40,null=True)
    mobile=models.CharField(max_length=13,null=True)
    email=models.CharField(max_length=40,null=True)
    skill=models.CharField(max_length=40,null=True)

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.name
    



    
