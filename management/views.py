from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from mentor import models as MMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
import pandas as pd
from django.contrib.auth.decorators import permission_required

# from student.models import *
# from teacher.models import *

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
    return render(request,'management/index.html')


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
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'management/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_teacher_view(request):
    # dict={
    # 'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    # 'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    # 'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    # }
    # return render(request,'management/admin_teacher.html',context=dict)
    mentors = MMODEL.mentor.objects.all() #.values('emp_id','name','department','mobile','email','status','mentor_image')
    mentor_pending =  MMODEL.mentor.objects.filter(status=False)
    mentor_approve = MMODEL.mentor.objects.filter(status=True) #.values('emp_id','name','department','mobile','email','status','mentor_image')
    
    return render(request,'management/faculty.html',{'mentor_pending':mentor_pending,'mentor_approve':mentor_approve})

def assignment(request):
    if(request.method=='POST'):
        students = request.POST.getlist('student_assignment')
    return render(request,'management/faculty.html')
    

def faculty_details(request):
    # if request.method=='POST':
    #     faculty_id = request.POST.get('faculty_id')
    #     faculty_name = request.POST.get('faculty_name')
    #     faculty_designation = request.POST.get('faculty_designation')
    #     faculty_email = request.POST.get('faculty_email')
    #     faculty_branch = request.POST.get('faculty_branch')
    #     faculty_phone = request.POST.get('facult_phone')
    #     skillset = request.POST.get('skillset')
    #     skillset = skillset.split(",")

    #     faculty_record = Faculty(faculty_id = faculty_id, faculty_name = faculty_name, faculty_designation = faculty_designation,
    #                   faculty_branch = faculty_branch, faculty_email = faculty_email, faculty_phone = faculty_phone)
    #     faculty_record.save()

    return render(request, 'management/faculty_details.html')

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
    mentor=MMODEL.mentor.objects.get(id=pk)
    mentor.status=True
    mentor.save()
    return HttpResponseRedirect('/admin-teacher')

@login_required(login_url='adminlogin')
def reject_mentor_view(request,pk):
    mentor=MMODEL.mentor.objects.get(id=pk)
    user=User.objects.get(id=mentor.user_id)
    user.delete()
    mentor.delete()
    return HttpResponseRedirect('/admin-teacher')

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


from django.contrib.auth.models import User
from django.db import transaction

# from student.models import Student
@login_required(login_url='adminlogin')
@admin_superuser_required
def admin_student_view(request):
    # dict={
    # 'total_student':SMODEL.Student.objects.all().count(),
    # }
    if request.method=="POST":
        DEFAULT_PASSWORD="GPREC"
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith(('.xls', '.xlsx')):
            excel_data = pd.read_excel(uploaded_file)
            for index, row in excel_data.iterrows():
                username=row[0]
                mail=row[1]
                user=User(username=username, email=mail, password=DEFAULT_PASSWORD)
                user.save()
                student=SMODEL.Student(user=user)
                student.save()
                student_group = Group.objects.get(name='STUDENT')
                student_group.user_set.add(user)
        render(request,'management/create_students_accounts.html')  
    return render(request,'management/create_students_accounts.html')

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

    skills = models.Skill.objects.all()
    domains = models.Skill.objects.values_list('domain',flat=True).distinct()

    if domain_filter:
        skills = skills.filter(domain=domain_filter)
    if sector_filter:
        skills = skills.filter(sector=sector_filter)
    if level_filter:
        skills = skills.filter(level=level_filter)

    context = {
        'skills':skills,
        'domain_filter':domain_filter,
        'sector_filter':sector_filter,
        'level_filter':level_filter,
        'domains':list(domains)
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

        models.Skill.objects.filter(skill_name=skill_name).update(skill_name = new_skill_name,sector = sector,domain = domain,level = level,parameters = parameters)
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
    



@admin_superuser_required
def aboutus_view(request):
    return render(request,'management/aboutus.html')

@admin_superuser_required
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

# import csv

# @login_required(login_url='adminlogin')
# def admin_create_student(request):
#     # Define a default password
#     DEFAULT_PASSWORD = 'default_password'

#     # Assuming you have a list of student data in the format of (username, email)
#     student_data = [
#         ('student9', 'student3@example.com'),
#         ('student10', 'student4@example.com'),
#         # Add more student data as needed
#     ]
#     csv_file_path = 'C:/Users/Abraar/OneDrive/Desktop/students.csv'
#     with open(csv_file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             # Create User instance
#             user = User.objects.create_user(
#                 username=row['userid'],
#                 email=row['email'],
#                 password=DEFAULT_PASSWORD
#             )
#             # Create StudentAccount instance
#             SMODEL.Studentaccount.objects.create(user=user)
        
#     return HttpResponse('aipoindi')

@login_required(login_url='adminlogin')
@admin_superuser_required
def mentor_assign(request):
    return render(request,'management/assign.html')



