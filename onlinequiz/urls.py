from django.urls import path,include
from django.contrib import admin
from management import views
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path("mentor/", include('mentor.urls')),
    


    path('',views.home_view,name='home'),
    path('logout', LogoutView.as_view(template_name='management/logout.html'),name='logout'),
    path('aboutus/', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    # path('get_skills', views.get_skills,name='get_skills'),
    
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='management/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('update-is-active/<str:empid>', views.update_is_active, name="update-is-active"),
    path('update-status/<str:empid>', views.update_status, name="update-status"),

    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),
    path('approve-mentor/<int:pk>', views.approve_mentor_view,name='approve-mentor1'),
    path('reject-mentor/<int:pk>', views.reject_mentor_view,name='reject-mentor1'),
    path('approve-examiner/<int:pk>', views.approve_examiner,name='approve-examiner'),
    path('reject-examiner/<int:pk>', views.reject_examiner,name='reject-examiner'),
    path('reject-skill/<str:name>', views.reject_skill,name='reject-skill'),
    path('accept-skill/<str:name>', views.accept_skill,name='accept-skill'),


    
    path('get_dashboard_data/',views.get_dashboard_data,name="get_dashboard_data"),
    path('admin-student', views.admin_student_view,name='admin-student'),
    path("download-sample", views.download_sample, name="download-sample"),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),

    path('admin-skill', views.admin_skill_view,name='admin-skill'),
    path('admin-add-course', views.admin_add_course_view,name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view,name='delete-course'),
    path("admin-add-skill", views.admin_add_skill, name="admin-add-skill"),
    path("admin-edit-skill/<str:skill_name>", views.admin_edit_skill, name="admin-edit-skill"),
    path("get_domains", views.get_domains , name="get_domains"),

    path("mentor-assign/<str:empid>", views.mentor_assign, name="mentor-assign"),
    path("mentor-details/<str:empid>", views.mentor_details, name="mentor-details"),

    path('examiner',views.examiner, name='examiner'),
    path('examiner-details/<str:empid>',views.examiner_details, name='examiner-details'),


    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),

    path('leaderboard', views.leaderboard, name="leaderboard"),
    path("email-verification", views.email_verification, name="email-verification"),
    path("verify-otp", views.verify_otp, name="verify-otp")


]
