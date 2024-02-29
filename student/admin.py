from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.


class TableAdmin(admin.ModelAdmin):
    list_display = ("mentor", "branch", "semester", "section", "gender")  # Ensure each field is a string

class TableAdmin2(admin.ModelAdmin):
    list_display = ("skill_name","student")  # Ensure each field is a string


admin.site.register(Student, TableAdmin)
admin.site.register(students_skills,TableAdmin2)


# user=models.OneToOneField(User,on_delete=models.CASCADE)
#     mentor = models.ForeignKey(mentor, on_delete=models.CASCADE,null=True)
#     branch=models.CharField(max_length=6,null=True)
#     semester=models.IntegerField(null=True)
#     section=models.CharField(max_length=1,blank=True)
#     gender=models.CharField(max_length=10,null=True)  