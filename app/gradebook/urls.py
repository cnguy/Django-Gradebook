from django.conf.urls import url
from . import views

urlpatterns = [
    # Home View
    url(r'^$', views.HomePageView.as_view(), name='home'),

    # Authentication Views
    url(r'^login/$', views.auth_v.LoginPageView.as_view(), name='login'),
    url(r'^logout/$', views.auth_v.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.auth_v.RegisterPageView.as_view(), name='register'),
    url(r'^register/teacher/$', views.auth_v.RegisterTeacher.as_view(), name='register_teacher'),
    url(r'^register/student/$', views.auth_v.RegisterStudent.as_view(), name='register_student'),
    url(r'^secret/$', views.home_v.SomeSecretView.as_view(), name='secret'),

    # List Views
    url(r'^allteachers/$', views.lists_v.TeacherList.as_view(), name='teacher_list'),
    url(r'^allstudents/$', views.lists_v.StudentList.as_view(), name='student_list'),
    url(r'^allcourses/$', views.lists_v.CourseList.as_view(), name='course_list'),
    url(r'^staff/$', views.lists_v.SectionList.as_view(), name='section_list'),

    # Section View
    url(r'^staff/(?P<sec>\d+)/$', views.sections_v.SpecificSection.as_view(), name='section'),

    # Announcement Views
    url(r'^staff/(?P<sec>\d+)/announcements/add/$', views.announcements_v.AnnouncementCreate.as_view(), name='announcement_new'),
    url(r'^staff/(?P<sec>\d+)/announcements/(?P<pk>\d+)/edit/$', views.announcements_v.AnnouncementUpdate.as_view(), name='announcement_edit'),
    url(r'^staff/(?P<sec>\d+)/announcements/(?P<pk>\d+)/delete/$', views.announcements_v.AnnouncementDelete.as_view(), name='announcement_delete'),

    # Assignment Views
    url(r'^staff/(?P<sec>\d+)/assignments/add/$', views.assignments_v.AssignmentCreate.as_view(), name='assignment_new'),
    url(r'^staff/(?P<sec>\d+)/assignments/(?P<pk>\d+)/edit/$', views.assignments_v.AssignmentUpdate.as_view(), name='assignment_edit'),
    url(r'^staff/(?P<sec>\d+)/assignments/(?P<pk>\d+)/delete/$', views.assignments_v.AssignmentDelete.as_view(), name='assignment_delete'),
    url(r'^staff/(?P<sec>\d+)/assignments/(?P<asn>\d+)/stats/$', views.assignments_v.AssignmentStats.as_view(), name='assignment_stats'),

    # Enrollment Views
    url(r'^staff/(?P<sec>\d+)/enrollments/add/$', views.enrollments_v.EnrollmentCreate.as_view(), name='enrollment_new'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<pk>\d+)/delete/$', views.enrollments_v.EnrollmentDelete.as_view(), name='enrollment_delete'),

    # Grade Views
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/$', views.grades_v.GradeList.as_view(), name='grade_list'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/add/$', views.grades_v.GradeCreate.as_view(), name='grade_new'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/add/off/(?P<asn>\d+)/$', views.grades_v.GradeCreateOffAssignment.as_view(), name='grade_new_off_assignment'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/(?P<pk>\d+)/edit/(?P<asn>\d+)/$', views.grades_v.GradeUpdate.as_view(), name='grade_edit'),
    url(r'^staff/(?P<sec>\d+)/enrollments/(?P<enr>\d+)/grades/(?P<pk>\d+)/delete/$', views.grades_v.GradeDelete.as_view(), name='grade_delete'),
]