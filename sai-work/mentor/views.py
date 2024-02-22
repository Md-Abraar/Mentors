from django.shortcuts import render
from django.shortcuts import render,redirect,reverse,get_object_or_404
# from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import Q
from .models import *
from quiz.models import *

from student.models import * 
# Create your views here.
def mentorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentor/mentorclick.html')


def mentor_signup_view(request):
    if request.method=='POST':
        username=request.POST['username']
        EmployeeID=request.POST['EmployeeID']
        full_name=request.POST['full_name']
        department=request.POST['department']
        mobile=request.POST['mobile']
        email=request.POST['email']
        password=request.POST['password']

        if(User.objects.filter(email=email).exists()):
            messages.info(request,"email already exists !")
            return redirect("mentorsignup")
        elif(User.objects.filter(username=username).exists()):
            messages.info(request,"user already exists !")
            return redirect("mentorsignup")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.mobile = mobile
            user.EmployeeID = EmployeeID
            user.name = full_name
            user.department = department
            user.status=False          
            user.save()
            mentor1=mentor(user=user,emp_id=EmployeeID,name=full_name,status=False,department=department,mobile=mobile,email=email)
            mentor1.save()
            mentor_group = Group.objects.get(name='mentor')
            mentor_group.user_set.add(user)
            return redirect('mentorlogin')
    return render(request,'mentor/mentorsignup.html')



# @login_required(login_url='teacherlogin')
def students_list(request):
    user_instance = User.objects.get(username=request.user)
    teacher_instance = mentor.objects.get(user=user_instance)
    students_data = Student.objects.filter(TD=teacher_instance).prefetch_related('user')
    return render(request, 'mentor/students_list.html', {'details': students_data})


@login_required(login_url='mentorlogin')
def mentor_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'mentor/mentor_dashboard.html',context=dict)



def students_skill_applications(request):
    if request.method=='POST':
        pass
    mentor_instance = get_object_or_404(mentor, user=request.user)
    students_data = Student.objects.filter(TD=mentor_instance)
    student_applications = students_skills.objects.filter(student__in=students_data)
    examiner=teacher_skills.objects.filter(skill_status=True)
    return render(request, 'mentor/students_skill_applications.html', {'student_applications': student_applications,'examiners':examiner})



def student_application_reject_view(request,pk):
    student_application = students_skills.objects.get(id=pk)
    student_application.skill_status="rejected"
    student_application.save()
    return HttpResponseRedirect('/mentor/students_skill_applications')


from datetime import date

today = date.today()

def student_application_approve_view(request,pk):
    application_id=pk
    examiner=request.POST['examiner_id']
    sapp=students_skills.objects.get(id=application_id)
    eapp=Teacher.objects.get(id=examiner)
    teacher=Teacher.objects.get(id=eapp.id) 
    new_app=student_skill_exam_applications(student=sapp.student,branch=sapp.student.branch,section=sapp.student.section,mentor_identity_number=sapp.student.TD.id,requested_date=today,application_status="pending",skill_name=sapp.skill_name,assessed_by=eapp.user.id,sem=sapp.student.sem)
    new_app.save()
    sapp.skill_status="under evaluation"
    sapp.save()
    messages.info(request,f"{sapp.student.name.upper()} student application sent to {teacher.name.upper()} successfully")
    return HttpResponseRedirect('/mentor/students_skill_applications')


def students_scores_view(request):
    mentor_instance = get_object_or_404(mentor, user=request.user)
    students_data = Student.objects.filter(TD=mentor_instance)


    # Assuming students_data is a list of student IDs or some other filter criteria
    # Replace students_data with your actual filter criteria

    # Filter student applications based on skill status
    student_applications = students_skills.objects.filter(
        Q(student__in=students_data) & (Q(skill_status="test_evaluated") | Q(skill_status="evaluated"))
    )    
    return render(request,'mentor/students_scores.html',{'data':student_applications})

def update_student_skill_view(request,id):
    student_skill = students_skills.objects.get(id=id)
    # new_project_score = request.POST.get(f'{id}_pm')
    student_skill.project_name=  request.POST['project_name']
    student_skill.project_type =request.POST['project_type']
    student_skill.updated_date=  request.POST['update_date']
    student_skill.project_score=request.POST['marks']
    student_skill.skill_status="evaluated"
    # student_skill.  project_score = new_project_score
    student_skill.save()
    return HttpResponseRedirect('/mentor/students_scores')
