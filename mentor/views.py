from django.shortcuts import render
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from management import models as QMODEL
from student import models as SMODEL
from django.contrib.auth.models import User
from django.contrib import messages

from .models import *
from management.models import *

from student.models import * 
# Create your views here.

def is_mentor(user):
    return user.groups.filter(name="MENTOR").exists()

def is_approved(user):
    #return user.groups.filter(name="MENTOR").status
    # mentor_group = Group.objects.get(name="MENTOR")
    # mentor_profile = user.mentor_profile  # Assuming Mentor model has a OneToOneField to User
    # return mentor_profile.status if mentor_profile else False
    try:
        mentor_profile = mentor.objects.get(user=user)
        return mentor_profile.status
    except mentor.DoesNotExist:
        return False

def mentorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentor/mentorclick.html')

def mentor_signup_view(request):
    if request.method=='POST':
        username=request.POST['username']
        EmployeeID=request.POST['username']
        full_name=request.POST['full_name']
        department=request.POST['department']
        mobile=request.POST['mobile']
        email=request.POST['email']
        password=request.POST['password']
        mentor_image = request.FILES.get('mentor_image')
        
        userExists = User.objects.filter(username=username).exists()
        emailExists = User.objects.filter(email=email).exists()
        if(userExists or emailExists):
            if userExists:
                messages.info(request,"Employee_id already exists !")
            if emailExists:
                messages.info(request,"Email already exists !")
            return redirect("mentorsignup")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)       
            user.save()
            mentor1=mentor(user=user,emp_id=EmployeeID,name=full_name,status=False,department=department,mobile=mobile,email=email, mentor_image=mentor_image)
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


# @login_required(login_url='mentorlogin')
@user_passes_test(is_approved)
def mentor_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'mentor/mentor_dashboard.html',context=dict)

