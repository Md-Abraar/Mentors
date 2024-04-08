from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path("student-forgot-password", views.student_forgot_password, name="student-forgot-password"),



path("studentlogin",LoginView.as_view(template_name='student/studentlogin.html'), name="studentlogin"),


path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
path('video_feed/', views.video_feed, name='video_feed'), 
path('success/', views.success_page, name='success'),
path('skill_application/', views.skill_application, name='skill_application'),
path('delete_application/<int:pk>', views.delete_application_view, name='delete_application'),
path('student_profile_edit/', views.student_profile_edit, name='student_profile_edit'),

path('student_profile/<str:roll>/', views.student_profile, name='student_profile'),
path('CE_url', views.CE_view, name='CE_url'),
path('PF_url', views.PF_view, name='PF_url'),
path('SWG_url', views.SWG_view, name='SWG_url'),
path('SM_url',  views.SM_view, name='SM_url'),

path('ED_url',  views.ED_view, name='ED_url'),
path('PR_url',  views.PR_view, name='PR_url'),
path('PD_url',  views.PD_view, name='PD_url'),
path('ECST_url',  views.ECST_view, name='ECST_url'),
path('S_remarks_url',  views.S_remarks_view, name='S_remarks_url'),
path('verify_passcode/<str:id>',  views.verify_passcode, name='verify_passcode'),

path('request_to_add_new_skill',  views.request_to_add_new_skill, name='request_to_add_new_skill'),
]