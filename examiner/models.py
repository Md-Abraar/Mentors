from django.db import models
from django.contrib.auth.models import User
import student.models as model

    
class Examiner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="user")
    emp_id = models.CharField(max_length=40)
    name = models.CharField(max_length=20,null=True)
    status= models.BooleanField(default=False)
    department=models.CharField(max_length=40,null=True)
    mobile=models.CharField(max_length=13,null=True)
    email=models.CharField(max_length=40,null=True)
    examiner_image = models.ImageField(upload_to='Faculty/')
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.name
    
