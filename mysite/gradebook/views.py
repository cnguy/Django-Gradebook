from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Announcement, Assignment, Course, Enrollment, Grade, Section, Student, Teacher


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


class SectionIDMixin(object):
    """
    This is for other Classes to inherit so that they can all have the section id needed
    to link back to the previous section's page. I use this for the Create/Update/List forms.
    """
    def get_context_data(self, **kwargs):
        context = super(SectionIDMixin, self).get_context_data(**kwargs)
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


class EnrollmentCreate(LoginRequiredMixin, EnrollmentViewMixin, SectionIDMixin, CreateView):
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


class AssignmentCreate(LoginRequiredMixin, AssignmentViewMixin, SectionIDMixin, CreateView):
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class AssignmentUpdate(LoginRequiredMixin, AssignmentViewMixin, SectionIDMixin, UpdateView):
    model = Assignment
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return {
            'section': section
        }


class GradeList(SectionIDMixin, ListView):
    model = Grade

    def get_queryset(self):
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['pk'], section=self.kwargs['sec'])
        return Grade.objects.filter(enrollment=enrollment)

    def get_context_data(self, **kwargs):
        context = super(GradeList, self).get_context_data(**kwargs)

        sum_of_points = 0
        total_points = 0.0

        enrollment = get_object_or_404(Enrollment, id=self.kwargs['pk'], section=self.kwargs['sec'])
        context['enrollment'] = enrollment

        grades = Grade.objects.filter(enrollment=enrollment)

        # Quick Summary of Data by Category
        essay_total_points = 0
        test_total_points = 0
        quiz_total_points = 0
        ps_total_points = 0
        hwk_total_points = 0

        essay_sum_of_points = 0.0
        test_sum_of_points = 0.0
        quiz_sum_of_points = 0.0
        ps_sum_of_points = 0.0
        hwk_sum_of_points = 0.0
        ec_sum_of_points = 0.0

        for grade in grades:
            total_points += grade.assignment.points_possible
            sum_of_points += grade.points

            # Get category-specific information.
            if grade.assignment.category == 'essay':
                essay_total_points += grade.assignment.points_possible
                essay_sum_of_points += grade.points
            elif grade.assignment.category == 'test':
                test_total_points += grade.assignment.points_possible
                test_sum_of_points += grade.points
            elif grade.assignment.category == 'quiz':
                quiz_total_points += grade.assignment.points_possible
                quiz_sum_of_points += grade.points
            elif grade.assignment.category == 'ps':
                ps_total_points += grade.assignment.points_possible
                ps_sum_of_points += grade.points
            elif grade.assignment.category == 'hwk':
                hwk_total_points += grade.assignment.points_possible
                hwk_sum_of_points += grade.points
            elif grade.assignment.category == 'ec':
                ec_sum_of_points += grade.points

        context['total_grade_percentage'] = "{0:.0f}%".format(sum_of_points/total_points * 100)
        context['total_points'] = total_points
        context['sum_of_points'] = sum_of_points
        context['letter_grade'] = 'A'

        # The code chunk below is the logic to display a summary
        # of the grades filtered by categories.
            # For example:
            # Essay | 87%
            # Test  | 50%
            # and so on..
        categories = ['Essay', 'Test', 'Quiz', 'Problem Set', 'Homework', 'Extra Credit']
        nothing = "Nothing yet."
        if essay_total_points == 0:
            essay_info = (categories[0], nothing)
        else:
            essay_info = (
                categories[0],
                "{0:.0f}%".format(essay_sum_of_points / essay_total_points * 100)
            )

        if test_total_points == 0:
            test_info = (categories[1], nothing)
        else:
            test_info = (
                categories[1],
                "{0:.0f}%".format(test_sum_of_points / test_total_points * 100)
            )

        if quiz_total_points == 0:
            quiz_info = (categories[2], nothing)
        else:
            quiz_info = (
                categories[2],
                "{0:.0f}%".format(quiz_sum_of_points / quiz_total_points * 100)
            )

        if ps_total_points == 0:
            ps_info = (categories[3], nothing)
        else:
            ps_info = (
                categories[3],
                "{0:.0f}%".format(ps_sum_of_points / ps_total_points * 100)
            )

        if hwk_total_points == 0:
            hwk_info = (categories[4], nothing)
        else:
            hwk_info = (
                categories[4],
                "{0:.0f}%".format(hwk_sum_of_points / hwk_total_points * 100)
            )

        if ec_sum_of_points == 0:
            ec_info = (categories[5], nothing)
        else:
            ec_info = (
                categories[5],
                ec_sum_of_points
            )

        context['categories'] = [essay_info, test_info, quiz_info, ps_info, hwk_info, ec_info]

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
        context['announcements'] = Announcement.objects.filter(section=section).order_by('date_time_created')
        context['assignments'] = Assignment.objects.filter(section=section).order_by('date_time_created')
        context['enrollments'] = Enrollment.objects.filter(section=section).order_by('student__user__last_name')
        return context