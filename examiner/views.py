from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group,auth
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from management import models as QMODEL
from student import models as SMODEL
from management import forms as QFORM
from .models import *
from student.models import *
from management.models import *
from django.contrib import messages

#for showing signup/login button for examiner
def examinerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'examiner/examinerclick.html')





def examinerlogin_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/examiner/examiner-dashboard')
        else:
            messages.info(request,"user name or password does not match !")
            return redirect("examinerlogin")
    return render(request,'examiner/examinerlogin.html')




def examiner_signup_view(request):
    if request.method=='POST':
        username=request.POST['username']
        EmployeeID=request.POST['EmployeeID']
        full_name=request.POST['full_name']
        department=request.POST['department']
        mobile=request.POST['mobile']
        email=request.POST['email']
        f_skill=request.POST['f_skill']
        password=request.POST['password']

        if(User.objects.filter(email=email).exists()):
            messages.info(request,"email already exists !")
            return redirect("examinersignup")
        elif(User.objects.filter(username=username).exists()):
            messages.info(request,"user already exists !")
            return redirect("examinersignup")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.mobile = mobile
            user.EmployeeID = EmployeeID
            user.name = full_name
            user.department = department
            user.status=False          
            user.save()
            examiner=Examiner(user=user,emp_id=EmployeeID,name=full_name,status=False,department=department,mobile=mobile,email=email,skill=f_skill)
            examiner.save()
            # examiner_skills=QMODEL.examiner_skills(examiner=examiner,skill_name=f_skill)
            # examiner_skills.save()
            mentor_group = Group.objects.get(name='examiner')
            mentor_group.user_set.add(user)
            return redirect('examinersignup')
    return render(request,'examiner/examinersignup.html')



def is_examiner(user):
    return user.groups.filter(name='examiner').exists()

@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_dashboard_view(request):

    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'examiner/examiner_dashboard.html',context=dict)

@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_exam_view(request):
    return render(request,'examiner/examiner_exam.html')


@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_add_exam_view(request):
    if request.method == 'POST':
        choosen_skill = request.POST.get('evaluating_skill')
        exam_name = request.POST.get('exam_name')
        total_questions = request.POST.get('total_questions')

        # Check if the exam name already exists
        if Course.objects.filter(course_name=exam_name).exists():
            warning_message = "Exam name already exists in the course. Please choose a different name."
            return render(request, 'examiner/examiner_add_exam.html', {'warning_message': warning_message})

        # If exam name is unique, create the Course object and save it
        course_obj = Course(course_name=exam_name, question_number=total_questions,skill_name=choosen_skill,examiner_id=request.user.id)
        course_obj.save()

        # Store exam details in session and redirect to add question view
        request.session['exam_name'] = exam_name
        request.session['total_questions'] = total_questions
        return HttpResponseRedirect('/examiner/examiner-add-question')
    
    reg_skills = Skill.objects.filter(status=True).values('skill_name')
    return render(request, 'examiner/examiner_add_exam.html',{'reg_skills':reg_skills})



@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_view_exam_view(request):
    courses = QMODEL.Course.objects.filter(examiner_id=request.user.id)
    print(request.user.id,"?????????????????????????")
    return render(request,'examiner/examiner_view_exam.html',{'courses':courses})      


@login_required(login_url='examinerlogin')
def see_student_view(request, pk):
    request.session['course_selected']=pk
    course = get_object_or_404(QMODEL.Course, id=pk)
    students_list = QMODEL.Result.objects.filter(exam=course).values("student")
    student_records = student_skill_exam_applications.objects.filter(student__in=students_list)



    combined_data = []  

    c=0
    for i in student_records:
        # print(i,"_+_+_++++_+++++++++++++++++++++++++++++++++++++++++")
        student_object=get_object_or_404(Student,id=i.student.id)
        # student_record = i.exam_id =pk #objects.filter(student=student_object,exam_id=pk).last()
            # student_record = student_skill_exam_applications.objects.filter(student=student_object,exam_id=pk).last()
        temp=i.exam_id
        if int(temp) == int(pk):
            c+=1
            results1 = QMODEL.Result.objects.filter(exam=course, student=student_object).last()
            combined_data.append({
                    'student':student_object,
                    'student_name': student_object.name,
                    'branch':i.branch,
                    'section':i.section,
                    'skill_name':results1.exam.course_name,
                    'marks': results1.marks,
                    'date': results1.date,
                    'status': i.application_status
            })
        # print(i.exam_id,"+{+{+{+{+{{++{{+{+{+{++{{+{+{+}}}}}}}}}}}}}}}")
        
    # print(c,pk,'????//////////////////////////////////////////////////')
    if request.method=='POST':
        selected_student_ids = request.POST.getlist('selected_students')
        for student_id in selected_student_ids:
            # su=get_object_or_404(User,id=student_id)
            student_object=get_object_or_404(Student,id=student_id)
            results1 = QMODEL.Result.objects.filter(exam=course, student=student_object).last()  # Assuming one result per student per exam
            student_record = student_skill_exam_applications.objects.filter(student=student_object,exam_id=pk).last()
            student_record1 = students_skills.objects.filter(student=student_object,skill_name=student_record.skill_name).last()
            student_record1.test_score=results1.marks
            examiner_obj=get_object_or_404(Examiner,user=request.user)
            student_record1.assessed_by=examiner_obj
            student_record1.skill_status="test_evaluated"
            student_record1.assessed_by=examiner_obj
            student_record1.save()
            student_record1.test_score=results1.marks
            student_record.completed_date=results1.date
            student_record.marks_obtained=results1.marks
            student_record.application_status="completed"
            student_record.save()
            messages.info(request,"Student Record Updated Successfully !")
    exam=QMODEL.Course.objects.get(id=pk)
    passcode=exam.passcode
    passcode=passcode if passcode else ""

    return render(request, 'examiner/students_course_result.html', {'results': combined_data,'course':course,'passcode':passcode})    




@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/examiner/examiner-view-exam')

@login_required(login_url='adminlogin')
def examiner_question_view(request):
    return render(request,'examiner/examiner_question.html')




@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_add_question_view(request):
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        course_id = request.POST.get('courseID')
        course=QMODEL.Course.objects.get(id=course_id)
        # course = QMODEL.Course.objects.get(id=course_id)
        marks_l=0
        
        for i in range(1,int(request.session.get('total_questions'))+1):
            question = QMODEL.Question(
                course=course,
                question=request.POST.get(f'question_{i}'),
                    option1=request.POST.get(f'option1_{i}'),
                    marks=request.POST.get(f'marks_{i}'),
                    option2=request.POST.get(f'option2_{i}'),
                    option3=request.POST.get(f'option3_{i}'),
                    option4=request.POST.get(f'option4_{i}'),
                    answer=request.POST.get(f'answer_{i}')
                )
            question.save()

        marks_l = marks_l+int(request.POST.get(f'marks_{i}'))
        marks_sum = Question.objects.filter(course=course).aggregate(total_marks=Sum('marks'))['total_marks']
        course.total_marks=marks_sum
        course.save()
        del request.session['total_questions']
        return HttpResponseRedirect(f'/examiner/see-question/{course_id}')
        # else:
        #     question = QMODEL.Question(
        #             course=course,
        #             question=request.POST.get(f'question_1'),
        #             option1=request.POST.get(f'option1_1'),
        #             marks=request.POST.get(f'marks_1'),
        #             option2=request.POST.get(f'option2_1'),
        #             option3=request.POST.get(f'option3_1'),
        #             option4=request.POST.get(f'option4_1'),
        #             answer=request.POST.get(f'answer_1')
        #         )
        #     question.save()
        #     marks_sum1 = Question.objects.filter(course=course).aggregate(total_marks=Sum('marks'))['total_marks']
        #     course.total_marks=marks_sum1
        #     course.save()

        # request.session['course_selected']=course.id
        # return HttpResponseRedirect('/examiner/select_students')
    else:
        questionForm = QFORM.QuestionForm()
        if "exam_name" in request.session:
            en = request.session.get('exam_name')
            TQ = request.session.get('total_questions')
            question_count = TQ  
            exam_name = en
            del request.session['exam_name']

            course1 = QMODEL.Course.objects.get(course_name=exam_name)
            return render(request, 'examiner/examiner_add_question.html', {'questionForm': questionForm, 'selected_course': course1, 'question_count': question_count})
        else:
            question_count=1
            courses=QMODEL.Course.objects.all()
            return render(request, 'examiner/examiner_add_question.html', {'questionForm': questionForm,'question_count': question_count,'courses':courses})





@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def examiner_view_question_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'examiner/examiner_view_question.html',{'courses':courses})

@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'examiner/see_question.html',{'questions':questions,'course_id':pk})

@login_required(login_url='examinerlogin')
@user_passes_test(is_examiner)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect(f'/examiner/see-question/{question.course.id}')




@login_required(login_url='examinerlogin')
def students_list(request):
    user_instance = student_skill_exam_applications.objects.filter(assessed_by=request.user.id)

    # examiner_instance = examiner.objects.get(user=user_instance)
    # students_data = Student.objects.filter(TD=examiner_instance).prefetch_related('user')
    return render(request, 'examiner/sample.html', {'details': user_instance})

from django.db.models import Min

def select_students(request,cid):
    SD= request.session.get('course_selected')
    # del request.session['course_selected']
    c_obj = Course.objects.get(id=cid)
    user_instance = student_skill_exam_applications.objects.filter(
        assessed_by=request.user.id, skill_name=c_obj.skill_name, exam_id__isnull=True)

    sk_name=c_obj.skill_name
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students')
        for i in selected_students:
            temp=student_skill_exam_applications.objects.get(id=i)
            sid=temp.student.id
            s_temp=Student.objects.get(id=sid)
            temp=student_skill_exam_applications.objects.filter(student=s_temp)

            for i in temp:
                if i.exam_id==cid:
                    return HttpResponseRedirect(f'/examiner/select_students/{cid}')
                
        users=user_instance.filter(id__in=selected_students).update(exam_id=SD,application_status="test_activated")
        msg="Exam Activated"
        txt="Exam enrollment complete for the selected students"
        return render(request, 'examiner/success_page.html',{'message':msg,'text':txt})
    return render(request,'examiner/students_list.html', {'details': user_instance,'SD':SD,'sk_name':sk_name})


def delete_student_application_view(request,id):
    app=student_skill_exam_applications.objects.get(id=id)
    app.delete()
    return HttpResponseRedirect('/examiner/students_list')


def update_passcode(request,id):
    if request.method=='POST':
        pass_code=request.POST.get('new_passcode')
        exam= QMODEL.Course.objects.get(id=id)
        exam.passcode=pass_code
        exam.save()
        return HttpResponseRedirect(f'/examiner/see-student/{id}')




def deactivate_passcode(request,id):
    exam= QMODEL.Course.objects.get(id=id)
    exam.passcode=None
    exam.save()
    return HttpResponseRedirect(f'/examiner/see-student/{id}')




def request_to_add_new_questions(request,cid):
    if request.method=='POST':
        questions_count=request.POST.get('questions_count')
        exam=Course.objects.get(id=cid)
        request.session['exam_name'] = exam.course_name
        request.session['total_questions'] = questions_count
        return HttpResponseRedirect('/examiner/examiner-add-question')
    



