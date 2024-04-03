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
            return HttpResponseRedirect(f'/student/student_profile/{user.student.roll}')
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
    reg_skills = Registered_skills.objects.filter(status='registered').values('skill_name')

    
    sectors = Registered_skills.objects.filter(status="registered").values('sector').distinct()
    domains = Registered_skills.objects.filter(status="registered").values('domain').distinct()

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
    if request.method=='POST':
        #STUDENT_TABLE
        sid=request.POST['sid']
        student_fullname=request.POST['student_fullname']
        branch = request.POST.get('branch',None)
        section = request.POST.get('section', None)
        semester=request.POST.get('semester',None)
        scheme=request.POST.get('section', None)
        dob = datetime.strptime(request.POST['dob'],'%Y-%m-%d').date() if request.POST.get('dob') else None 
        gender=request.POST.get('gender',None)
        student_phone_no = request.POST.get('student_phone_no')
        if student_phone_no:
            try:
                student_phone_no = int(student_phone_no)
            except ValueError:
                pass
        else:
            student_phone_no = None
        student_email_id=request.POST['student_email_id']
        
        l_hno=request.POST['l_hno']
        l_street=request.POST['l_street']
        l_city=request.POST['l_city']
        l_district=request.POST['l_district']
        l_state=request.POST['l_state']
        l_pincode=request.POST['l_pincode']
        l_pincode = int(l_pincode) if l_pincode else None
        p_hno=request.POST['p_hno']
        p_street=request.POST['p_street']
        p_city=request.POST['p_city']
        p_district=request.POST['p_district']
        p_state=request.POST['p_state']
        p_pincode=request.POST['p_pincode']
        p_pincode = int(p_pincode) if p_pincode else None

        residential_details=request.POST.get('residential_details',None)
        nationality=request.POST['nationality']
        aadhar_number=request.POST['aadhar_number']
        aadhar_number = int(aadhar_number) if aadhar_number else None

        category=request.POST.get('category',None)
        reservation_category=request.POST.get('reservation_category',None)
        blood_group=request.POST.get('blood_group',None)
        ph_status=True if request.POST.get('ph_status')=="True" else False
        hobbies=request.POST['hobbies']
        scholarship=request.POST['scholarship']
        transport_mode=request.POST.get('transport_mode',None)
        mother_tongue=request.POST['mother_tongue']
        height=request.POST['height']
        height = int(height) if height else None
        weight=request.POST['weight']
        weight = int(weight) if weight else None
        illness=request.POST['illness']
        
        #PARENTS_TABLE
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

        # EDUCATION_TABLE
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

        # COMPETITIVE_EXAMS_TABLE
        test_name = request.POST.get('test_name')
        rank_obtained = int(request.POST['rank_obtained']) if 'rank_obtained' in request.POST and request.POST['rank_obtained'] else None
        score_obtained = int(request.POST['score_obtained']) if 'score_obtained' in request.POST and request.POST['score_obtained'] else None

        # PROFILE_TABLE
        profile_name = request.POST.get('profile_name')
        profile_url = request.POST.get('profile_url')

        # ACHIEVEMENTS_TABLE
        achieve_name = request.POST.get('achieve_name')
        achieve_score = int(request.POST['achieve_score']) if 'achieve_score' in request.POST and request.POST['achieve_score'] else None

        # SKILLS_TABLE
        skill_name = request.POST.get('skill_name')
        test_score = int(request.POST['test_score']) if 'test_score' in request.POST and request.POST['test_score'] else None
        project_name = request.POST.get('project_name')
        project_type = request.POST.get('project_type')
        project_score = int(request.POST['project_score']) if 'project_score' in request.POST and request.POST['project_score'] else None
        certification_status = True if request.POST.get('certification_status') == "True" else False
        updated_date = datetime.strptime(request.POST['updated_date'],'%Y-%m-%d').date() if request.POST.get('updated_date') else None
        faculty_id = int(request.POST.get('faculty_id', '').strip()) if request.POST.get('faculty_id', '').strip() else None
        skill_status = request.POST.get('skill_status')
        overall_score = request.POST.get('overall_score')

        # CERTIFICATIONS_TABLE
        certificate_name = request.POST.get('certificate_name')
        certificate_score = int(request.POST['certificate_score']) if 'certificate_score' in request.POST and request.POST['certificate_score'] else None
        certification_date = datetime.strptime(request.POST['certification_date'],'%Y-%m-%d').date() if request.POST.get('certification_date') else None

        # INTERNSHIP_TABLE
        tech_name = request.POST.get('tech_name')
        internship_name = request.POST.get('internship_name')
        internship_mode = request.POST.get('internship_mode')
        internship_duration = int(request.POST.get('internship_duration', '').strip()) if request.POST.get('internship_duration', '').strip() else None
        date_of_completion = datetime.strptime(request.POST['date_of_completion'],'%Y-%m-%d').date() if request.POST.get('date_of_completion') else None
        stipend = True if request.POST.get('stipend') == "True" else False

        # EXTRA_CURRICULARS_TABLE
        activity = request.POST.get('activity')
        role = request.POST.get('role')

        # ATTENDANCE_TABLE
        attendance_sem = request.POST.get('attendance_sem')
        month = request.POST.get('month')
        phase = request.POST.get('phase')
        attendance_percentage = int(request.POST['attendance_percentage']) if 'attendance_percentage' in request.POST and request.POST['attendance_percentage'] else None

        # SEMWISE_GRADES_TABLE
        grades_sem = request.POST.get('grades_sem')
        sgpa = float(request.POST['sgpa']) if 'sgpa' in request.POST and request.POST['sgpa'] else None
        cgpa = float(request.POST['cgpa']) if 'cgpa' in request.POST and request.POST['cgpa'] else None

        # SEMESTER_MARKS_TABLE
        sname = request.POST.get('sname')
        sub_type = request.POST.get('sub_type')
        first_ses = request.POST.get('first_ses')
        second_ses = request.POST.get('second_ses')
        marks_sem = request.POST.get('marks_sem')
        grade = request.POST.get('grade')

        # BACKLOGS_TABLE
        sname = request.POST.get('sname')
        backlog_sem = request.POST.get('backlog_sem')
        sem_cleared = request.POST.get('sem_cleared')
        ayoc = datetime.strptime(request.POST['ayoc'],'%Y-%m-%d').date() if request.POST.get('ayoc') else None

        # PLACEMENT_TABLE
        company = request.POST.get('company')
        date_placed = datetime.strptime(request.POST['date_placed'],'%Y-%m-%d').date() if request.POST.get('date_placed') else None
        package = request.POST.get('package')
        drive_mode = request.POST.get('drive_mode')

        # REMARKS_TABLE
        remarks_date = datetime.strptime(request.POST['remarks_date'],'%Y-%m-%d').date() if request.POST.get('remarks_date') else None
        student_opinions = request.POST.get('student_opinions')
        mentor_remarks = request.POST.get('mentor_remarks')
        remarks_sem = request.POST.get('remarks_sem')

        try:
            ps_obj= Personal_details.objects.get(student_id=sid)
        except:
            ps_obj=None

        if ps_obj:
            ps_obj.student_id=sid
            ps_obj.student_fullname=student_fullname
            ps_obj.branch=branch
            ps_obj.semester=semester
            ps_obj.section=section
            ps_obj.dob=dob
            ps_obj.gender=gender
            ps_obj.scheme=scheme
            ps_obj.student_phone_no=student_phone_no
            ps_obj.student_email_id=student_email_id
            ps_obj.L_hno=l_hno
            ps_obj.L_street=l_street
            ps_obj.L_city=l_city
            ps_obj.L_district=l_district
            ps_obj.L_state=l_state
            ps_obj.L_pincode=l_pincode
            ps_obj.P_hno=p_hno
            ps_obj.P_street=p_street
            ps_obj.P_city=p_city
            ps_obj.P_district=p_district
            ps_obj.P_state=p_state
            ps_obj.P_pincode=p_pincode
            ps_obj.residential_details=residential_details
            ps_obj.nationality=nationality
            ps_obj.aadhar_number=aadhar_number
            ps_obj.category=category
            ps_obj.reservation_category=reservation_category
            ps_obj.bloodgroup=blood_group
            ps_obj.ph_status=ph_status
            ps_obj.hobbies=hobbies
            ps_obj.scholarship=scholarship
            ps_obj.transport_mode=transport_mode
            ps_obj.mother_tongue=mother_tongue
            ps_obj.height=height
            ps_obj.weight=weight
            ps_obj.illness=illness
            ps_obj.save()

        try:
            pd_obj= Parents_details.objects.get(student_id=sid)
        except:
            pd_obj=None
        
        if pd_obj:
            pd_obj=Parents_details.objects.get(student_id=sid)
            pd_obj.father_name=father_name
            pd_obj.father_occupation=father_occupation
            pd_obj.father_phone_number=father_phone
            pd_obj.mother_name=mother_name
            pd_obj.mother_occupation=mother_occupation
            pd_obj.mother_phone_number=mother_phone
            pd_obj.guardian_name=guardian_name
            pd_obj.guardian_occupation=guardian_occupation
            pd_obj.guardian_phone_number=guardian_phone
            pd_obj.parent_email=pg_email
            pd_obj.save()

        try:
            ed1_obj= Education_details.objects.filter(student_id=sid).first()
        except:
            ed1_obj=None
        
        if ed1_obj:
            ed1_obj=Education_details.objects.filter(student_id=sid).first()
            ed1_obj.qualification=s_qualification
            ed1_obj.institute_name=s_institute_name
            ed1_obj.institute_location=s_institute_location
            ed1_obj.YOP=s_YOP
            ed1_obj.board=s_board
            ed1_obj.percentage=s_percentage
            ed1_obj.gpa=s_gpa
            ed1_obj.medium=s_medium
            ed1_obj.save()
        try:
            ed2_obj= Education_details.objects.filter(student_id=sid).last()
        except:
            ed2_obj=None
        
        if ed2_obj:
            ed2_obj=Education_details.objects.filter(student_id=sid).last()
            # ed2_obj=Education_details.objects.get(student_id=sid)
            ed2_obj.qualification=h_qualification
            ed2_obj.course=h_course
            ed2_obj.institute_name=h_institute_name
            ed2_obj.institute_location=h_institute_location
            ed2_obj.YOP=h_YOP
            ed2_obj.board=h_board
            ed2_obj.percentage=h_percentage
            ed2_obj.gpa=h_gpa
            ed2_obj.medium=h_medium
            ed2_obj.save()


            ce_obj=Competitive_exam.objects.get(student_id=sid)
            ce_obj.test_name=test_name
            ce_obj.rank_obtained=rank_obtained
            ce_obj.score_obtained=score_obtained
            ce_obj.save()

            p_obj=Profile.objects.get(student_id=sid)
            p_obj.profile_name=profile_name
            p_obj.profile_url=profile_url
            p_obj.save()

            a_obj=Achievements.objects.get(student_id=sid)
            a_obj.achieve_name=achieve_name
            a_obj.achieve_score=achieve_score
            a_obj.save()

            s_obj=Skills.objects.get(student_id=sid)
            s_obj.skill_name=skill_name
            s_obj.test_score=test_score
            s_obj.project_name=project_name
            s_obj.project_type=project_type
            s_obj.project_score=project_score
            s_obj.certification_status=certification_status
            s_obj.updated_date=updated_date
            s_obj.faculty_id=faculty_id
            s_obj.skill_status=skill_status
            s_obj.overall_score=overall_score
            s_obj.save()



            c_obj=Certifications.objects.get(student_id=sid)
            c_obj.certificate_name=certificate_name
            c_obj.certificate_score=certificate_score
            c_obj.certification_date=certification_date
            c_obj.save()

            i_obj=Internships.objects.get(student_id=sid)
            i_obj.tech_name=tech_name
            i_obj.internship_name=internship_name
            i_obj.internship_mode=internship_mode
            i_obj.internship_duration=internship_duration
            i_obj.date_of_completion=date_of_completion
            i_obj.stipend=stipend
            i_obj.save()

            ec_obj=Extra_Curriculars.objects.get(student_id=sid)
            ec_obj.activity=activity
            ec_obj.role=role
            ec_obj.save()

            ad_obj=Attendance_details.objects.get(student_id=sid)
            ad_obj.attendance_sem=attendance_sem
            ad_obj.month=month
            ad_obj.phase=phase
            ad_obj.attendance_percentage=attendance_percentage
            ad_obj.save()

            sg_obj=Semwise_grades.objects.get(student_id=sid)
            sg_obj.grades_sem=grades_sem
            sg_obj.sgpa=sgpa
            sg_obj.cgpa=cgpa
            sg_obj.save()

            sm_obj=Semester_marks.objects.get(student_id=sid)
            sm_obj.subject_name=sname
            sm_obj.subject_type=sub_type
            sm_obj.first_sessional=first_ses
            sm_obj.second_sessional=second_ses
            sm_obj.marks_sem=marks_sem
            sm_obj.grade_obtained=grade
            sm_obj.save()


            b_obj=Backlogs.objects.get(student_id=sid)
            b_obj.subject_name=sname
            b_obj.backlog_sem=backlog_sem
            b_obj.sem_cleared=sem_cleared
            b_obj.ayoc=ayoc
            b_obj.save()

            place_obj=Placements.objects.get(student_id=sid)
            place_obj.company=company
            place_obj.date_placed=date_placed
            place_obj.package=package
            place_obj.drive_mode=drive_mode
            place_obj.save()

            r_obj=Remarks.objects.get(student_id=sid)
            r_obj.remarks_date=remarks_date
            r_obj.student_opinions=student_opinions
            r_obj.mentor_remarks=mentor_remarks
            r_obj.remarks_sem=remarks_sem
            r_obj.save()
        else:
            PS=Personal_details(student_id=sid,student_fullname=student_fullname,branch=branch,section=section,semester=semester,scheme=scheme,dob=dob,gender=gender,student_phone_no=student_phone_no,student_email_id=student_email_id,L_hno=l_hno,L_street=l_street,L_city=l_city,L_district=l_district,L_state=l_state,L_pincode=l_pincode,P_hno=p_hno,P_street=p_street,P_city=p_city,P_district=p_district,P_state=p_state,P_pincode=p_pincode,residential_details=residential_details,nationality=nationality,aadhar_number=aadhar_number,category=category,reservation_category=reservation_category,bloodgroup=blood_group,ph_status=ph_status,hobbies=hobbies,scholarship=scholarship,transport_mode=transport_mode,mother_tongue=mother_tongue,height=height,weight=weight,illness=illness)
            PD=Parents_details(student_id=sid,father_name=father_name,father_occupation=father_occupation,father_phone_number=father_phone,mother_name=mother_name,mother_occupation=mother_occupation,mother_phone_number=mother_phone,guardian_name=guardian_name,guardian_occupation=guardian_occupation,guardian_phone_number=guardian_phone,parent_email=pg_email)
            ED1=Education_details(student_id=sid,qualification=s_qualification,institute_name=s_institute_name,institute_location=s_institute_location,YOP=s_YOP,board=s_board,percentage=s_percentage,gpa=s_gpa,medium=s_medium)
            ED2=Education_details(student_id=sid,qualification=h_qualification,course=h_course,institute_name=h_institute_name,institute_location=h_institute_location,YOP=h_YOP,board=h_board,percentage=h_percentage,gpa=h_gpa,medium=h_medium)
            CE=Competitive_exam(student_id=sid,test_name=test_name,rank_obtained=rank_obtained,score_obtained=score_obtained)
            P=Profile(student_id=sid,profile_name=profile_name,profile_url=profile_url)
            A=Achievements(student_id=sid,achieve_name=achieve_name,achieve_score=achieve_score)
            S=Skills(student_id=sid,skill_name=skill_name,test_score=test_score,project_score=project_score,updated_date=updated_date,faculty_id=faculty_id,certification_status=certification_status,project_name=project_name,project_type=project_type,skill_status=skill_status,overall_score=overall_score)
            C=Certifications(student_id=sid,certificate_name=certificate_name,certificate_score=certificate_score,certification_date=certification_date)
            I=Internships(student_id=sid,tech_name=tech_name,internship_name=internship_name,internship_mode=internship_mode,internship_duration=internship_duration,date_of_completion=date_of_completion,stipend=stipend)
            EC=Extra_Curriculars(student_id=sid,activity=activity,role=role)
            AD=Attendance_details(student_id=sid,attendance_sem=attendance_sem,month=month,phase=phase,attendance_percentage=attendance_percentage)
            SG=Semwise_grades(student_id=sid,grades_sem=grades_sem,sgpa=sgpa,cgpa=cgpa)
            SM=Semester_marks(student_id=sid,subject_name=sname,subject_type=sub_type,first_sessional=first_ses,second_sessional=second_ses,marks_sem=marks_sem,grade_obtained=grade)
            B=Backlogs(student_id=sid,subject_name=sname,backlog_sem=backlog_sem,sem_cleared=sem_cleared,ayoc=ayoc)
            Place=Placements(student_id=sid,company=company,date_placed=date_placed,package=package,drive_mode=drive_mode)
            R=Remarks(student_id=sid,remarks_date=remarks_date,student_opinions=student_opinions,mentor_remarks=mentor_remarks,remarks_sem=remarks_sem)
            
            PS.save()
            PD.save()
            ED1.save()
            ED2.save()
            CE.save()
            P.save()
            A.save()
            S.save()
            C.save()
            I.save()
            EC.save()
            AD.save()
            SG.save()
            SM.save()
            B.save()
            Place.save()
            R.save()

        # else:
        #     return render(request,'form.html',user="student")
    
        # return render(request,'student_dashboard.html',{})
        # return render(request,'student_dashboard.html')
        msg=" Submitted"
        txt="details submitted successfully !"
        return render(request, 'student/success.html',{'message':msg,'text':txt})
    
    # try:
    #     user1=request.session.get('uid')
    # except:
    #     user1=None
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
    if request.user.groups.filter(name='mentor').exists():
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

        ski_det = students_skills.objects.filter(student=s_rec,skill_status='evaluated').order_by(F('overall_score').desc())
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

        new_obj = Registered_skills(skill_name=skill_name,sector=sector,domain=domain,status='pending')
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
        skills=Registered_skills.objects.filter(sector=sector)
    else:
        skills = Registered_skills.objects.all()
    if domain:
        skills=skills.filter(domain=domain)
    skills=skills.values_list('skill_name',flat=True).distinct()
    return JsonResponse(list(skills), safe=False)


def get_domains(request):
    sector = request.POST.get('sector','')
    if sector:
        domains = Registered_skills.objects.filter(sector=sector).values_list('domain',flat=True).distinct()
    else:
        domains = Registered_skills.objects.values_list('domain',flat=True).distinct()
    return JsonResponse(list(domains), safe=False)