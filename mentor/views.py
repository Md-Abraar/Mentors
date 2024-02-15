from django.shortcuts import render
from django.shortcuts import render,redirect,reverse,get_object_or_404
# from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from management import models as QMODEL
from student import models as SMODEL
from management import forms as QFORM
from django.contrib.auth.models import User,auth
from django.contrib import messages

from .models import *
from management.models import *

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
            mentor_group = Group.objects.get(name='MENTOR')
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

