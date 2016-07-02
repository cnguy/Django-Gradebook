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
        if request.user.is_authenticated():
            return redirect('/secret/')
        request.session.set_test_cookie()
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/secret/')
        else:
            # TODO: fix invalid message
            return super(LoginPageView, self).dispatch(request, *args, {'invalid': True})


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
            user = authenticate(
                username=username,
                password=password
            )
            teacher = Teacher(user=user)
            teacher.save()
            return redirect('/main/')
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

        if password == confirm_password:
            user = User.objects.create_user(
                username,
                email,
                password,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = authenticate(
                username=username,
                password=password
            )
            student = Student(user=user)
            student.save()
            return redirect('/secret/')
        else:
            return redirect('/register/')


class SomeSecretView(LoginRequiredMixin, TemplateView):
    template_name = 'gradebook/secret.html'
    login_url = '/login/'
    raise_exception = False


class TeacherList(ListView):
    model = Teacher


class CourseList(ListView):
    model = Course


class SectionList(LoginRequiredMixin, ListView):
    model = Section
    login_url = '/login/'
    raise_exception = False

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return Section.objects.filter(teacher=teacher)

    #
    # def get_queryset(self):
    #     course = get_object_or_404(Course, id=self.kwargs['crs'])
    #     return Section.objects.filter(course=course)


# class EnrollmentList(ListView):
#     model = Enrollment
#
#     def get_queryset(self):
#         section = get_object_or_404(Section, id=self.kwargs['sec'])
#         return Enrollment.objects.filter(section=section)


class EnrollmentViewMixin(object):
    model = Enrollment

    def get_success_url(self):
        return reverse_lazy('section',
                            kwargs={'sec': self.kwargs['sec']})


class EnrollmentCreate(LoginRequiredMixin, EnrollmentViewMixin, CreateView):
    #model = Enrollment
    #success_url = reverse_lazy('enrollment_list')

    fields = ['section', 'student']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }

    def form_valid(self, form):
        if form.instance not in Enrollment.objects.all():
            return super(EnrollmentCreate, self).form_valid(form)
        else: # TODO: FIX
            return super(EnrollmentCreate, self).form_invalid(form)
            #return reverse_lazy('enrollment_new',
                                # kwargs={'sec': self.kwargs['sec']})


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


class AssignmentCreate(LoginRequiredMixin, AssignmentViewMixin, CreateView):
    fields = ['section', 'title', 'description', 'category', 'date_created', 'date_due', 'is_complete']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class AssignmentUpdate(LoginRequiredMixin, AssignmentViewMixin, UpdateView):
    model = Assignment
    fields = ['section', 'title', 'description', 'category', 'date_created', 'date_due', 'is_complete']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class GradeList(ListView):
    model = Grade

    def get_queryset(self):
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['student'])
        return Grade.objects.filter(enrollment=enrollment)


class StudentList(ListView):
    model = Student


class SpecificSection(LoginRequiredMixin, TemplateView):
    template_name = 'gradebook/section.html'

    def get_context_data(self, **kwargs):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        section = get_object_or_404(Section, teacher=teacher)
        context = super(SpecificSection, self).get_context_data(**kwargs)
        context['current_section'] = section
        context['assignments'] = Assignment.objects.filter(section=section).order_by('date_created')
        context['enrollments'] = Enrollment.objects.filter(section=section).order_by('student__user__last_name')
        return context