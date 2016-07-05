from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Assignment, Course, Enrollment, Grade, Section, Student, Teacher


class HomePageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('secret')
        return super(HomePageView, self).dispatch(request, *args, **kwargs)


class LoginPageView(TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.user.is_authenticated():
                return redirect('/secret/')
            return super(LoginPageView, self).dispatch(request, *args, {'invalid': True})
        else:

            request.session.set_test_cookie()
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/secret/')
            else:
                # TODO: fix invalid message
                return redirect('/login', {'invalid': True})
                # return super(LoginPageView, self).dispatch(request, *args, {'invalid': True})


class LogoutView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterPageView(TemplateView):
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/secret/')
        return super(RegisterPageView, self).dispatch(request, *args, **kwargs)


class RegisterTeacher(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/secret/')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            confirm_password = request.POST.get('confirm_password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password == confirm_password:
                user = User.objects.create_user(
                    username,
                    email,
                    password,
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                teacher = Teacher(user=user)
                teacher.save()

                user = authenticate(
                    username=username,
                    password=password
                )

                login(request, user)
                return redirect('/staff/')
        else:
            return redirect('/register/')


class RegisterStudent(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        username = request.POST.get('username2')
        password = request.POST.get('password2')
        email = request.POST.get('email2')
        confirm_password = request.POST.get('confirm_password2')
        first_name = request.POST.get('first_name2')
        last_name = request.POST.get('last_name2')
        student_id = request.POST.get('student_id')

        if password == confirm_password:
            user = User.objects.create_user(
                username,
                email,
                password,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            student = Student(user=user, student_id=student_id)
            student.save()
            user = authenticate(
                username=username,
                password=password
            )
            return redirect('/student/')
        else:
            return redirect('/register/')


class SomeSecretView(LoginRequiredMixin, TemplateView):
    template_name = 'gradebook/secret.html'
    login_url = '/login/'
    raise_exception = False


class GenericForm(object):
    """
    This is for other Classes to inherit so that they can all have the section id needed
    to link back to the previous section's page. I use this for the Create/Update forms.
    """
    def get_context_data(self, **kwargs):
        context = super(GenericForm, self).get_context_data(**kwargs)
        section_pk = self.kwargs.get('sec')
        context['current_section_pk'] = section_pk
        return context


class StudentList(ListView):
    model = Student
    template_name = 'student_list.html'


class TeacherList(ListView):
    model = Teacher
    template_name = 'teacher_list.html'


class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'


class SectionList(LoginRequiredMixin, ListView):
    model = Section
    login_url = '/login/'
    raise_exception = False

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return Section.objects.filter(teacher=teacher)


class EnrollmentViewMixin(object):
    model = Enrollment

    def get_success_url(self):
        return reverse_lazy('section',
                            kwargs={'sec': self.kwargs['sec']})


class EnrollmentCreate(LoginRequiredMixin, EnrollmentViewMixin, GenericForm, CreateView):
    fields = ['section', 'student']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class EnrollmentDelete(LoginRequiredMixin, EnrollmentViewMixin, DeleteView):
    pass


class AssignmentViewMixin(object):
    model = Assignment

    def get_success_url(self):
        return reverse_lazy('section',
                            kwargs={'sec': self.kwargs['sec']})


class AssignmentList(LoginRequiredMixin, AssignmentViewMixin, ListView):
    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        section = get_object_or_404(Section, teacher=teacher)
        return Assignment.objects.filter(section=section)


class AssignmentCreate(LoginRequiredMixin, AssignmentViewMixin, GenericForm, CreateView):
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class AssignmentUpdate(LoginRequiredMixin, AssignmentViewMixin, GenericForm, UpdateView):
    model = Assignment
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class GradeList(ListView):
    model = Grade

    def get_queryset(self):
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['pk'], section=self.kwargs['sec'])
        return Grade.objects.filter(enrollment=enrollment)

    def get_context_data(self, **kwargs):
        context = super(GradeList, self).get_context_data(**kwargs)
        sum_of_points = 0
        total_points = 0.0
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['pk'], section=self.kwargs['sec'])
        grades = Grade.objects.filter(enrollment=enrollment)

        for grade in grades:
            total_points += grade.assignment.points_possible
            sum_of_points += grade.points

        context['total_grade_percentage'] = "{0:.0f}%".format(sum_of_points/total_points * 100)
        context['total_points'] = total_points
        context['sum_of_points'] = sum_of_points
        context['letter_grade'] = 'A'
        return context

class SpecificSection(LoginRequiredMixin, TemplateView):
    """
    A view to display the description, enrollment, and assignments of a specific section.
    """
    template_name = 'gradebook/section.html'

    def get_context_data(self, **kwargs):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        section = get_object_or_404(Section, teacher=teacher, pk=self.kwargs['sec'])
        context = super(SpecificSection, self).get_context_data(**kwargs)
        context['current_section'] = section
        context['assignments'] = Assignment.objects.filter(section=section).order_by('date_time_created')
        context['enrollments'] = Enrollment.objects.filter(section=section).order_by('student__user__last_name')
        return context