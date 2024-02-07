from django.db import models
from django.contrib.auth.models import User

from teacher.models import *
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    TD = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher',default=1)

class Student_profile(models.Model):
    student_id=models.CharField(max_length=10)
    student_fullname=models.CharField(max_length=50)
    branch=models.CharField(max_length=6)
    section=models.CharField(max_length=1,blank=True)
    DOB=models.DateField()
    gender=models.CharField(max_length=10)
    student_phone_no=models.Integerfield(max_length=20)
    student_email_id=models.CharField(max_length=30)

    L_hno=models.CharField()
    L_street=models.CharField()
    L_city=models.CharField()
    L_district=models.CharField()
    L_state=models.CharField()
    L_pincode=models.Integerfield(max_length=6)

    P_hno=models.CharField()
    P_street=models.CharField()
    P_city=models.CharField()
    P_district=models.CharField()
    P_state=models.CharField()
    P_pincode=models.Integerfield(max_length=6)

    residential_details=models.CharField()
    nationality=models.CharField()
    aadhar_number=models.Integerfield(max_length=12)
    category=models.CharField(max_length=1)
    reservation_category=models.CharField()
    bloodgroup=models.CharField()
    ph_status=models.BooleanField()
    student_passportsize_photo=models.FileField(upload_to='static/media/student_files')
    hobbies=models.CharField(null=True,blank=True)
    scholarship=models.CharField(null=True,blank=True)
    transport_mode=models.CharField()
    mother_tongue=models.CharField()
    height=models.Integerfield(null=True,blank=True)
    weight=models.Integerfield(null=True,blank=True)
    illness=models.CharField(null=True,blank=True)

class Education_details(models.Model):
    student_id=models.CharField(max_length=10)
    qualification=models.CharField(max_length=10)
    course=models.CharField(max_length=10, blank=True)
    institute_name=models.CharField(max_length=50)
    insitute_location=models.CharField(max_length=30)
    YOP=models.Integerfield()
    board=models.CharField(max_length=20)
    percentage=models.IntegerField()
    gpa=models.FloatField()
    medium=models.CharField(max_length=10)

class Parents_details(models.Model):
    student_id=models.CharField(max_length=10)
    father_name=models.CharField(max_length=40,null=True,blank=True)
    father_occupation=models.CharField(max_length=40,null=True,blank=True)
    father_phone_number=models.IntegerField(null=True,blank=True)
    mother_name=models.CharField(max_length=50,null=True,blank=True)
    mother_occupation=models.CharField(max_length=50,null=True,blank=True)
    mother_phone_number=models.IntegerField(null=True,blank=True)
    guardian_name=models.CharField(max_length=50,null=True,blank=True)
    guardian_occupation=models.CharField(max_length=50,null=True,blank=True)
    guardian_phone_number=models.IntegerField(max_length=50,null=True,blank=True)
    parent_email=models.CharField(max_length=50)

class Competitive_exam(models.Model):
    student_id=models.CharField(max_length=10)
    test_name=models.CharField(blank=True)
    rank_obtained=models.IntegerField(blank=True)
    score_obtained=models.IntegerField(blank=True)

class Remarks(models.Model):
    student_id=models.CharField(max_length=10)
    remarks_date=models.DateField(null=True,blank=True)
    student_views=models.TextField(null=True,blank=True)
    mentor_remarks=models.TextField(null=True,blank=True)
    semester=models.IntegerField(null=True,blank=True)

class Attendance(models.Model):
    student_id=models.CharField(max_length=10)
    semester=models.IntegeField()
    month=models.CharField()
    phase=models.IntegerField()
    percentage=models.FloatField()

class Achievements(models.Model):
    student_id=models.CharField(max_length=10)
    achieve_name=models.CharField(max_length=50,blank=True)
    achieve_score=models.IntegerField(blank=True)

class Skills(models.Model):
    student_id=models.CharField(max_length=10)
    skill_name=models.CharField(max_length=50,null=True,blank=True)
    test_score=models.IntegerField(null=True,blank=True)
    project_score=models.IntegerField(null=True,blank=True)
    updated_date=models.DateField(null=True,blank=True)
    faculty_id=models.IntegerField(null=True,blank=True)

class Certifications(models.Model):
    student_id=models.CharField(max_length=10)
    certificate_name=models.CharField(max_length=50, blank=True)
    certificate_score=models.IntegerField(blank=True)
    certificate_date=models.DateField(blank=True)

class Internships(models.Model):
    student_id=models.CharField(max_length=10)
    tech_name=models.CharField(max_length=50)
    internship_name=models.CharField(max_length=50)
    internship_mode=models.CharField(max_length=10)
    internship_duration=models.IntegerField()
    date_of_completion=models.DateField()
    stipend=models.IntegerField(blank=True)

class Placements(models.Model):
    student_id=models.CharField(max_length=10)
    company=models.CharField(max_length=50,blank=True)
    date_placed=models.DateField()
    package=models.IntegerField()
    drive_mode=models.CharField(max_length=10)

class Semwise_grades(models.Model):
    student_id=models.CharField(max_length=10)
    semester=models.IntegerField()
    sgpa=models.IntegerField()
    cgpa=models.IntegerField()

class Semester_marks(models.Model):
    student_id=models.CharField(max_length=10)
    subject_name=models.CharField(max_length=50)
    subject_type=models.CharField(max_length=20)
    first_sessional=models.IntegerField()
    second_sessional=models.IntegerField()
    semester=models.IntegerField()
    grade_obtained=models.CharField(max_length=2)

class Backlogs(models.Model):
    student_id=models.CharField(max_length=10)
    subject_name=models.CharField(blank=True)
    semester=models.IntegerField(blank=True)
    sem_cleared=models.IntegerField(blank=True)
    ayoc=models.IntegerField(blank=True)

class Extra_Curriculars(models.Model):
    student_id=models.CharField(max_length=10)
    activity=models.TextField()
    role=models.TextField()

class Profile(models.Model):
    student_id=models.CharField(max_length=10)
    profile_name=models.CharField()
    profile_url=models.TextField()

    
@property
def get_name(self):
    return self.user.first_name+" "+self.user.last_name
@property
def get_instance(self):
    return self
def __str__(self):
    return self.user.first_name