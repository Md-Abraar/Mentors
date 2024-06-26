from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class mentor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=50,null=False)
    status= models.BooleanField(default=False)
    department=models.CharField(max_length=40,null=True)
    mobile=models.CharField(max_length=13,null=True)
    email=models.CharField(max_length=40,null=True)
    mentor_image = models.ImageField(upload_to='static/Faculty/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


