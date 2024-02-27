from django.db import models
from django.contrib.auth.models import User
from teacher.models import *
from mentor.models import mentor
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mentor = models.ForeignKey(mentor, on_delete=models.CASCADE,null=True,blank=True)
    branch=models.CharField(max_length=6,null=True)
    department=models.CharField(max_length=6,null=True)
    semester=models.IntegerField(null=True)
    section=models.CharField(max_length=1,blank=True)
    gender=models.CharField(max_length=10,null=True)    

    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.username
class Student_profile(models.Model):
    student_id=models.CharField(max_length=10)
    student_fullname=models.CharField(max_length=50)
    branch=models.CharField(max_length=6)
    section=models.CharField(max_length=1,blank=True)
    DOB=models.DateField()
    gender=models.CharField(max_length=10)
    student_phone_no=models.IntegerField()
    student_email_id=models.CharField(max_length=30)

    L_hno=models.CharField(max_length=10)
    L_street=models.CharField(max_length=20)
    L_city=models.CharField(max_length=20)
    L_district=models.CharField(max_length=30)
    L_state=models.CharField(max_length=30)
    L_pincode=models.IntegerField()

    P_hno=models.CharField(max_length=10)
    P_street=models.CharField(max_length=20)
    P_city=models.CharField(max_length=20)
    P_district=models.CharField(max_length=30)
    P_state=models.CharField(max_length=30)
    P_pincode=models.IntegerField()

    residential_details=models.CharField(max_length=20)
    nationality=models.CharField(max_length=20)
    aadhar_number=models.IntegerField()
    category=models.CharField(max_length=1)
    reservation_category=models.CharField(max_length=20)
    bloodgroup=models.CharField(max_length=5)
    ph_status=models.BooleanField()
    student_passportsize_photo=models.FileField(upload_to='static/media/student_files')
    hobbies=models.CharField(max_length=100,null=True,blank=True)
    scholarship=models.CharField(max_length=30,null=True,blank=True)
    transport_mode=models.CharField(max_length=20)
    mother_tongue=models.CharField(max_length=20)
    height=models.IntegerField(null=True,blank=True)
    weight=models.IntegerField(null=True,blank=True)
    illness=models.CharField(max_length=30,null=True,blank=True)

class Education_details(models.Model):
    student_id=models.CharField(max_length=10)
    qualification=models.CharField(max_length=10)
    course=models.CharField(max_length=10, blank=True)
    institute_name=models.CharField(max_length=50)
    insitute_location=models.CharField(max_length=30)
    YOP=models.IntegerField()
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
    guardian_phone_number=models.IntegerField(null=True,blank=True)
    parent_email=models.CharField(max_length=50)

class Competitive_exam(models.Model):
    student_id=models.CharField(max_length=10)
    test_name=models.CharField(max_length=10,blank=True)
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
    semester=models.IntegerField()
    month=models.CharField(max_length=10)
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
    subject_name=models.CharField(max_length=50,blank=True)
    semester=models.IntegerField(blank=True)
    sem_cleared=models.IntegerField(blank=True)
    ayoc=models.IntegerField(blank=True)

class Extra_Curriculars(models.Model):
    student_id=models.CharField(max_length=10)
    activity=models.TextField()
    role=models.TextField()

class Profile(models.Model):
    student_id=models.CharField(max_length=10)
    profile_name=models.CharField(max_length=40)
    profile_url=models.TextField()