from django.conf.urls import url
from . import views

# urlpatterns = [
#     url(r'allteachers', views.TeacherList.as_view(), name='teacher_list'),
#     url(r'^crs/$', views.CourseList.as_view(), name='course_list'),
#     url(r'^sec/$', views.SectionList.as_view(), name='section_list'),
#     url(r'^sec/(?P<sec>\d+)/$', views.EnrollmentList.as_view(), name='enrollment_list'),
#     url(r'^enrollments/create/$', views.EnrollmentCreate.as_view(), name='enrollment_new'),
#     url(r'^sec/(?P<sec>\d+)/assignments/$', views.AssignmentList.as_view(), name='assignment_list'),
#     url(r'^sec/(?P<sec>\d+)/assignments/create/$', views.AssignmentCreate.as_view(), name='assignment_new'),
#     url(r'^sec/(?P<sec>\d+)/(?P<student>\d+)/grades/$', views.GradeList.as_view(), name='grade_list'),
#     url(r'^allstudents/$', views.StudentList.as_view(), name='student_list')
# ]

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
    # url(r'^crs/$', views.CourseList.as_view(), name='course_list'),
    url(r'^main/$', views.SectionList.as_view(), name='section_list'),
    url(r'^main/(?P<sec>\d+)/$', views.SpecificSection.as_view(), name='section'),
    # url(r'^crs/(?P<crs>\d+)/$', views.SectionList.as_view(), name='section_list'),
    # url(r'^crs/(?P<crs>\d+)/(?P<sec>\d+)/$', views.EnrollmentList.as_view(), name='enrollment_list'),
    url(r'^main/(?P<sec>\d+)/assignments/(?P<pk>\d+)/edit/$', views.AssignmentUpdate.as_view(), name='assignment_edit'),
    url(r'^main/(?P<sec>\d+)/enrollments/add/$', views.EnrollmentCreate.as_view(), name='enrollment_new'),
    url(r'^main/(?P<sec>\d+)/enrollments/(?P<pk>\d+)/delete/$', views.EnrollmentDelete.as_view(), name='enrollment_delete'),
    url(r'^main/(?P<sec>\d+)/assignments/add/$', views.AssignmentCreate.as_view(), name='assignment_new'),
    # url(r'^crs/(?P<crs>\d+)/(?P<sec>\d+)/assignments/$', views.AssignmentList.as_view(), name='assignment_list'),
    # url(r'^crs/(?P<crs>\d+)/(?P<sec>\d+)/assignments/create/$', views.AssignmentCreate.as_view(), name='assignment_new'),
    url(r'^crs/(?P<crs>\d+)/(?P<sec>\d+)/(?P<student>\d+)/grades/$', views.GradeList.as_view(), name='grade_list'),
]