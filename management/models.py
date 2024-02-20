from django.db import models

from student.models import Student
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    # student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class Skill(models.Model):
    skill_name = models.CharField(max_length=50, primary_key=True)
    sector = models.CharField(max_length=30)
    domain = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    parameters = models.TextField()

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
    

