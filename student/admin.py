from django.contrib import admin

# Register your models here.
from .models import *

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('username','semester','branch','section','gender','mentor')
#     def username(self,obj):
#         return obj.user.username
    
# # Register your models here.
# admin.site.register(Student,StudentAdmin)

# class StudentSkill(admin.ModelAdmin):
#     list_display = ("skill_name","student")

# admin.site.register(students_skills,StudentSkill)



admin.site.register(Student)


admin.site.register(Personal_details)
admin.site.register(Parents_details)
admin.site.register(Education_details)
admin.site.register(Competitive_exam)
admin.site.register(Profile)
admin.site.register(Achievements)
admin.site.register(Skills)
admin.site.register(Certifications)
admin.site.register(Internships)
admin.site.register(Extra_Curriculars)
admin.site.register(Attendance_details)
admin.site.register(Semwise_grades)
admin.site.register(Semester_marks)
admin.site.register(Backlogs)
admin.site.register(Placements)
admin.site.register(Remarks)