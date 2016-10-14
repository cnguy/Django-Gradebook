from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from gradebook.models import Student, Teacher
from gradebook.forms import LoginForm
from django.core.exceptions import ObjectDoesNotExist


class LoginPageView(FormView):
    # TODO: FIX CSRF
    template_name = 'login.html'
    form_class = LoginForm
    success_url = ''

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
    # TODO: FIX CSRF
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