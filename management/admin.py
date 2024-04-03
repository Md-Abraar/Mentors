from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Skill)
admin.site.register(Faculty)
admin.site.register(Mentorship)



admin.site.register(students_skills)

admin.site.register(examiner_skills)

admin.site.register(student_skill_exam_applications)
admin.site.register(Skills_criteria)
admin.site.register(Registered_skills)