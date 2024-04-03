from django.db import models
from django.contrib.auth.models import User
from examiner.models import Examiner as Tmodel
# from management.models import Skill as skill

from mentor.models import mentor
class Student(models.Model):
    name = models.CharField(max_length=40,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll=models.CharField(max_length=40,null=True)

    mentor = models.ForeignKey(mentor, on_delete=models.CASCADE,null=True,blank=True)
    branch=models.CharField(max_length=6,null=True)
    department=models.CharField(max_length=6,null=True)
    semester=models.IntegerField(null=True)
    section=models.CharField(max_length=1,blank=True)
    gender=models.CharField(max_length=10,null=True)
    profile_score = models.IntegerField(default=0)   

    def __str__(self):
        return self.user.username
    

# class Student_profile(models.Model):
#     student_id=models.CharField(max_length=10)
#     student_fullname=models.CharField(max_length=50)
#     branch=models.CharField(max_length=6)
#     section=models.CharField(max_length=1,blank=True)
#     DOB=models.DateField()
#     gender=models.CharField(max_length=10)
#     student_phone_no=models.IntegerField()
#     student_email_id=models.CharField(max_length=30)

#     L_hno=models.CharField(max_length=10)
#     L_street=models.CharField(max_length=20)
#     L_city=models.CharField(max_length=20)
#     L_district=models.CharField(max_length=30)
#     L_state=models.CharField(max_length=30)
#     L_pincode=models.IntegerField()

#     P_hno=models.CharField(max_length=10)
#     P_street=models.CharField(max_length=20)
#     P_city=models.CharField(max_length=20)
#     P_district=models.CharField(max_length=30)
#     P_state=models.CharField(max_length=30)
#     P_pincode=models.IntegerField()

#     residential_details=models.CharField(max_length=20)
#     nationality=models.CharField(max_length=20)
#     aadhar_number=models.IntegerField()
#     category=models.CharField(max_length=1)
#     reservation_category=models.CharField(max_length=20)
#     bloodgroup=models.CharField(max_length=5)
#     ph_status=models.BooleanField()
#     student_passportsize_photo=models.FileField(upload_to='static/media/student_files')
#     hobbies=models.CharField(max_length=100,null=True,blank=True)
#     scholarship=models.CharField(max_length=30,null=True,blank=True)
#     transport_mode=models.CharField(max_length=20)
#     mother_tongue=models.CharField(max_length=20)
#     height=models.IntegerField(null=True,blank=True)
#     weight=models.IntegerField(null=True,blank=True)
#     illness=models.CharField(max_length=30,null=True,blank=True)


class Personal_details(models.Model): #student
    student_id=models.CharField(max_length=15,null=True)
    student_fullname=models.CharField(max_length=50)
    branch=models.CharField(max_length=6,default='',null=True,blank=True)
    section=models.CharField(max_length=1,blank=True,null=True)
    semester=models.IntegerField(blank=True, null=True)
    dob=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    student_phone_no = models.CharField(max_length=10,null=True, blank=True)
    student_email_id=models.EmailField(blank=True,null=True)
    scheme=models.CharField(max_length=20,blank=True,null=True,default='None')
    yob=models.DateField(null=True, blank=True)
    yop=models.DateField(null=True, blank=True)


    L_hno=models.CharField(max_length=30)
    L_street=models.CharField(max_length=50)
    L_city=models.CharField(max_length=30)
    L_district=models.CharField(max_length=30)
    L_state=models.CharField(max_length=30)
    L_pincode=models.IntegerField(null=True, blank=True)

    P_hno=models.CharField(max_length=30)
    P_street=models.CharField(max_length=50)
    P_city=models.CharField(max_length=30)
    P_district=models.CharField(max_length=30)
    P_state=models.CharField(max_length=30)
    P_pincode=models.IntegerField(null=True, blank=True)

    residential_details=models.CharField(max_length=30,null=True, blank=True)
    nationality=models.CharField(max_length=30)
    aadhar_number=models.CharField(max_length=12,null=True, blank=True)
    category=models.CharField(max_length=15,null=True, blank=True)
    reservation_category=models.CharField(max_length=30,null=True, blank=True)
    bloodgroup=models.CharField(max_length=5,null=True, blank=True)
    ph_status=models.BooleanField(default=False,null=True, blank=True)
    hobbies=models.TextField(null=True,blank=True)
    scholarship=models.CharField(max_length=30,null=True,blank=True)
    transport_mode=models.CharField(max_length=30,null=True, blank=True)
    mother_tongue=models.CharField(max_length=30,null=True, blank=True)
    height=models.IntegerField(null=True,blank=True)
    weight=models.IntegerField(null=True,blank=True)
    illness=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return self.student_id

# class Student_table(models.Model):
#     student_id=models.CharField(max_length=10)
#     student_fullname=models.CharField(max_length=50)
#     branch1=models.CharField(max_length=6)
#     semester=models.IntegerField()
#     section=models.CharField(max_length=1)
#     gender=models.CharField(max_length=10)
#     student_email_id=models.EmailField()



class Parents_details(models.Model):#student
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
    parent_email=models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):
        return self.student_id
    
class Education_details(models.Model): #student
    student_id=models.CharField(max_length=10)
    qualification=models.CharField(max_length=20,null=True, blank=True)
    course=models.CharField(max_length=10, blank=True,null=True)
    institute_name=models.CharField(max_length=50,null=True, blank=True)
    institute_location=models.CharField(max_length=30,null=True, blank=True)
    YOP=models.DateField(null=True, blank=True)
    board=models.CharField(max_length=20,null=True, blank=True)
    percentage=models.IntegerField(null=True, blank=True)
    gpa=models.FloatField(null=True, blank=True)
    medium=models.CharField(max_length=10,null=True, blank=True)
    def __str__(self):
        return self.student_id

class Competitive_exam(models.Model): #student
    student_id=models.CharField(max_length=10)
    test_name=models.CharField(max_length=30,blank=True,null=True)
    rank_obtained=models.IntegerField(blank=True,null=True)
    score_obtained=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.student_id

class Profile(models.Model): #student
    student_id=models.CharField(max_length=10)
    profile_name=models.CharField(max_length=30,blank=True,null=True)
    profile_url=models.URLField(max_length=200,blank=True)
    def __str__(self):
        return self.student_id

class Achievements(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    achieve_name=models.CharField(max_length=50,blank=True, null=True)
    achieve_score=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.student_id

class Skills(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    skill_name=models.CharField(max_length=50,null=True,blank=True)
    test_score=models.IntegerField(null=True,blank=True)
    project_name=models.CharField(max_length=50,null=True,blank=True)
    project_type=models.CharField(max_length=50,null=True,blank=True)
    project_score=models.IntegerField(null=True,blank=True)
    certification_status=models.BooleanField(default=False,null=True,blank=True)
    updated_date=models.DateField(null=True,blank=True)
    faculty_id=models.IntegerField(null=True,blank=True)
    skill_status=models.CharField(max_length=30,null=True,blank=True)
    overall_score=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.student_id


class Certifications(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    certificate_name=models.CharField(max_length=50, blank=True,null=True)
    certificate_score=models.IntegerField(blank=True,null=True)
    certification_date=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.student_id


class Internships(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    tech_name=models.CharField(max_length=50,null=True,blank=True)
    internship_name=models.CharField(max_length=50,null=True,blank=True)
    internship_mode=models.CharField(max_length=10,null=True,blank=True)
    internship_duration=models.IntegerField(null=True,blank=True)
    date_of_completion=models.DateField(blank=True,null=True)
    stipend=models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.student_id

class Extra_Curriculars(models.Model):#nocondition
    student_id=models.CharField(max_length=10)
    activity=models.TextField(null=True,blank=True)
    role=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.student_id

class Attendance_details(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    attendance_sem=models.IntegerField(null=True,blank=True)
    month=models.CharField(max_length=10,null=True,blank=True)
    phase=models.IntegerField(null=True,blank=True)
    attendance_percentage=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.student_id

class Semwise_grades(models.Model): #student
    student_id=models.CharField(max_length=10)
    grades_sem=models.IntegerField(null=True,blank=True)
    sgpa=models.IntegerField(null=True,blank=True)
    cgpa=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.student_id

class Semester_marks(models.Model): #student
    student_id=models.CharField(max_length=10)
    subject_name=models.CharField(max_length=50,null=True,blank=True)
    subject_type=models.CharField(max_length=20,null=True,blank=True)
    first_sessional=models.IntegerField(null=True,blank=True)
    second_sessional=models.IntegerField(null=True,blank=True)
    marks_sem=models.IntegerField(null=True,blank=True)
    grade_obtained=models.CharField(max_length=2,null=True,blank=True)
    def __str__(self):
        return self.student_id


class Backlogs(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    subject_name=models.CharField(max_length=30,blank=True,null=True)
    backlog_sem=models.IntegerField(blank=True,null=True)
    sem_cleared=models.IntegerField(blank=True,null=True)
    ayoc=models.DateField(blank=True,null=True)
    def __str__(self):
        return self.student_id

class Placements(models.Model):#mentor
    student_id=models.CharField(max_length=10)
    company=models.CharField(max_length=50,blank=True,null=True)
    date_placed=models.DateField(blank=True,null=True)
    package=models.IntegerField(blank=True,null=True)
    drive_mode=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.student_id

class Remarks(models.Model):#no condition
    student_id=models.CharField(max_length=10)
    remarks_date=models.DateField(null=True,blank=True)
    student_opinions=models.TextField(null=True,blank=True)
    mentor_remarks=models.TextField(null=True,blank=True)
    remarks_sem=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.student_id