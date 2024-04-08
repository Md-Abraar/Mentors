from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import *
from management import views as m_views
urlpatterns = [
path('examinerclick', views.examinerclick_view),
path('examinersignup', views.examiner_signup_view,name='examinersignup'),
path("examiner-forgot-password", views.examiner_forgot_password, name="examiner-forgot-password"),
path('examiner-dashboard', views.examiner_dashboard_view,name='examiner-dashboard'),
path('examiner-exam', views.examiner_exam_view,name='examiner-exam'),
path('examiner-add-exam', views.examiner_add_exam_view,name='examiner-add-exam'),
path('examiner-view-exam', views.examiner_view_exam_view,name='examiner-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('examiner-question', views.examiner_question_view,name='examiner-question'),
path('examiner-add-question', views.examiner_add_question_view,name='examiner-add-question'),
# path('examiner-view-question', views.examiner_view_question_view,name='examiner-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('see-student/<int:pk>', views.see_student_view,name='see-student'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
path('students_list/',students_list,name='students_list'),

path('select_students/<str:cid>',select_students,name='select_students'),

path('delete-student-application/<int:id>',delete_student_application_view,name='delete-student-application'),
path('examinerlogin', LoginView.as_view(template_name='examiner/examinerlogin.html'),name='examinerlogin'),
path('update_passcode/<str:id>', update_passcode,name='update_passcode'),
path('deactivate_passcode/<str:id>', deactivate_passcode,name='deactivate_passcode'),
path('request_to_add_new_questions/<str:cid>', request_to_add_new_questions,name='request_to_add_new_questions'),

]

