from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group,User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from management import models as QMODEL
from examiner import models as TMODEL

import datetime
from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group,auth
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from management import models as QMODEL
from examiner import models as TMODEL
import cv2
import pyaudio
import json
import audioop
from django.http import StreamingHttpResponse
# from .utils import VideoCamera # type: ignore
from management.models import *
from .models import *
from django.contrib import messages
from datetime import date, datetime
from django.utils.dateparse import parse_date

#for showing signup/login button for student


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












def student_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        newpassword = request.POST.get('newpassword')
        if newpassword:
            user = User.objects.get(email=email)
            user.set_password(newpassword)
            user.save()
        return redirect('studentlogin')
    return render(request, 'management/forgot_password.html')





#----sai views---------------




# Initialize audio input stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('/student/studentlogin')



def student_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            request.session['student_details_edit'] = user.student.roll
            auth.login(request,user)
            # roll=user.student
            return HttpResponseRedirect(f'/student/student_profle/{user.student.roll}')
        else:
            messages.info(request,"user name or password does not match !")
            return redirect("studentlogin")
    return render(request,'student/studentlogin.html')




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
    courses = Course.objects.filter(id__in=exam_ids)
    
    final_obj = {}
    for course in courses:
        try:
            # Check if the student has attempted the exam
            result = Result.objects.get(student=current_student, exam=course)
            status = "Attempted"
        except Result.DoesNotExist:
            status = "None"
        
        final_obj[course] = status

    
    return render(request,'student/student_exam.html',{'courses':final_obj})

from functools import wraps








@login_required(login_url='studentlogin')
@user_passes_test(is_student)

def take_exam_view(request, pk):
    try:
        status=request.session.get('passcode_status')
        del request.session['passcode_status']
    except:
        status=None
    
    if status:
        course = get_object_or_404(QMODEL.Course, pk=pk)
        student = request.user.student  # Assuming Student is related to the User model

        total_questions = QMODEL.Question.objects.filter(course=course).count()
        total_marks = QMODEL.Question.objects.filter(course=course).aggregate(Sum('marks'))['marks__sum']

        return render(request, 'student/take_exam.html', {
                'course': course,
                'total_questions': total_questions,
                'total_marks': total_marks
            })
    else:
        return HttpResponseRedirect('/student/student-exam')

    

        




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
    student_instance = get_object_or_404(Student, user=request.user)
        
    if request.method=='POST':
        skill_name=request.POST['skill_applying']

        existing_skills = students_skills.objects.filter(student=student_instance).exclude(skill_status='rejected').values_list('skill_name', flat=True)
        if skill_name in existing_skills:
            messages.info(request,'Skill Already Exist!!!')
            return HttpResponseRedirect('/student/skill_application')
        
        certification_status = request.POST.get('certification_status', False)  =="on"
        project_select = request.POST.get('project_select', '')
        student=Student.objects.get(user=request.user)
        obj1 = students_skills(student=student,skill_name=skill_name, 
                                              certification_status=certification_status, 
                                              project_type=project_select)
        obj1.save()

    student_applications = students_skills.objects.filter(student=student_instance)
    reg_skills = Skill.objects.filter(status=True).values('skill_name')

    
    sectors = Skill.objects.filter(status=True).values('sector').distinct()
    domains = Skill.objects.filter(status=True).values('domain').distinct()

    try:
        check=request.session['request_sent']
    except: 
        check=None
    
    if check:
        statuss=request.session.get('request_sent')
        del request.session['request_sent']
        return render(request,'student/skill_application_form.html',{'student_applications':student_applications,'reg_skills':reg_skills,'sectors':sectors,'domains':domains,'status':statuss})
    else:
        statuss=False
        return render(request,'student/skill_application_form.html',{'student_applications':student_applications,'reg_skills':reg_skills,'sectors':sectors,'domains':domains,'status':statuss})


def delete_application_view(request,pk):
    application=students_skills.objects.get(id=pk)
    # user=User.objects.get(id=student.user_id)
    # user.delete()
    application.delete()
    return HttpResponseRedirect('/student/skill_application')


# from django.shortcuts import render,redirect,reverse
# from django.http import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required,user_passes_test
# from django.conf import settings

# from .models import *
# def student_profile_edit_c(request,roll):







# Create your views here.
def student_profile_edit(request):

    user1=request.session.get("student_details_edit")
    # student_d = Student.objects.get(roll=user12)
    # user1=student_d.roll
    per_det=Personal_details.objects.filter(student_id=user1)
    par_det=Parents_details.objects.filter(student_id=user1)
    edu_det=Education_details.objects.filter(student_id=user1)
    com_det=Competitive_exam.objects.filter(student_id=user1)
    prof_det=Profile.objects.filter(student_id=user1)
    ach_det=Achievements.objects.filter(student_id=user1)
    ski_det=Skills.objects.filter(student_id=user1)
    cer_det=Certifications.objects.filter(student_id=user1)
    int_det=Internships.objects.filter(student_id=user1)
    ext_det=Extra_Curriculars.objects.filter(student_id=user1)
    att_det=Attendance_details.objects.filter(student_id=user1)
    sem_wise_det=Semwise_grades.objects.filter(student_id=user1)
    marks_det=Semester_marks.objects.filter(student_id=user1)
    pla_det=Placements.objects.filter(student_id=user1)
    bac_det=Backlogs.objects.filter(student_id=user1)
    rem_det=Remarks.objects.filter(student_id=user1)
    if request.user.groups.filter(name='MENTOR').exists():
        return render(request,'mentor/student_profile_edit.html',{'per_det':per_det,'par_det':par_det,'edu_det':edu_det,'com_det':com_det,'prof_det':prof_det,'ach_det':ach_det,'ski_det':ski_det,'cer_det':cer_det,'int_det':int_det,'ext_det':ext_det,'att_det':att_det,'sem_wise_det':sem_wise_det,'marks_det':marks_det,'pla_det':pla_det,'bac_det':bac_det,'rem_det':rem_det,"user11":"mentor","st_id":user1})
    elif(request.user.groups.filter(name='STUDENT').exists()):
        return render(request,'student/student_profile_edit.html',{'per_det':per_det,'par_det':par_det,'edu_det':edu_det,'com_det':com_det,'prof_det':prof_det,'ach_det':ach_det,'ski_det':ski_det,'cer_det':cer_det,'int_det':int_det,'ext_det':ext_det,'att_det':att_det,'sem_wise_det':sem_wise_det,'marks_det':marks_det,'pla_det':pla_det,'bac_det':bac_det,'rem_det':rem_det,"user11":"student","st_id":user1})
    else:
        return render(request,'student_dashboard.html',{'per_det':per_det,'par_det':par_det,'edu_det':edu_det,'com_det':com_det,'prof_det':prof_det,'ach_det':ach_det,'ski_det':ski_det,'cer_det':cer_det,'int_det':int_det,'ext_det':ext_det,'att_det':att_det,'sem_wise_det':sem_wise_det,'marks_det':marks_det,'pla_det':pla_det,'bac_det':bac_det,'rem_det':rem_det})












from django.db.models import F



def student_profile(request,roll):
    if request.user.groups.filter(name='STUDENT').exists():
        user1=roll
        s_rec=Student.objects.get(roll=roll)
        per_det=Personal_details.objects.filter(student_id=user1)
        prof_det=Profile.objects.filter(student_id=user1)

        ski_det1 = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
        ski_det=list()
        for i in ski_det1:
            temp=dict()
            temp["skill_name"]=i.skill_name
            temp['overall_score']=i.test_score + i.project_score
            ski_det.append(temp)
            
        print(ski_det)
        ach_det=Achievements.objects.filter(student_id=user1)
        int_det=Internships.objects.filter(student_id=user1)
        cer_det=Certifications.objects.filter(student_id=user1)
        ext_det=Extra_Curriculars.objects.filter(student_id=user1)
        Profile_score = Student.objects.filter(roll=roll).values('profile_score').first()
        base_url = f"{request.scheme}://{request.META['HTTP_HOST']}"
        # base_url_without_student = base_url.replace("/student", "")

        profile_url = f"{base_url}/student_profile/{roll}"

        # print(profile_url,"LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        return render(request,'student/student_profile.html',{'per_det':per_det,'prof_det':prof_det,'ski_det':ski_det,'ach_det':ach_det,'int_det':int_det,'cer_det':cer_det,'ext_det':ext_det,'profile_url': profile_url,'Profile_score':Profile_score})
    else:
        return HttpResponseRedirect(f'/student_profile/{roll}')





def CE_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        test_name = request.POST.getlist('test_name')
        rank_obtained = request.POST.getlist('rank_obtained')
        score_obtained = request.POST.getlist('score_obtained')

        existing_records=Competitive_exam.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(test_name)):
            if test_name[i]:
                new_CE = Competitive_exam(
                            student_id=sid,
                            test_name=test_name[i] if i < len(test_name) else None,
                            rank_obtained=rank_obtained[i] if i < len(rank_obtained) else None,
                            score_obtained=score_obtained[i] if i < len(score_obtained) else None,
                        )
                new_CE.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')
    






def PF_view(request):
    if request.method == 'POST':

        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        profile_name = request.POST.getlist('profile_name')
        profile_url = request.POST.getlist('profile_url')

        existing_records=Profile.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(profile_name)):
            if profile_name[i]:
                new_CE = Profile(
                            student_id=sid,
                            profile_name=profile_name[i] if i < len(profile_name) else None,
                            profile_url=profile_url[i] if i < len(profile_url) else None,
                        )
                new_CE.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')
    



def SWG_view(request):
    if request.method == 'POST':

        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        grades_sem = request.POST.getlist('grades_sem')
        sgpa = request.POST.getlist('sgpa')
        cgpa = request.POST.getlist('cgpa')

        existing_records=Semwise_grades.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(grades_sem)):
            if grades_sem[i]:
                new_SWG = Semwise_grades(
                            student_id=sid,
                            grades_sem=grades_sem[i] if i < len(grades_sem) else None,
                            sgpa=sgpa[i] if i < len(sgpa) else None,
                            cgpa=cgpa[i] if i < len(cgpa) else None,
                        )
                new_SWG.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')
    




def SM_view(request):
    if request.method == 'POST':

        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        sname = request.POST.getlist('sname')
        sub_type = request.POST.getlist('sub_type')
        marks_sem = request.POST.getlist('marks_sem')
        first_ses = request.POST.getlist('first_ses')
        second_ses = request.POST.getlist('second_ses')
        grade = request.POST.getlist('grade')

        existing_records=Semester_marks.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(sname)):
            if sname[i]:
                new_SM = Semester_marks(
                            student_id=sid,
                            subject_name=sname[i] if i < len(sname) else None,
                            subject_type=sub_type[i] if i < len(sub_type) else None,
                            first_sessional=marks_sem[i] if i < len(marks_sem) else None,
                            second_sessional=first_ses[i] if i < len(first_ses) else None,
                            marks_sem=second_ses[i] if i < len(second_ses) else None,
                            grade_obtained=grade[i] if i < len(grade) else None,
                        )
                new_SM.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')
    


def ED_view(request):
    if request.method == 'POST':
        sid = request.POST['sid']
        s_qualification = request.POST.get('s_qualification')
        s_institute_name = request.POST.get('s_institute_name')
        s_institute_location = request.POST.get('s_institute_location')
        s_YOP = datetime.strptime(request.POST['s_YOP'],'%Y-%m-%d').date() if request.POST.get('s_YOP') else None 
        s_board = request.POST.get('s_board')
        s_percentage = float(request.POST['s_percentage']) if 's_percentage' in request.POST and request.POST['s_percentage'] else None
        s_gpa = float(request.POST['s_gpa']) if 's_gpa' in request.POST and request.POST['s_gpa'] else None

        s_medium = request.POST.get('s_medium')

        h_qualification = request.POST.get('h_qualification')
        h_course = request.POST.get('h_course')
        h_institute_name = request.POST.get('h_institute_name')
        h_institute_location = request.POST.get('h_institute_location')
        h_YOP = datetime.strptime(request.POST['h_YOP'],'%Y-%m-%d').date() if request.POST.get('h_YOP') else None
        h_board = request.POST.get('h_board')
        h_percentage = float(request.POST['h_percentage']) if 'h_percentage' in request.POST and request.POST['h_percentage'] else None
        h_gpa = float(request.POST['h_gpa']) if 'h_gpa' in request.POST and request.POST['h_gpa'] else None
        h_medium = request.POST.get('h_medium')

        existing_records=Education_details.objects.filter(student_id=sid)
        existing_records.delete()

        ED1=Education_details(student_id=sid,qualification=s_qualification,institute_name=s_institute_name,institute_location=s_institute_location,YOP=s_YOP,board=s_board,percentage=s_percentage,gpa=s_gpa,medium=s_medium)
        ED2=Education_details(student_id=sid,qualification=h_qualification,course=h_course,institute_name=h_institute_name,institute_location=h_institute_location,YOP=h_YOP,board=h_board,percentage=h_percentage,gpa=h_gpa,medium=h_medium)
        ED1.save()
        ED2.save()
        
        return HttpResponseRedirect('/student/student_profile_edit/')


def PR_view(request):
    if request.method == 'POST':
        sid = request.POST['sid']
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_phone = int(request.POST['father_phone']) if 'father_phone' in request.POST and request.POST['father_phone'].isdigit() else None
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_phone = int(request.POST['mother_phone']) if 'mother_phone' in request.POST and request.POST['mother_phone'].isdigit() else None
        guardian_name = request.POST.get('guardian_name')
        guardian_occupation = request.POST.get('guardian_occupation')
        guardian_phone = int(request.POST['guardian_phone']) if 'guardian_phone' in request.POST and request.POST['guardian_phone'].isdigit() else None
        pg_email = request.POST.get('pg_email')

        existing_records=Parents_details.objects.filter(student_id=sid)
        existing_records.delete()

        PD=Parents_details(student_id=sid,father_name=father_name,father_occupation=father_occupation,father_phone_number=father_phone,mother_name=mother_name,mother_occupation=mother_occupation,mother_phone_number=mother_phone,guardian_name=guardian_name,guardian_occupation=guardian_occupation,guardian_phone_number=guardian_phone,parent_email=pg_email)
        PD.save()

        
        return HttpResponseRedirect('/student/student_profile_edit/')
    

def PD_view(request):
    if request.method == 'POST':
        # STUDENT_TABLE
        sid = request.POST.get('sid1')

        print(sid, "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        student_fullname = request.POST.get('student_fullname')
        branch = request.POST.get('branch')
        section = request.POST.get('section')
        semester = request.POST.get('semester')
        scheme = request.POST.get('section')
        dob = datetime.strptime(request.POST.get('dob'), '%Y-%m-%d').date() if request.POST.get('dob') else None
        gender = request.POST.get('gender')
        student_phone_no = request.POST.get('student_phone_no')
        student_email_id = request.POST.get('student_email_id')

        l_hno = request.POST.get('l_hno')
        l_street = request.POST.get('l_street')
        l_city = request.POST.get('l_city')
        l_district = request.POST.get('l_district')
        l_state = request.POST.get('l_state')
        l_pincode = request.POST.get('l_pincode') if request.POST.get('l_pincode').isdigit() else None


        p_hno = request.POST.get('p_hno')
        p_street = request.POST.get('p_street')
        p_city = request.POST.get('p_city')
        p_district = request.POST.get('p_district')
        p_state = request.POST.get('p_state')
        p_pincode = request.POST.get('p_pincode') if request.POST.get('p_pincode').isdigit() else None

        residential_details = request.POST.get('residential_details')
        nationality = request.POST.get('nationality')
        aadhar_number = request.POST.get('aadhar_number')

        category = request.POST.get('category')
        reservation_category = request.POST.get('reservation_category')
        blood_group = request.POST.get('blood_group')
        ph_status = True if request.POST.get('ph_status') == "True" else False
        hobbies = request.POST.get('hobbies')
        scholarship = request.POST.get('scholarship')
        transport_mode = request.POST.get('transport_mode')
        mother_tongue = request.POST.get('mother_tongue')
        height = request.POST['height'] if request.POST['height'].isdigit() else None


        weight = request.POST['weight'] if request.POST['weight'].isdigit() else None
        illness = request.POST.get('illness')

        per_d=Personal_details.objects.filter(student_id=sid)
        per_d.delete()

        PS=Personal_details(student_id=sid,student_fullname=student_fullname,branch=branch,section=section,semester=semester,scheme=scheme,dob=dob,gender=gender,student_phone_no=student_phone_no,student_email_id=student_email_id,L_hno=l_hno,L_street=l_street,L_city=l_city,L_district=l_district,L_state=l_state,L_pincode=l_pincode,P_hno=p_hno,P_street=p_street,P_city=p_city,P_district=p_district,P_state=p_state,P_pincode=p_pincode,residential_details=residential_details,nationality=nationality,aadhar_number=aadhar_number,category=category,reservation_category=reservation_category,bloodgroup=blood_group,ph_status=ph_status,hobbies=hobbies,scholarship=scholarship,transport_mode=transport_mode,mother_tongue=mother_tongue,height=height,weight=weight,illness=illness)
        PS.save()

        return HttpResponseRedirect('/student/student_profile_edit/')




def ECST_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        activity = request.POST.getlist('activity')
        role = request.POST.getlist('role')

        existing_records=Extra_Curriculars.objects.filter(student_id=sid)
        existing_records.delete()

        for i in range(len(activity)):
            if role[i]:
                new_EC = Extra_Curriculars(
                            student_id=sid,
                            activity=activity[i] if i < len(activity) else None,
                            role=role[i] if i < len(role) else None,
                        )
                
                new_EC.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')  # Change '/success/' to your desired URL
    





def S_remarks_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        mentor_remarks = request.POST.getlist('mentor_remarks')
        student_opinions = request.POST.getlist('student_opinions')
        remarks_sem = request.POST.getlist('remarks_sem')
        remarks_date=[datetime.strptime(date, '%Y-%m-%d').date() if date else None for date in request.POST.getlist('remarks_date')]




        existing_records=Remarks.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(remarks_date)):
            if remarks_date[i]:
                new_bac = Remarks(
                            student_id=sid,
                            remarks_sem=remarks_sem[i] if i < len(remarks_sem) else None,
                            mentor_remarks=mentor_remarks[i] if i < len(mentor_remarks) else None,
                            student_opinions=student_opinions[i] if i < len(student_opinions) else None,
                            remarks_date=remarks_date[i] if i < len(remarks_date) else None,
                        )
                new_bac.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/student/student_profile_edit/')
    


def request_to_add_new_skill(request):
    if request.method == 'POST':
        skill_name=request.POST.get('skill_name_r')
        sector=request.POST.get('sector_r')
        domain=request.POST.get('domain_r')

        new_obj = Skill(skill_name=skill_name,sector=sector,domain=domain)
        new_obj.save()
        request.session['request_sent']=True
        return HttpResponseRedirect('/student/skill_application/')





def verify_passcode(request,id):
    if request.method=='POST':
        passcode=request.POST.get('passcode')
        exam=QMODEL.Course.objects.get(id=id)
        if exam.passcode==passcode:
            request.session["passcode_status"]=True
            return HttpResponseRedirect(f'/student/take-exam/{id}')
        else:
            return HttpResponseRedirect('/student/student-exam')




    

def get_skills(request):
    sector=request.POST.get('sector','')
    domain=request.POST.get('domain','')
    print(domain)
    if sector:
        skills=Skill.objects.filter(sector=sector)
    else:
        skills = Skill.objects.all()
    if domain:
        skills=skills.filter(domain=domain)
    skills=skills.values_list('skill_name',flat=True).distinct()
    return JsonResponse(list(skills), safe=False)


def get_domains(request):
    sector = request.POST.get('sector','')
    if sector:
        domains = Skill.objects.filter(sector=sector).values_list('domain',flat=True).distinct()
    else:
        domains = Skill.objects.values_list('domain',flat=True).distinct()
    return JsonResponse(list(domains), safe=False)