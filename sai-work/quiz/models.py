from django.db import models
from django.contrib.auth.models import User
from student.models import *
from teacher.models import *

class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField(blank=True,null=True)
   total_marks = models.PositiveIntegerField(blank=True,null=True)
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


class students_skills(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    skill_name = models.CharField(max_length=30)
    test_score = models.IntegerField(null=True, blank=True)
    project_name = models.CharField(max_length=50, null=True, blank=True)
    project_type = models.CharField(max_length=50, null=True, blank=True)
    project_score = models.IntegerField(null=True, blank=True)
    certification_status = models.BooleanField(default=False)
    updated_date = models.DateField(null=True, blank=True)
    assessed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    skill_status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return self.skill_name



class teacher_skills(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True)
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
    exam_id=models.CharField(max_length=30,null=True)
    marks_obtained=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.student.name



