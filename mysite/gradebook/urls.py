from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login/$', views.LoginPageView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterPageView.as_view(), name='register'),
    url(r'^register/teacher/$', views.RegisterTeacher.as_view(), name='register_teacher'),
    url(r'^register/student/$', views.RegisterStudent.as_view(), name='register_student'),
    url(r'^secret/$', views.SomeSecretView.as_view(), name='secret'),
    url(r'^allteachers/$', views.TeacherList.as_view(), name='teacher_list'),
    url(r'^allstudents/$', views.StudentList.as_view(), name='student_list'),
    url(r'^allcourses/$', views.CourseList.as_view(), name='course_list'),
    url(r'^staff/$', views.SectionList.as_view(), name='section_list'),
    url(r'^staff/(?P<sec>\d+)/$', views.SpecificSection.as_view(), name='section'),
    url(r'^staff/(?P<sec>\d+)/announcements/add/$', views.AnnouncementCreate.as_view(), name='announcement_new'),
    url(r'^staff/(?P<sec>\d+)/announcements/(?P<pk>\d+)/edit/$', views.AnnouncementUpdate.as_view(), name='announcement_edit'),
    url(r'^staff/(?P<sec>\d+)/announcements/(?P<pk>\d+)/delete/$', views.AnnouncementDelete.as_view(), name='announcement_delete'),
    url(r'^staff/(?P<sec>\d+)/assignments/(?P<pk>\d+)/edit/$', views.AssignmentUpdate.as_view(), name='assignment_edit'),
    url(r'^staff/(?P<sec>\d+)/enrollments/add/$', views.EnrollmentCreate.as_view(), name='enrollment_new'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<pk>\d+)/delete/$', views.EnrollmentDelete.as_view(), name='enrollment_delete'),
    url(r'^staff/(?P<sec>\d+)/assignments/add/$', views.AssignmentCreate.as_view(), name='assignment_new'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<pk>\d+)/grades/$', views.GradeList.as_view(), name='grade_list'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/add/$', views.GradeCreate.as_view(), name='grade_new'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/add/(?P<pk>\d+)/$', views.GradeCreateOffAssignment.as_view(), name='grade_new_off_assignment'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/(?P<pk>\d+)/edit/$', views.GradeDelete.as_view(), name='grade_edit'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/(?P<pk>\d+)/delete/$', views.GradeDelete.as_view(), name='grade_delete'),
]