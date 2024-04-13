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
        return HttpResponseRedirect('mentor-dashboard')
    return redirect('mentorlogin')

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
# def students_list(request):
#     user_instance = User.objects.get(username=request.user)
#     teacher_instance = mentor.objects.get(user=user_instance)
#     students_data = Student.objects.filter(TD=teacher_instance).prefetch_related('user')
#     return render(request, 'mentor/students_list.html', {'details': students_data})


# @login_required(login_url='mentorlogin')
# @user_passes_test(is_approved)
# def mentor_dashboard_view(request):
#     dict={
    
#     'total_course':QMODEL.Course.objects.all().count(),
#     'total_question':QMODEL.Question.objects.all().count(),
#     'total_student':SMODEL.Student.objects.all().count()
#     }
#     return render(request,'mentor/mentor_dashboard.html',context=dict)

def mentor_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        newpassword = request.POST.get('newpassword')
        if newpassword:
            user = User.objects.get(email=email)
            user.set_password(newpassword)
            user.save()
        return redirect('mentorlogin')
    return render(request, 'management/forgot_password.html')


#---sai views------------------------

import datetime
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
from django.db.models import Q
from .models import *
from management.models import *
from datetime import date, datetime
from student.models import * 
# Create your views here.



def mentor_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            return HttpResponseRedirect('/')
        else:
            messages.info(request,"user name or password does not match !")
            return redirect("mentorlogin")
    return render(request,'mentor/mentorlogin.html')



# def mentor_signup_view(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         EmployeeID=request.POST['EmployeeID']
#         full_name=request.POST['full_name']
#         department=request.POST['department']
#         mobile=request.POST['mobile']
#         email=request.POST['email']
#         password=request.POST['password']

#         if(User.objects.filter(email=email).exists()):
#             messages.info(request,"email already exists !")
#             return redirect("mentorsignup")
#         elif(User.objects.filter(username=username).exists()):
#             messages.info(request,"user already exists !")
#             return redirect("mentorsignup")
#         else:
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.mobile = mobile
#             user.EmployeeID = EmployeeID
#             user.name = full_name
#             user.department = department
#             user.status=False          
#             user.save()
#             mentor1=mentor(user=user,emp_id=EmployeeID,name=full_name,status=False,department=department,mobile=mobile,email=email)
#             mentor1.save()
#             mentor_group = Group.objects.get(name='mentor')
#             mentor_group.user_set.add(user)
#             return redirect('mentorlogin')
#     return render(request,'mentor/mentorsignup.html')



# @login_required(login_url='examinerlogin')
def students_list(request):                            
    user_instance = User.objects.get(username=request.user)
    mentor_instance = mentor.objects.get(user=user_instance)
    students_data = Student.objects.filter(mentor=mentor_instance).prefetch_related('user')
    return render(request, 'mentor/students_list.html', {'details': students_data})


@login_required(login_url='mentorlogin')
def mentor_dashboard_view(request):
    m_user=request.user
    M_obj=mentor.objects.get(user=m_user)
    dict={
    'total_students':Student.objects.filter(mentor=M_obj).count(),
    'total_applications' : students_skills.objects.filter(student__mentor=M_obj).count(),
    'total_evaluated':students_skills.objects.filter(student__mentor=M_obj,skill_status="evaluated").count()
    }
    return render(request,'mentor/mentor_dashboard.html',context=dict)



def students_skill_applications(request):
    if request.method=='POST':
        pass
    mentor_instance = get_object_or_404(mentor, user=request.user)
    students_data = Student.objects.filter(mentor=mentor_instance)
    student_applications = students_skills.objects.filter(student__in=students_data)
    examiner=examiner_skills.objects.filter(skill_status=True)
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
    eapp=Examiner.objects.get(id=examiner)
    examiner=Examiner.objects.get(id=eapp.id) 
    new_app=student_skill_exam_applications(student=sapp.student,branch=sapp.student.branch,section=sapp.student.section,mentor_identity_number=sapp.student.mentor.id,requested_date=today,application_status="pending",skill_name=sapp.skill_name,assessed_by=eapp.user.id,sem=sapp.student.semester)
    new_app.save()
    sapp.skill_status="under evaluation"
    sapp.save()
    messages.info(request,f"{sapp.student.name.upper()} student application sent to {examiner.name.upper()} successfully")
    return HttpResponseRedirect('/mentor/students_skill_applications')


def students_scores_view(request):
    mentor_instance = get_object_or_404(mentor, user=request.user)
    students_data = Student.objects.filter(mentor=mentor_instance)


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
    registered_skill = Skill.objects.get(skill_name=student_skill)
    print(registered_skill.skill_name)
    print(registered_skill.level)
    if registered_skill.level == 'Basic':
        multiplier = 1
    elif registered_skill.level == 'Intermediate':
        multiplier = 2
    elif registered_skill.level == 'Advanced':
        multiplier = 3
    else:
        multiplier = 1  # Default multiplier

    student_skill.project_name=  request.POST['project_name']
    student_skill.project_type =request.POST['project_type']
    student_skill.updated_date=  request.POST['update_date']
    student_skill.project_score=request.POST['marks']
    student_skill.skill_status="evaluated"
    student_skill.overall_score =  (int(student_skill.test_score)+int(student_skill.project_score))*multiplier

    student_skill.save()

    user1=student_skill.student.roll
    s_rec=Student.objects.get(roll=user1)
    ski_det = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
    ach_det=Achievements.objects.filter(student_id=user1)
    int_det=Internships.objects.filter(student_id=user1)
    cer_det=Certifications.objects.filter(student_id=user1)

    skill_score=0
    for i in ski_det:
        skill_score+=int(i.overall_score)

    achievements_score=0
    for i in ach_det:
        achievements_score+=int(i.achieve_score)

    certifications_score=0
    for i in cer_det:
        certifications_score+=int(i.certificate_score)

    int_det_count=int_det.count()
    Internships_score=int_det_count*50
    Profile_score=skill_score + achievements_score + certifications_score + Internships_score
    s_rec.profile_score=Profile_score
    s_rec.save()
    return HttpResponseRedirect('/mentor/students_scores')

from django.db.models import F

@login_required(login_url='mentorlogin')
def student_profile(request,roll):
    if request.user.groups.filter(name='MENTOR').exists():
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
            
        ach_det=Achievements.objects.filter(student_id=user1)
        int_det=Internships.objects.filter(student_id=user1)
        cer_det=Certifications.objects.filter(student_id=user1)
        ext_det=Extra_Curriculars.objects.filter(student_id=user1)

        profile_score = Student.objects.filter(roll=roll).values('profile_score').first()
        
        
        base_url = f"{request.scheme}://{request.META['HTTP_HOST']}"
        # base_url_without_student = base_url.replace("/student", "")

        profile_url = f"{base_url}/student_profile/{roll}"

        return render(request, 'mentor/student_profile.html', {'per_det': per_det, 'prof_det': prof_det, 'ski_det': ski_det, 'ach_det': ach_det, 'int_det': int_det, 'cer_det': cer_det, 'ext_det': ext_det,"profile_url":profile_url,'Profile_score':profile_score})
    else:
        return HttpResponseRedirect(f'/student_profile/{roll}')


def student_profile_edit_c(request,roll):
    request.session['student_details_edit']=roll
    return HttpResponseRedirect('/mentor/student_profile_edit')



def user_auth_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='MENTOR').exists():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not authorized to access this page.')
            return redirect('some_redirect_url')  # Redirect to an appropriate URL
    return wrap

# Create your views here.
@login_required
@user_auth_required
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



def achievements_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        achieve_names = request.POST.get('achieve_name')
        achieve_scores = request.POST.get('achieve_score')
        achieve_files = request.FILES.get('achieve_file')



        # achieve_scores = [int(score) if score else None for score in request.POST.getlist('achieve_score')]

        # existing_records=Achievements.objects.filter(student_id=sid)
        # existing_records.delete()
        new_achievement = Achievements(
                            student_id=sid,
                            achieve_name=achieve_names if achieve_names else None,
                            achieve_score=achieve_scores if achieve_scores else None,
                            achieve_file=achieve_files  
                        )
                
        new_achievement.save()


                
        user1=sid
        s_rec=Student.objects.get(roll=user1)
        ski_det = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
        ach_det=Achievements.objects.filter(student_id=user1)
        int_det=Internships.objects.filter(student_id=user1)
        cer_det=Certifications.objects.filter(student_id=user1)

        skill_score=0
        for i in ski_det:
            skill_score+=int(i.overall_score)

        achievements_score=0
        for i in ach_det:
            achievements_score+=int(i.achieve_score)

        certifications_score=0
        for i in cer_det:
            certifications_score+=int(i.certificate_score)

        int_det_count=int_det.count()
        Internships_score=int_det_count*50
        Profile_score=skill_score + achievements_score + certifications_score + Internships_score
        s_rec.profile_score=Profile_score
        s_rec.save()
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')  # Change '/success/' to your desired URL


import os

def delete_achievement_view(request,oid,sid):
    obj=Achievements.objects.get(id=oid)
    file_path = obj.achieve_file.path

    obj.delete()

    if os.path.exists(file_path):
        os.remove(file_path)
    return HttpResponseRedirect(f"/mentor/student_profile_edit_c/{sid}")



def edit_achievement_view(request,id):
    if request.method == 'POST':
        A_name = request.POST.get('achieve_name')
        A_score = request.POST.get('achieve_score')
        A_obj=Achievements.objects.get(id=id)
        A_obj.achieve_name=A_name
        A_obj.achieve_score=A_score
        A_obj.save()
        return HttpResponseRedirect("/mentor/student_profile_edit/")





def cert_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        certificate_name = request.POST.getlist('certificate_name')
        certificate_score = [int(score) if score else None for score in request.POST.getlist('certificate_score')]
        certification_dates=[datetime.strptime(date, '%Y-%m-%d').date() if date else None for date in request.POST.getlist('certification_date')]
        print(sid)
        print(certificate_name)
        print(certificate_score)
        print(certification_dates)



        existing_records=Certifications.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(certificate_name)):
            if certificate_name[i]:
                new_cert = Certifications(
                            student_id=sid,
                            certificate_name=certificate_name[i] if i < len(certificate_name) else None,
                            certificate_score=certificate_score[i] if i < len(certificate_score) else None,
                            certification_date=certification_dates[i] if i < len(certification_dates) else None,
                        )
                new_cert.save()
        user1=sid
        s_rec=Student.objects.get(roll=user1)
        ski_det = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
        ach_det=Achievements.objects.filter(student_id=user1)
        int_det=Internships.objects.filter(student_id=user1)
        cer_det=Certifications.objects.filter(student_id=user1)

        skill_score=0
        for i in ski_det:
            skill_score+=int(i.overall_score)

        achievements_score=0
        for i in ach_det:
            achievements_score+=int(i.achieve_score)

        certifications_score=0
        for i in cer_det:
            certifications_score+=int(i.certificate_score)

        int_det_count=int_det.count()
        Internships_score=int_det_count*50
        Profile_score=skill_score + achievements_score + certifications_score + Internships_score
        s_rec.profile_score=Profile_score
        s_rec.save()
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')  # Change '/success/' to your desired URL


def EC_view(request):
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
        return HttpResponseRedirect('/mentor/student_profile_edit/')  # Change '/success/' to your desired URL
    





def ATT_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        attendance_sem = request.POST.getlist('attendance_sem')
        month = request.POST.getlist('month')
        phase = request.POST.getlist('phase')
        attendance_percentage = request.POST.getlist('attendance_percentage')

        existing_records=Attendance_details.objects.filter(student_id=sid)
        existing_records.delete()

        for i in range(len(attendance_sem)):
            if attendance_sem[i]:
                new_ATT = Attendance_details(
                            student_id=sid,
                            attendance_sem=attendance_sem[i] if i < len(attendance_sem) else None,
                            month=month[i] if i < len(month) else None,
                            phase=phase[i] if i < len(phase) else None,
                            attendance_percentage=attendance_percentage[i] if i < len(attendance_percentage) else None,
                        )
                
                new_ATT.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')
    



def bac_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        sname = request.POST.getlist('sname')
        backlog_sem = request.POST.getlist('backlog_sem')
        sem_cleared = request.POST.getlist('sem_cleared')
        ayoc=[datetime.strptime(date, '%Y-%m-%d').date() if date else None for date in request.POST.getlist('ayoc')]




        existing_records=Backlogs.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(sname)):
            if sname[i]:
                new_bac = Backlogs(
                            student_id=sid,
                            subject_name=sname[i] if i < len(sname) else None,
                            backlog_sem=backlog_sem[i] if i < len(backlog_sem) else None,
                            sem_cleared=sem_cleared[i] if i < len(sem_cleared) else None,
                            ayoc=ayoc[i] if i < len(ayoc) else None,
                        )
                new_bac.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')
    





def remarks_view(request):
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
        return HttpResponseRedirect('/mentor/student_profile_edit/')
    

def intern_view(request):
    if request.method == 'POST':
         # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        
        tech_name = request.POST.getlist('tech_name')
        internship_name = request.POST.getlist('internship_name')
        internship_mode = request.POST.getlist('internship_mode')
        internship_duration = request.POST.getlist('internship_duration')
        stipend = request.POST.getlist('stipend')
        date_of_completion=[datetime.strptime(date, '%Y-%m-%d').date() if date else None for date in request.POST.getlist('date_of_completion')]




        existing_records=Internships.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(internship_name)):
            if internship_name[i]:
                new_intern = Internships(
                            student_id=sid,
                            tech_name=tech_name[i] if i < len(tech_name) else None,
                            internship_name=internship_name[i] if i < len(internship_name) else None,
                            internship_mode=internship_mode[i] if i < len(internship_mode) else None,
                            internship_duration=internship_duration[i] if i < len(internship_duration) else None,
                            date_of_completion=date_of_completion[i] if i < len(date_of_completion) else None,
                            stipend=stipend[i] if i < len(stipend) else None,
                        )
                new_intern.save()
        user1=sid
        s_rec=Student.objects.get(roll=user1)
        ski_det = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
        ach_det=Achievements.objects.filter(student_id=user1)
        int_det=Internships.objects.filter(student_id=user1)
        cer_det=Certifications.objects.filter(student_id=user1)

        skill_score=0
        for i in ski_det:
            skill_score+=int(i.overall_score)

        achievements_score=0
        for i in ach_det:
            achievements_score+=int(i.achieve_score)

        certifications_score=0
        for i in cer_det:
            certifications_score+=int(i.certificate_score)

        int_det_count=int_det.count()
        Internships_score=int_det_count*50
        Profile_score=skill_score + achievements_score + certifications_score + Internships_score
        s_rec.profile_score=Profile_score
        s_rec.save()
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')
    




def pm_view(request):
    if request.method == 'POST':
        # Assuming you have a form with CSRF token and fields sid, achieve_name, and achieve_score
        sid = request.POST['sid']
        company = request.POST.getlist('company')
        date_placed=[datetime.strptime(date, '%Y-%m-%d').date() if date else None for date in request.POST.getlist('date_placed')]
        drive_mode = request.POST.getlist('drive_mode')
        package = request.POST.getlist('package')

        existing_records=Placements.objects.filter(student_id=sid)
        existing_records.delete()
        for i in range(len(drive_mode)):
            if drive_mode[i]:
                new_pm = Placements(
                            student_id=sid,
                            company=company[i] if i < len(company) else None,
                            date_placed=date_placed[i] if i < len(date_placed) else None,
                            package=package[i] if i < len(package) else None,
                            drive_mode=drive_mode[i] if i < len(drive_mode) else None,
                        )
                new_pm.save()
        
        # Redirect to a success page or wherever you need to redirect after form submission
        return HttpResponseRedirect('/mentor/student_profile_edit/')