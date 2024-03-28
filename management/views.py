from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.views.static import serve
from django.db.models import Count,Q,Sum
from django.contrib.auth.models import Group,User
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from mentor import models as MMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from .models import Skill as Skill
import pandas as pd
from django.contrib.auth.decorators import permission_required
from student.models import students_skills as student_skills
import math
# from student.models import *
# from teacher.models import *

roman = {
        1:'I',
        2:'II',
        3:'III',
        4:'IV',
        5:'V',
        6:'VI',
        7:'VII',
        8:'VIII'
}

numbers = {
        'I':1,
        'II':2,
        'III':3,
        'IV':4,
        'V':5,
        'VI':6,
        'VII':7,
        'VIII':8
}


def admin_superuser_required(view_func):
    """
    Decorator for views that checks if the user is logged in, is an admin, and is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser and u.is_staff,
        login_url='/login/'  # Redirect URL if the user doesn't meet the requirements
    )
    return actual_decorator(view_func)

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    else:
        year_filter = request.GET.get('year','')
        dept_filter = request.GET.get('department','')
        domain_filter = request.GET.get('domain','')
        students = SMODEL.Student.objects.all()
        if year_filter:
            sem_filter = 2*int(year_filter)-1 #calculating the first sem of particular yr
            students = students.filter(Q(semester=sem_filter)|Q(semester=sem_filter+1))
        if dept_filter:
            students = students.filter(department=dept_filter)
        if domain_filter:
            students = students.filter(
                students_skills__skill_status="Evaluated",
                students_skills__skill_name__domain=domain_filter,
            ).annotate(
                total_score=Sum('students_skills__overall_score')
            )
            student_top = students.order_by('-total_score')[:10]
        else:
            student_top = students.order_by('-profile_score')[:10]
        top=[]
        for index, row in enumerate(student_top, start=1):
            top.append({
                'roll':row.user.username,
                'rank':index,
                'name': row.name,
                'yb': roman[math.ceil(row.semester/2)]+' '+row.branch,
                'score': row.total_score if domain_filter else row.profile_score
            })
        domains = Skill.objects.values_list('domain',flat=True).distinct()
        return render(request,'management/index.html',{'top':top, 'domains':domains,'year_filter':year_filter, 'dept_filter':dept_filter, 'domain_filter':domain_filter})  


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_mentor(user):
    return user.groups.filter(name='MENTOR').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    elif is_mentor(request.user):
        accountapproval=MMODEL.mentor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mentor/mentor-dashboard')
        else:
            return render(request,'mentor/mentor_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_dashboard_view(request):
    if request.method=="GET":
        sector = request.GET.get('sector','')
        domain = request.GET.get('domain', '')
        level = request.GET.get('level','')
        skills=models.Skill.objects.all()   
        if sector:
            skills=skills.filter(sector=sector)
        if domain:
            skills=skills.filter(domain=domain)
        if level:
            skills=skills.filter(level=level)
        list=[]
        for i in skills:
            list.append(i.skill_name)         
        return render(request,'management/dashboard.html',{'list':list,'level':level,'domain':domain,'sector':sector}) 
    return render(request,'management/dashboard.html')
    # return render(request,'management/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
@admin_superuser_required
def examiner(request):
    # mentors = MMODEL.mentor.objects.all() #.values('emp_id','name','department','mobile','email','status','mentor_image')
    #mentor_pending =  MMODEL.mentor.objects.filter(status=False).values('emp_id','name','department','mobile','email','mentor_image')
    #mentor_approve = MMODEL.mentor.objects.filter(status=True).values('emp_id','name','department','mentor_image').annotate(mentee_count=Count('student')).order_by('mentee_count','name')
    examiners=TMODEL.Examiner.objects.all()
    examiner_pending = TMODEL.Examiner.objects.filter(status=False).values('emp_id','name', 'department', 'examiner_image')
    examiner_approve = TMODEL.Examiner.objects.filter(status=True).values('emp_id','name', 'department', 'examiner_image')
    return render(request,'management/examiner.html',{'examiner_pending':examiner_pending,'examiner_approve':examiner_approve})

# @login_required(login_url='adminlogin')
# @admin_superuser_required
# def skill(request):
#     # mentors = MMODEL.mentor.objects.all() #.values('emp_id','name','department','mobile','email','status','mentor_image')
#     #mentor_pending =  MMODEL.mentor.objects.filter(status=False).values('emp_id','name','department','mobile','email','mentor_image')
#     #mentor_approve = MMODEL.mentor.objects.filter(status=True).values('emp_id','name','department','mentor_image').annotate(mentee_count=Count('student')).order_by('mentee_count','name')
#     skills=Skill.objects.all()
#     skill_pending = Skill.objects.filter(status=False).values('emp_id','name', 'department', 'examiner_image')
#     skill_approve = Skill.objects.filter(status=True).values('emp_id','name', 'department', 'examiner_image')
#     return render(request,'management/skill.html',{'skill_pending':skill_pending,'skill_approve':skill_approve})



@login_required(login_url='adminlogin')
@admin_superuser_required
def examiner_details(request,empid):
    examiner = TMODEL.Examiner.objects.get(emp_id=empid)
    details = {
        'emp_id':examiner.emp_id,
        'name':examiner.name,
        'department':examiner.department,
        'mobile':examiner.mobile,
        'email':examiner.email,
        'examiner_image':examiner.examiner_image,
        'is_active' : examiner.status
    }
    return render(request,'management/examiner_details.html',{'details':details})


@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_teacher_view(request):
    # mentors = MMODEL.mentor.objects.all() #.values('emp_id','name','department','mobile','email','status','mentor_image')
    mentor_pending =  MMODEL.mentor.objects.filter(status=False).values('emp_id','name','department','mobile','email','mentor_image')
    mentor_approve = MMODEL.mentor.objects.filter(status=True).values('emp_id','name','department','mentor_image').annotate(mentee_count=Count('student')).order_by('mentee_count','name')
    return render(request,'management/faculty.html',{'mentor_pending':mentor_pending,'mentor_approve':mentor_approve})

@login_required(login_url='adminlogin')
@admin_superuser_required
def mentor_assign(request,empid):
    mentor = MMODEL.mentor.objects.get(emp_id=empid)
    mentees = SMODEL.Student.objects.filter(mentor=mentor)

    details = {
        'emp_id':mentor.emp_id,
        'name':mentor.name,
        'department':mentor.department,
        'mobile':mentor.mobile,
        'email':mentor.email,
        'mentor_image':mentor.mentor_image,
        'is_active' : mentor.is_active
    }

    

    students = SMODEL.Student.objects.filter(department=mentor.department, mentor=None)
    classes = []
    for i in students.values('semester','branch','section').distinct():
        classes.append(roman[i['semester']]+' '+i['branch']+' '+i['section'])

    if request.method=='GET':
        classname = request.GET.get('class','')
        gender = request.GET.get('gender','')

        if gender:
            students = students.filter(gender=gender)
        if classname:
            semester, branch, section = classname.split(' ')
            semester = numbers[semester]
            students = students.filter(semester=semester,branch=branch,section=section)
        return render(request,'management/assign.html',{'details':details, 'students':students, 'classes':classes, 'class_filter':classname, 'gender_filter':gender, 'mentees':mentees})
    if request.method == 'POST':
        rolls = request.POST.getlist('roll')
        #Clear previous mentees
        for mentee in mentees:
            mentee.mentor = None
            mentee.save()
        for roll in rolls:
            try:
                user = User.objects.get(username=roll)
                student = SMODEL.Student.objects.get(user=user)
                student.mentor = mentor
                student.save()
            except User.DoesNotExist:
                return render(request,'management/assign.html',{'details':details, 'students':students, 'classes':classes})
            except SMODEL.Student.DoesNotExist:
                return render(request,'management/assign.html',{'details':details, 'students':students, 'classes':classes})
            
        return redirect(reverse('mentor-details',args=[empid]))

    return render(request,'management/assign.html',{'details':details, 'students':students, 'classes':classes})

@login_required(login_url='adminlogin')
@admin_superuser_required
def mentor_details(request,empid):
    mentor = MMODEL.mentor.objects.get(emp_id=empid)
    details = {
        'emp_id':mentor.emp_id,
        'name':mentor.name,
        'department':mentor.department,
        'mobile':mentor.mobile,
        'email':mentor.email,
        'mentor_image':mentor.mentor_image,
        'is_active' : mentor.is_active
    }

    classname = 'All'
    gender = 'All'
    mentees = SMODEL.Student.objects.filter(mentor=mentor)
    if mentees.values('semester','branch','section').distinct().count() == 1:
        classname = roman[mentees[0].semester]+' '+mentees[0].branch+' '+mentees[0].section
    if mentees.values('gender').distinct().count() == 1:
        gender = mentees[0].gender

    return render(request,'management/mentor_details.html',{'details':details, 'class':classname, 'gender':gender, 'mentees':mentees})

@login_required(login_url='adminlogin')
@admin_superuser_required
def update_status(request,empid):
    # examiner_obj=TMODEL.Examiner.objects.get(emp_id=empid)
    # examiner_obj.is_active=False
    # examiner_obj.save()
    examiner=TMODEL.Examiner.objects.get(emp_id=empid)
    user=User.objects.get(id=examiner.user_id)
    user.delete()
    examiner.delete()
    return HttpResponseRedirect('/examiner')

@login_required(login_url='adminlogin')
@admin_superuser_required
def update_is_active(request,empid):
    mentor_obj=MMODEL.mentor.objects.get(emp_id=empid)
    mentor_obj.is_active=False
    mentor_obj.save()

    mentees = SMODEL.Student.objects.filter(mentor=mentor_obj)
    for mentee in mentees:
        mentee.mentor = None
        mentee.save()
    
    return redirect(reverse('mentor-details',args=[empid]))

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'management/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@admin_superuser_required
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'management/update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@admin_superuser_required
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'management/admin_view_pending_teacher.html',{'teachers':teachers})
    # return render(request,'management/faculty.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
def approve_mentor_view(request,pk):
    mentor=MMODEL.mentor.objects.get(emp_id=pk)
    mentor.status=True
    mentor.save()
    return HttpResponseRedirect('/admin-teacher')

@login_required(login_url='adminlogin')
def approve_examiner(request,pk):
    examiner=TMODEL.Examiner.objects.get(emp_id=pk)
    examiner.status=True
    examiner.save()
    return HttpResponseRedirect('/examiner')

@login_required(login_url='adminlogin')
def accept_skill(request,name):
    skill=Skill.objects.get(skill_name=name)
    skill.status=True
    skill.save()
    return HttpResponseRedirect('/admin-skill')

@login_required(login_url='adminlogin')
def reject_skill(request,name):
    skill=Skill.objects.get(skill_name=name)
    skill.delete()
    return HttpResponseRedirect('/admin-skill')

@login_required(login_url='adminlogin')
def reject_mentor_view(request,pk):
    mentor=MMODEL.mentor.objects.get(emp_id=pk)
    user=User.objects.get(id=mentor.user_id)
    user.delete()
    mentor.delete()
    return HttpResponseRedirect('/admin-teacher')

@login_required(login_url='adminlogin')
def reject_examiner(request,pk):
    examiner=TMODEL.Examiner.objects.get(emp_id=pk)
    user=User.objects.get(id=examiner.user_id)
    user.delete()
    examiner.delete()
    return HttpResponseRedirect('/examiner')

@login_required(login_url='adminlogin')
@admin_superuser_required
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'management/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
@admin_superuser_required
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'management/admin_view_teacher_salary.html',{'teachers':teachers})

from django.db import transaction
from django.db.utils import IntegrityError

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_student_view(request):
    if request.method == "POST":
        DEFAULT_PASSWORD = "GPREC123"
        uploaded_file = request.FILES.get('file')
        
        if uploaded_file is not None and uploaded_file.name.endswith(('.xls', '.xlsx')):
            excel_data = pd.read_excel(uploaded_file)
            
            with transaction.atomic():
                try:
                    for index, row in excel_data.iterrows():
                        username = row.iloc[0]
                        name = row.iloc[1]
                        branch = row.iloc[2]
                        department = row.iloc[3]
                        semester = row.iloc[4]
                        section = row.iloc[5]
                        gender = row.iloc[6]
                        email = row.iloc[7]
                        
                        # Perform validation
                        validation = is_valid(name, branch, department, semester, section, gender, email)
                        if validation != None:
                            raise ValueError(f"Validation failed due to {validation}")
                        
                        # Create User and Student objects
                        user = User(username=username, email=email, password=DEFAULT_PASSWORD)
                        user.save()
                        student = SMODEL.Student(user=user, name=name, branch=branch, department=department, semester=semester, section=section, gender=gender )
                        student.save()
                        
                        # Add user to the 'STUDENT' group
                        student_group = Group.objects.get(name='STUDENT')
                        student_group.user_set.add(user)
                except (ValueError,IntegrityError,TypeError) as e:
                    transaction.set_rollback(True)
                    error_message = str(e)+" at row "+str(index+2)
                    print(f"Error: {error_message}")
                    return render(request, 'management/create_students_accounts.html', {'error': error_message})
                
                return render(request, 'management/create_students_accounts.html',{'success':'Accounts created successfully'})
        else:
            return render(request, 'management/create_students_accounts.html', {'error': "Invalid file format"})
        
    return render(request, 'management/create_students_accounts.html')

import re
def is_valid(name, branch, department, semester, section, gender, email):
    # Validation for name: Should only contain letters and spaces
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return "Invalid name"
    # Validation for branch: Should be one amongst 
    valid_branches = ['CSE', 'ECE', 'EEE', 'CIV', 'MEC', 'CST', 'CSB', 'CSM', 'CSD']
    if branch not in valid_branches:
        return "Invalid branch"
    # Validation for department: Should be one amongst 
    valid_departments = ['ECS', 'CSE', 'ECE', 'EEE', 'CIV', 'MEC']
    if department not in valid_departments:
        return "Invalid department"
    # Validation for semester: Should be in the range 1-8 (integers)
    if not isinstance(semester, int) or semester < 1 or semester > 8:
        return "Invalid semester"
    # Validation for section: Should be a single uppercase letter
    if not re.match(r'^[A-Z]$', section):
        return "Invalid section"
    # Validation for gender: Should be amongst
    valid_genders = ['Male', 'Female', 'Other']
    if gender not in valid_genders:
        return "Invalid gender"
    # Validation for email: Using a simple regex pattern for email validation
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Invalid email"
    
    return None

@login_required(login_url='adminlogin')
@admin_superuser_required
def download_sample(request):
    return serve(request, 'sample.xlsx', document_root=settings.STATIC_DIR)

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'management/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
@admin_superuser_required
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'management/update_student.html',context=mydict)


@login_required(login_url='adminlogin')
@admin_superuser_required
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-skill')


@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_course_view(request):
    
    return render(request,'management/admin_course.html')

@login_required(login_url='adminlogin')
@admin_superuser_required
def get_domains(request):
    sector = request.GET.get('sector','')
    if sector:
        domains = models.Skill.objects.filter(sector=sector).values_list('domain',flat=True).distinct()
    else:
        domains = models.Skill.objects.values_list('domain',flat=True).distinct()
    return JsonResponse(list(domains), safe=False)

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_skill_view(request):

    domain_filter = request.GET.get('domain_filter', '')
    sector_filter = request.GET.get('sector_filter', '')
    level_filter = request.GET.get('level_filter', '')  

    skill_pending = Skill.objects.filter(status=False)
    skill_approve = Skill.objects.filter(status=True)
    domains = models.Skill.objects.values_list('domain',flat=True).distinct()

    if domain_filter:
        skill_pending = skill_pending.filter(domain=domain_filter)
        skill_approve = skill_approve.filter(domain=domain_filter)

    if sector_filter:
        skill_pending = skill_pending.filter(sector=sector_filter)
        skill_approve = skill_approve.filter(sector=sector_filter)
    if level_filter:
        skill_pending = skill_pending.filter(level=level_filter)
        skill_approve = skill_approve.filter(level=level_filter)
    
    
    # return render(request,'management/examiner.html',{'examiner_pending':examiner_pending,'examiner_approve':examiner_approve})

    context = {
        'domain_filter':domain_filter,
        'sector_filter':sector_filter,
        'level_filter':level_filter,
        'domains':list(domains),
        'skill_pending':skill_pending,
        'skill_approve':skill_approve
    }
    return render(request,'management/skills.html',context)

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_add_skill(request):
    if request.method=='POST':
        skill_name = request.POST.get('skill_name')
        sector = request.POST.get('sector')
        domain = request.POST.get('domain')
        level = request.POST.get('level')
        parameters = request.POST.get('parameters')

        skill = models.Skill(skill_name=skill_name,sector=sector,domain=domain,level=level,parameters=parameters)
        skill.save()

    return redirect(admin_skill_view)
@admin_superuser_required
def admin_edit_skill(request,skill_name):
    if request.method=='POST':
        new_skill_name = request.POST.get('skill_name')
        sector = request.POST.get('sector')
        domain = request.POST.get('domain')
        level = request.POST.get('level')
        parameters = request.POST.get('parameters')

        models.Skill.objects.filter(skill_name=skill_name).update(skill_name = new_skill_name,sector = sector,domain = domain,level = level)
    return redirect(admin_skill_view)

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'management/admin_add_course.html',{'courseForm':courseForm})

@admin_superuser_required
@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'management/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
@admin_superuser_required
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_question_view(request):
    return render(request,'management/admin_question.html')

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'management/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'management/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
@admin_superuser_required
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'management/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
@admin_superuser_required
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'management/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'management/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'management/admin_check_marks.html',{'results':results})
    
def aboutus_view(request):
    return render(request,'management/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'management/contactussuccess.html')
    return render(request, 'management/contactus.html', {'form':sub})

def get_dashboard_data(request):
    selected_values= request.GET.getlist('selectedValues[]')
    dict={}
    for i in selected_values:
        students=student_skills.objects.filter(skill_name=i)
        students = list(students.select_related('student').values('student__branch'))  
        branch_counts = {item['student__branch']: students.count(item) for item in students}
        dict[i]=branch_counts
        # print(grouped_student_skills)
    # print(dict)
    return JsonResponse(dict)

def leaderboard(request):
    year_filter = request.GET.get('year','')
    dept_filter = request.GET.get('department','')
    domain_filter = request.GET.get('domain','')
    students = SMODEL.Student.objects.all()
    if year_filter:
        sem_filter = 2*int(year_filter)-1 #calculating the first sem of particular yr
        students = students.filter(Q(semester=sem_filter)|Q(semester=sem_filter+1))
    if dept_filter:
        students = students.filter(department=dept_filter)
    if domain_filter:
        students = students.filter(
            students_skills__skill_status="Evaluated",
            students_skills__skill_name__domain=domain_filter,
        ).annotate(
            total_score=Sum('students_skills__overall_score')
        )
        student_top = students.order_by('-total_score')[:10]
    else:
        student_top = students.order_by('-profile_score')[:10]
    top=[]
    for index, row in enumerate(student_top, start=1):
        top.append({
            'roll':row.user.username,
            'rank':index,
            'name': row.name,
            'yb': roman[math.ceil(row.semester/2)]+' '+row.branch,
            'score': row.total_score if domain_filter else row.profile_score
        })
    domains = Skill.objects.values_list('domain',flat=True).distinct()
    return render(request,'leaderboard.html',{'top':top, 'domains':domains,'year_filter':year_filter, 'dept_filter':dept_filter, 'domain_filter':domain_filter})

# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
import string

def email_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        reset = request.POST.get('reset','')
        if reset:
            try:
                userExists = User.objects.filter(email=email).exists()
                if not userExists:
                    return JsonResponse({'status':'nomail'})
            except:
                return JsonResponse({'status':'fail'})
        if email:
            try:
                otp = ''.join(random.choices(string.digits, k=6))  # Generate 6-digit OTP
                send_mail(
                    'OTP for Email Verification',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,  # Change this to your sender email
                    [email],
                    fail_silently=False,
                )
                request.session['otp'] = otp
                request.session['email'] = email
                # return redirect('verify-otp')
                return JsonResponse({'status':'sent'})
            except:
                return JsonResponse({'status':'fail'})
    return render(request, 'mentor/mentorsignup.html')
    
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('otp'):
            # OTP matched, do further actions like marking email as verified
            del request.session['otp']
            email = request.session.get('email')
            del request.session['email']
            return JsonResponse({'verified':True,'email': email})
        else:
            # Incorrect OTP
            return JsonResponse({'verified':False})
    return render(request, 'mentor/mentorsignup.html')

