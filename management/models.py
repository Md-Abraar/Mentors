from django.db import models
from django.contrib.auth.models import User
from student.models import *
# from teacher.models import *
from examiner.models import *


class Skills_criteria(models.Model):
    skill_name = models.CharField(max_length=50, primary_key=True)
    sector = models.CharField(max_length=30)
    domain = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    parameters = models.TextField(null=True,blank=True)

class Registered_skills(models.Model):
    skill_name = models.CharField(max_length=50, primary_key=True)
    sector = models.CharField(max_length=30)
    domain = models.CharField(max_length=50)
    level = models.CharField(max_length=15,blank=True,null=True)
    status = models.CharField(max_length=15,blank=True,null=True)
    def __str__(self) -> str:
        return self.skill_name

class Course(models.Model):
    # skill_belongs=models.ForeignKey(Skills_criteria,on_delete=models.CASCADE,default=None)
    skill_name=models.CharField(max_length=50,default="")
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField(blank=True,null=True)
    total_marks = models.PositiveIntegerField(blank=True,null=True)
    passcode=models.CharField(max_length=50,blank=True,null=True)
    examiner_id=models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField(blank=True,null=True)
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    def __str__(self):
        return self.course

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.exam.course_name

class students_skills(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    skill_name = models.CharField(max_length=30)
    test_score = models.IntegerField(null=True, blank=True)
    project_name = models.CharField(max_length=50, null=True, blank=True)
    project_type = models.CharField(max_length=50, null=True, blank=True)
    project_score = models.IntegerField(null=True, blank=True)
    certification_status = models.BooleanField(default=False)
    updated_date = models.DateField(null=True, blank=True)
    assessed_by = models.ForeignKey(Examiner, on_delete=models.SET_NULL, null=True, blank=True)
    skill_status = models.CharField(max_length=20, default="pending")
    overall_score=models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.skill_name 
    

 

# class teacher_skills(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True)
#     skill_name = models.CharField(max_length=30)
#     skill_status = models.CharField(max_length=20,default=False)
#     def __str__(self):
#         return self.skill_name if self.skill_name else "Unnamed Skill"


class examiner_skills(models.Model):
    examiner = models.ForeignKey(Examiner, on_delete=models.SET_NULL,null=True)
    skill_name = models.CharField(max_length=30)
    skill_status = models.CharField(max_length=20,default=False)
    def __str__(self):
        return self.skill_name if self.skill_name else "Unnamed Skill"
    

class student_skill_exam_applications(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,null=True)
    sem = models.IntegerField(null=True,blank=True)
    branch = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    mentor_identity_number = models.CharField(max_length=30)
    requested_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    application_status = models.CharField(max_length=30,default="pending")
    skill_name = models.CharField(max_length=30)
    assessed_by = models.CharField(max_length=30)
    exam_id=models.CharField(max_length=30,blank=True,null=True)
    marks_obtained=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return self.student.name








class Skill(models.Model):
    skill_name = models.CharField(max_length=50, primary_key=True)
    sector = models.CharField(max_length=30)
    domain = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    status= models.BooleanField(default=False)

    def __str__(self):
        return self.skill_name

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10)
    faculty_name = models.CharField(max_length=30)
    faculty_branch = models.CharField(max_length=30)
    faculty_designation= models.CharField(max_length=25)
    skill_set  = models.ManyToManyField(Skill)
    faculty_email = models.EmailField()
    faculty_phone = models.CharField(max_length=10)
    faculty_image = models.ImageField(upload_to='static/Faculty/')

class Mentorship(models.Model):
    mentor_id = models.CharField(max_length=30, primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    # def save(self, *args, **kwargs):
    # # Call the superclass's save method to create the Student object
    #     super().save(*args, **kwargs)
    #     # Check if the skill already exists
    #     existing_skill = Skill.objects.filter(
    #         skill_name=self.skill_name,
    #         domain=self.domain,
    #         sector=self.sector,
    #         level=self.level
    #     ).first()
    #     if existing_skill:
    #         # Skill already exists, update it
    #         existing_skill.save()
    #     else:
    #         # Skill does not exist, create a new one
    #         new_skill = Skill.objects.create(
    #             skill_name=self.skill_name,
    #             domain=self.domain,
    #             sector=self.sector,
    #             level=self.level
    #         )
    