from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
import cv2
import pyaudio
import json
import audioop
from django.http import StreamingHttpResponse
from .utils import VideoCamera
from quiz.models import *
from .models import *
from django.contrib import messages

# Initialize audio input stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
# @user_passes_test(is_student)
def student_exam_view(request):
    current_student = Student.objects.get(user=request.user)

    exam_ids = student_skill_exam_applications.objects.filter(student=current_student).values_list('exam_id', flat=True)

    courses = QMODEL.Course.objects.filter(id__in=exam_ids)

    return render(request,'student/student_exam.html',{'courses':courses})




@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = get_object_or_404(QMODEL.Course, pk=pk)
    student = request.user.student  # Assuming Student is related to the User model

    try:
        result = QMODEL.Result.objects.get(student=student, exam=course)
        msg="Already Submitted"
        txt="You have already submitted the test. Your input has been recorded."
        return render(request, 'student/success.html',{'message':msg,'text':txt})
    except QMODEL.Result.DoesNotExist:
        total_questions = QMODEL.Question.objects.filter(course=course).count()
        total_marks = QMODEL.Question.objects.filter(course=course).aggregate(Sum('marks'))['marks__sum']

        return render(request, 'student/take_exam.html', {
            'course': course,
            'total_questions': total_questions,
            'total_marks': total_marks
        })
        




def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        # student_application=student_skill_exam_applications.objects.get(student=request.user,)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('success')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})


def success_page(request):
    msg="Success"
    txt="Test submitted successfully. Your input has been recorded."
    return render(request,'student/success.html',{'message':msg,'text':txt})


def skill_application(request):
    if request.method=='POST':
        skill_name=request.POST['skill_applying']
        certification_status = request.POST.get('certification_status', False)  =="on"
        project_select = request.POST.get('project_select', '')
        student=Student.objects.get(user=request.user)
        obj1 = students_skills(student=student,skill_name=skill_name, 
                                              certification_status=certification_status, 
                                              project_type=project_select)
        obj1.save()
        messages.success(request, 'Skill application saved successfully.')

    student_instance = get_object_or_404(Student, user=request.user)
        
    student_applications = students_skills.objects.filter(student=student_instance)

    return render(request,'student/skill_application_form.html',{'student_applications':student_applications})


def delete_application_view(request,pk):
    application=students_skills.objects.get(id=pk)
    # user=User.objects.get(id=student.user_id)
    # user.delete()
    application.delete()
    return HttpResponseRedirect('/student/skill_application')