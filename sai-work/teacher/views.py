from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from .models import *
from student.models import *
from quiz.models import *
from django.contrib import messages

#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
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
            return redirect("teachersignup")
        elif(User.objects.filter(username=username).exists()):
            messages.info(request,"user already exists !")
            return redirect("teachersignup")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.mobile = mobile
            user.EmployeeID = EmployeeID
            user.name = full_name
            user.department = department
            user.status=False          
            user.save()
            teacher=Teacher(user=user,emp_id=EmployeeID,name=full_name,status=False,department=department,mobile=mobile,email=email,skill=f_skill)
            teacher.save()
            # teacher_skills=QMODEL.teacher_skills(teacher=teacher,skill_name=f_skill)
            # teacher_skills.save()
            mentor_group = Group.objects.get(name='TEACHER')
            mentor_group.user_set.add(user)
            return redirect('teachersignup')
    return render(request,'teacher/teachersignup.html')



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):

    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    if request.method=='POST':
        exam_name=request.POST['exam_name']
        total_questions=request.POST['total_questions']
        # marks=request.POST['marks']
        course_obj=Course(course_name=exam_name,question_number=total_questions)                        
        course_obj.save()
        request.session['exam_name']=exam_name
        request.session['total_questions']=total_questions

        return HttpResponseRedirect('/teacher/teacher-add-question')
    return render(request,'teacher/teacher_add_exam.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})      


@login_required(login_url='teacherlogin')
def see_student_view(request, pk):
    request.session['course_selected']=pk
    course = get_object_or_404(QMODEL.Course, id=pk)
    students_list = QMODEL.Result.objects.filter(exam=course).values_list("student")
    student_records = student_skill_exam_applications.objects.filter(student__in=students_list)
    combined_data = []
    
    for i in student_records:
            student_object=get_object_or_404(Student,id=i.student.id)
            student_record = student_skill_exam_applications.objects.filter(student=student_object,exam_id=pk).last()
            if student_record:
                results1 = QMODEL.Result.objects.filter(exam=course, student=student_object).last()
                combined_data.append({
                    'student':student_object,
                    'student_name': student_object.name,
                    'branch':student_record.branch,
                    'section':student_record.section,
                    'skill_name':results1.exam.course_name,
                    'marks': results1.marks,
                    'date': results1.date,
                    'status': student_record.application_status
                })

    if request.method=='POST':
        selected_student_ids = request.POST.getlist('selected_students')
        for student_id in selected_student_ids:
            # su=get_object_or_404(User,id=student_id)
            student_object=get_object_or_404(Student,id=student_id)
            results1 = QMODEL.Result.objects.filter(exam=course, student=student_object).last()  # Assuming one result per student per exam

            student_record = student_skill_exam_applications.objects.filter(student=student_object,exam_id=pk).last()
            student_record1 = students_skills.objects.filter(student=student_object,skill_name=student_record.skill_name).last()
            student_record1.test_score=results1.marks
            teacher_obj=get_object_or_404(Teacher,user=request.user)
            student_record1.assessed_by=teacher_obj
            student_record1.skill_status="test_evaluated"
            student_record1.assessed_by=teacher_obj
            student_record1.save()
            student_record1.test_score=results1.marks
            student_record.completed_date=results1.date
            student_record.marks_obtained=results1.marks
            student_record.application_status="completed"
            student_record.save()
            messages.info(request,"Student Record Updated Successfully !")
        
    return render(request, 'teacher/students_course_result.html', {'results': combined_data,'course':course})    




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        course_id = request.POST.get('courseID')
        course=QMODEL.Course.objects.get(id=course_id)
        # course = QMODEL.Course.objects.get(id=course_id)
        if 'total_questions' in request.session:
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
        else:
            question = QMODEL.Question(
                    course=course,
                    question=request.POST.get(f'question_1'),
                    option1=request.POST.get(f'option1_1'),
                    marks=request.POST.get(f'marks_1'),
                    option2=request.POST.get(f'option2_1'),
                    option3=request.POST.get(f'option3_1'),
                    option4=request.POST.get(f'option4_1'),
                    answer=request.POST.get(f'answer_1')
                )
            question.save()
            marks_sum1 = Question.objects.filter(course=course).aggregate(total_marks=Sum('marks'))['total_marks']
            course.total_marks=marks_sum1
            course.save()

        request.session['course_selected']=course.id
        return HttpResponseRedirect('/teacher/select_students')
    else:
        questionForm = QFORM.QuestionForm()
        if "exam_name" in request.session:
            en = request.session.get('exam_name')
            TQ = request.session.get('total_questions')
            question_count = TQ  
            exam_name = en
            del request.session['exam_name']
            course1 = QMODEL.Course.objects.get(course_name=exam_name)
            return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm, 'selected_course': course1, 'question_count': question_count})
        else:
            question_count=1
            courses=QMODEL.Course.objects.all()
            return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm,'question_count': question_count,'courses':courses})





@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')




@login_required(login_url='teacherlogin')
def students_list(request):
    user_instance = student_skill_exam_applications.objects.filter(assessed_by=request.user.id)

    # teacher_instance = Teacher.objects.get(user=user_instance)
    # students_data = Student.objects.filter(TD=teacher_instance).prefetch_related('user')
    return render(request, 'teacher/sample.html', {'details': user_instance})


def select_students(request):
    SD= request.session.get('course_selected')
    # del request.session['course_selected']
    user_instance = student_skill_exam_applications.objects.filter(assessed_by=request.user.id)

    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students')
        users=user_instance.filter(id__in=selected_students).update(exam_id=SD)
        msg="Exam Activated"
        txt="Exam enrollment complete for the selected students"
        return render(request, 'teacher/success_page.html',{'message':msg,'text':txt})
    return render(request,'teacher/students_list.html', {'details': user_instance,'SD':SD})


def delete_student_application_view(request,id):
    app=student_skill_exam_applications.objects.get(id=id)
    app.delete()
    return HttpResponseRedirect('/teacher/students_list')

