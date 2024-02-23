from django.contrib import admin

# Register your models here.
from .models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username','semester','branch','section','gender')
    def username(self,obj):
        return obj.user.username
    
# Register your models here.
admin.site.register(Student,StudentAdmin)