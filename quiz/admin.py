from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(students_skills)
admin.site.register(teacher_skills)
admin.site.register(student_skill_exam_applications)
admin.site.register(Skills_criteria)