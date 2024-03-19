from django.urls import path
from mentor import views
from django.contrib.auth.views import LoginView
from .views import *
urlpatterns = [
    
path('mentorclick', views.mentorclick_view,name="mentorclick"),
path('mentorlogin', LoginView.as_view(template_name='mentor/mentorlogin.html'),name='mentorlogin'),
path('mentorsignup', views.mentor_signup_view,name='mentorsignup'),
path('mentor-dashboard', views.mentor_dashboard_view,name='mentor-dashboard'),
path('students_list/',students_list,name='students_list'),
path("forgot-password", views.mentor_forgot_password, name="forgot-password")

]