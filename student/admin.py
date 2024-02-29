from django.contrib import admin

# Register your models here.
from .models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username','semester','branch','section','gender','mentor')
    def username(self,obj):
        return obj.user.username
    
# Register your models here.
admin.site.register(Student,StudentAdmin)

class StudentSkill(admin.ModelAdmin):
    list_display = ("skill_name","student")

admin.site.register(students_skills,StudentSkill)