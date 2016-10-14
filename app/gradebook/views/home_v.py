from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from gradebook.models import Student, Teacher


class HomePageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            url = ''
            try:
                teacher = Teacher.objects.filter(user=request.user)
                if teacher is not None:
                    url = 'section_list'
            except Teacher.DoesNotExist:  # Not sure how to do exceptions properly yet.
                raise ObjectDoesNotExist
            try:
                student = Student.objects.filter(user=request.user)
                if student is not None:
                    url = 'secret'
            except:
                raise ObjectDoesNotExist
            return redirect(url)
        return super(HomePageView, self).dispatch(request, *args, **kwargs)


class SomeSecretView(LoginRequiredMixin, TemplateView):
    template_name = 'gradebook/secret.html'
    login_url = '/login/'
    raise_exception = False