from django.db import models
from django.contrib.auth.models import User
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)

    # @property
    # def get_name(self):
    #     return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    
class teacher_skills(models.Model):
    # teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True)
    skill_name = models.CharField(max_length=30)
    skill_status = models.CharField(max_length=20,default=False)
    def _str_(self):
        return self.skill_name if self.skill_name else "Unnamed Skill"

class Examiner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    emp_id = models.CharField(max_length=40)
    name = models.CharField(max_length=20,null=True)
    status= models.BooleanField(default=False)
    department=models.CharField(max_length=40,null=True)
    mobile=models.CharField(max_length=13,null=True)
    email=models.CharField(max_length=40,null=True)
    skill=models.CharField(max_length=40,null=True)
    examiner_image = models.ImageField(upload_to='Faculty/')
    is_active = models.BooleanField(default=True)
    @property
    def get_instance(self):
        return self

    def _str_(self):
        return self.name
    
