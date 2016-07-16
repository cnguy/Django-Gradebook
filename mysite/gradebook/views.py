from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView, FormView, TemplateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Announcement, Assignment, Course, Enrollment, Grade, Section, Student, Teacher
from .forms import LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from .utils import *

# TODO: Clean up this drug-induced code.


class HomePageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                teacher = Teacher.objects.filter(user=request.user)
                url = 'section_list'
            except Teacher.DoesNotExist:  # Not sure how to do exceptions properly yet.
                raise ObjectDoesNotExist
            try:
                student = Student.objects.filter(user=request.user)
                url = 'secret'
            except:
                raise ObjectDoesNotExist
            return redirect(url)
        return super(HomePageView, self).dispatch(request, *args, **kwargs)


class LoginPageView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = ''  # filler

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = request.user
            if user.is_authenticated():
                url = ''
                try:
                    teacher = Teacher.objects.filter(user=user).first()
                    if teacher is not None:
                        url = 'section_list'
                except Teacher.DoesNotExist:
                    pass
                try:
                    student = Student.objects.filter(user=user).first()
                    if student is not None:
                        url = 'secret'
                except Student.DoesNotExist:
                    pass

                return redirect(url)
            return super(LoginPageView, self).dispatch(request, *args, **kwargs)
        else:
            # user = form.login()

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                url = ''
                try:
                    teacher = Teacher.objects.filter(user=user).first()
                    if teacher is not None:
                        url = 'section_list'
                except Teacher.DoesNotExist:
                    pass
                try:
                    student = Student.objects.filter(user=user).first()
                    if student is not None:
                        url = 'secret'
                except Student.DoesNotExist:
                    pass

                return redirect(url)
            else:
                return super(LoginPageView, self).dispatch(request, *args, **kwargs)
                # return super(LoginPageView, self).dispatch(request, *args, {'invalid': True})

    def form_valid(self, form):
        return super(LoginPageView, self).form_valid(form)


class LogoutView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterPageView(TemplateView):
    template_name = 'register.html'
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            url = ''
            try:
                teacher = Teacher.objects.filter(user=user).first()
                if teacher is not None:
                    url = 'section_list'
            except Teacher.DoesNotExist:
                pass
            try:
                student = Student.objects.filter(user=user).first()
                if student is not None:
                    url = 'secret'
            except Student.DoesNotExist:
                pass

            return redirect(url)
        return super(RegisterPageView, self).dispatch(request, *args, **kwargs)


class RegisterTeacher(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/staff/')

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

            login(request, user)

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

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        context['title'] = "All Students"
        return context


class TeacherList(ListView):
    model = Teacher
    template_name = 'teacher_list.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherList, self).get_context_data(**kwargs)
        context['title'] = "All Teachers"
        return context


class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'

    def get_context_data(self, **kwargs):
        context = super(CourseList, self).get_context_data(**kwargs)
        context['title'] = "All Courses"
        return context


class SectionList(LoginRequiredMixin, ListView):
    model = Section
    login_url = '/login/'
    raise_exception = False

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return Section.objects.filter(teacher=teacher)


class AnnouncementViewMixin(object):
    model = Announcement

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class AnnouncementCreate(LoginRequiredMixin, AnnouncementViewMixin, SectionIDMixin, CreateView):
    fields = ['section', 'headline', 'details', 'date_time_created']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return { 'section': section }


class AnnouncementUpdate(LoginRequiredMixin, AnnouncementViewMixin, SectionIDMixin, UpdateView):
    fields = ['section', 'headline', 'details', 'date_time_created']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return { 'section': section }


class AnnouncementDelete(LoginRequiredMixin, AnnouncementViewMixin, DeleteView):
    pass


class EnrollmentViewMixin(object):
    model = Enrollment

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class EnrollmentCreate(LoginRequiredMixin, EnrollmentViewMixin, SectionIDMixin, CreateView):
    fields = ['section', 'student']

    def get_form(self, form_class):
        """
        Only displays the section to prevent enrolling to other sections.
        Only displays students not already enrolled to be in the queryset.
        """
        form = super(CreateView, self).get_form(form_class)
        students = Student.objects.all()

        for student in students:
            enrollment = Enrollment.objects.filter(student=student).first()
            if enrollment is None:
                form.fields['student'].queryset.append(student)

        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs.get('sec'))
        return form

    def get_initial(self):
        """
        The correct section is already selected.
        """
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return { 'section': section }


class EnrollmentDelete(LoginRequiredMixin, EnrollmentViewMixin, DeleteView):
    pass


class AssignmentViewMixin(object):
    model = Assignment

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class AssignmentCreate(LoginRequiredMixin, AssignmentViewMixin, SectionIDMixin, CreateView):
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return { 'section': section }


class AssignmentUpdate(LoginRequiredMixin, AssignmentViewMixin, SectionIDMixin, UpdateView):
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_time_created', 'date_time_due']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('sec'))
        return { 'section': section }


class GradeViewMixin(object):
    model = Grade

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class GradeList(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, ListView):
    # TODO: drug-induced, FIX
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

        # Store assignments that we will filter out
        # so that we can display the ungraded assignments
        # in a different fashion.
        grades_container = []

        for grade in grades:
            total_points += grade.assignment.points_possible
            sum_of_points += grade.points
            grades_container.append(grade.assignment)

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

        # Filter out assignments.
        assignments = Assignment.objects.filter(section=self.kwargs['sec'])
        context['ungraded_assignments'] = []

        for assignment in assignments:
            if assignment not in grades_container:
                context['ungraded_assignments'].append(assignment)

        # Calculate total grade and associated data.
        if total_points != 0:
            context['total_grade_percentage'] = to_percent(sum_of_points, total_points)
        context['total_points'] = total_points
        context['sum_of_points'] = sum_of_points
        context['letter_grade'] = 'A'

        # The code chunk below is the logic to display a summary
        # of the grades filtered by categories.
        # For example:
        # Essay | 87%
        # Test  | 50%
        # and so on..
        categories = ['Essay', 'Test', 'Quiz', 'Problem Set', 'Homework', 'Extra Credit', 'Total']
        nothing_msg = "Nothing yet."

        essay_info = (categories[0], nothing_msg) if essay_total_points == 0 else \
            (categories[0], to_percent(essay_sum_of_points, essay_total_points))
        test_info = (categories[1], nothing_msg) if test_total_points == 0 else \
            (categories[1], to_percent(test_sum_of_points, test_total_points))
        quiz_info = (categories[2], nothing_msg) if quiz_total_points == 0 else \
            (categories[2], to_percent(quiz_sum_of_points, quiz_total_points))
        ps_info = (categories[3], nothing_msg) if ps_total_points == 0 else \
            (categories[3], to_percent(ps_sum_of_points, ps_total_points))
        hwk_info = (categories[4], nothing_msg) if hwk_total_points == 0 else \
            (categories[4], to_percent(hwk_sum_of_points, hwk_total_points))
        ec_info = (categories[5], nothing_msg) if ec_sum_of_points == 0 else \
            (categories[5], ec_sum_of_points)

        total_info = (categories[6], nothing_msg) if total_points == 0 else \
            (categories[6], context['total_grade_percentage'])

        context['categories'] = [
            essay_info, test_info, quiz_info,
            ps_info, hwk_info,
            ec_info,
            total_info
        ]

        return context


class GradeCreate(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, CreateView):
    fields = ['enrollment', 'assignment', 'points', 'grade']

    def get_form(self, form_class):
        """
        Only allows assignments created for that section, and only allow
        the user that was selected to be in the field choices..
        """
        form = super(CreateView, self).get_form(form_class)
        form.fields['enrollment'].queryset = Enrollment.objects.filter(pk=self.kwargs.get('pk'))
        form.fields['assignment'].queryset = Assignment.objects.filter(section=self.kwargs.get('sec'))
        return form

    def get_initial(self):
        enrollment = get_object_or_404(Enrollment, pk=self.kwargs.get('pk'))
        return { 'enrollment': enrollment }


class GradeEdit(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, UpdateView):
    fields = ['enrollment', 'assignment', 'points', 'grade']

    def get_initial(self):
        enrollment = get_object_or_404(Section, pk=self.kwargs.get('pk'))
        return { 'enrollment': enrollment }


class GradeDelete(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, DeleteView):
    pass


class SpecificSection(LoginRequiredMixin, TemplateView):
    """
    A custom view to display the description, annoucenments, assignments,
    and enrollments of a specific section.
    """
    # TODO: drug-induced, FIX

    template_name = 'gradebook/section.html'

    def get_context_data(self, **kwargs):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        section = get_object_or_404(Section, teacher=teacher, pk=self.kwargs['sec'])
        context = super(SpecificSection, self).get_context_data(**kwargs)
        context['current_section'] = section
        context['announcements'] = Announcement.objects.filter(section=section).order_by('date_time_created')
        context['assignments'] = Assignment.objects.filter(section=section).order_by('date_time_created')
        context['enrollments'] = Enrollment.objects.filter(section=section).order_by('student__user__last_name')
        enrollments_and_grades = []

        # Number of a's, number of b's, etc.
        a = 0
        b = 0
        c = 0
        d = 0
        f = 0

        # Calculate current letter grades.
        for enrollment in context['enrollments']:
            grades = Grade.objects.filter(enrollment=enrollment)
            points = 0.0
            possible_points = 0

            for grade in grades:
                points += grade.points
                possible_points += grade.assignment.points_possible

            percentage = to_percent(points, possible_points) if possible_points != 0 else 0
            float_percentage = float(percentage)
            letter_grade = 'NULL'

            if float_percentage > 90:
                letter_grade = 'A'
                a += 1
            elif 80.0 <= float_percentage < 90.0:
                letter_grade = 'B'
                b += 1
            elif 70.0 <= float_percentage < 80.0:
                letter_grade = 'C'
                c += 1
            elif 60.0 <= float_percentage < 70.0:
                letter_grade = 'D'
                d += 1
            elif float_percentage < 60.0:
                letter_grade = 'F'
                f += 1

            needs_grading = True if len(grades) != len(context['assignments']) else False

            enrollments_and_grades.append((enrollment, letter_grade, needs_grading))

        context['a'] = a
        context['b'] = b
        context['c'] = c
        context['d'] = d
        context['f'] = f
        context['enrollment_and_grades'] = enrollments_and_grades
        context['grade_summary'] = [('A', a), ('B', b), ('C', c), ('D', d), ('F', f)]
        return context
