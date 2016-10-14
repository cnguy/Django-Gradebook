from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView

from gradebook.models import Enrollment, Section, Student
from gradebook.views.utils_mixins import SectionIDMixin


class EnrollmentViewMixin(object):
    model = Enrollment

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class EnrollmentCreate(LoginRequiredMixin, EnrollmentViewMixin, SectionIDMixin, CreateView):
    fields = ['section', 'student']

    def get_form(self, form_class=None):
        """
        Only displays the section to prevent enrolling to other sections.
        Only displays students not already enrolled to be in the queryset.
        """
        form = super(EnrollmentCreate, self).get_form(form_class)
        students = Student.objects.all()
        pks_of_students_not_enrolled = []
        for student in students:
            enrollment = Enrollment.objects.filter(student=student, section=self.kwargs['sec']).first()
            if enrollment is None:
                pks_of_students_not_enrolled.append(student.pk)

        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs['sec'])
        form.fields['student'].queryset = Student.objects.filter(pk__in=pks_of_students_not_enrolled)

        return form

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs['sec'])
        return {'section': section}

    def get_context_data(self, **kwargs):
        context = super(EnrollmentCreate, self).get_context_data(**kwargs)
        context['title'] = "Enroll a new student"
        return context


class EnrollmentDelete(LoginRequiredMixin, EnrollmentViewMixin, DeleteView):
    pass