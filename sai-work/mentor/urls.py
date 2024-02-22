from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView
from .views import *
urlpatterns = [

path('mentorclick',mentorclick_view,name="mentorclick"),
path('mentorsignup', mentor_signup_view,name='mentorsignup'),
path('mentorlogin', LoginView.as_view(template_name='mentor/mentorlogin.html'),name='mentorlogin'),
path('students_list', students_list,name='students_list'),
path('mentor-dashboard',mentor_dashboard_view,name='mentor-dashboard'),
path('student_application_reject/<int:pk>/', student_application_reject_view, name='student_application_reject'),


path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
# path('see-question/<int:pk>', views.see_question_view,name='see-question'),
# path('see-student/<int:pk>', views.see_student_view,name='see-student'),

path('students_skill_applications', students_skill_applications,name='students_skill_applications'),
# path('students_list/',students_list,name='students_list'),
path('student_application_approve/<int:pk>', student_application_approve_view,name='student_application_approve'),
path('students_scores', students_scores_view,name='students_scores'),

path('update_student_skill/<int:id>', update_student_skill_view,name='update_student_skill'),


]