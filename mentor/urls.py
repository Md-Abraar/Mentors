from django.urls import path
from mentor import views
from django.contrib.auth.views import LoginView
from .views import *
from student import views as views_s

urlpatterns = [
path("edit_achievement/<str:id>",edit_achievement_view,name="edit_achievement"),

path('mentorclick', views.mentorclick_view,name="mentorclick"),
path('mentorlogin', LoginView.as_view(template_name='mentor/mentorlogin.html'),name='mentorlogin'),
path('mentorsignup', views.mentor_signup_view,name='mentorsignup'),
path('mentor-dashboard', views.mentor_dashboard_view,name='mentor-dashboard'),
path('students_list/',students_list,name='students_list'),
path("mentor-forgot-password", views.mentor_forgot_password, name="mentor-forgot-password"),





path('student_application_reject/<int:pk>/', student_application_reject_view, name='student_application_reject'),



path('students_skill_applications', students_skill_applications,name='students_skill_applications'),
# path('students_list/',students_list,name='students_list'),
path('student_application_approve/<int:pk>', student_application_approve_view,name='student_application_approve'),
path('students_scores', students_scores_view,name='students_scores'),

path('update_student_skill/<int:id>', update_student_skill_view,name='update_student_skill'),
path('student_profile/<str:roll>/', student_profile, name='student_profile'),

# path('student_profile_edit/', views_s.student_profile_edit, name='student_profile_edit'),
path('student_profile_edit_c/<str:roll>', student_profile_edit_c, name='student_profile_edit_c'),

path('student_profile_edit/', student_profile_edit, name='student_profile_edit'),


path("/delete_achievement/<str:oid>/<str:sid>", delete_achievement_view, name="delete_achievement"),

path('achievements_url', achievements_view, name='achievements_url'),
path('cert_url', cert_view, name='cert_url'),
path('EC_url', EC_view, name='EC_url'),
path('ATT_url', ATT_view, name='ATT_url'),
path('bac_url', bac_view, name='bac_url'),
path('remarks_url', remarks_view, name='remarks_url'),
path('intern_url', intern_view, name='intern_url'),
path('pm_url', pm_view, name='pm_url'),


]