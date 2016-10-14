from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import ContextMixin

from gradebook.models import Assignment, Enrollment, Grade
from gradebook.views.utils_mixins import SectionIDMixin
from gradebook.utils import *


class GradeViewMixin(object):
    model = Grade


class GradeFormMixin(ContextMixin):
    fields = ['enrollment', 'assignment', 'points', 'letter_grade', 'date_time_turned_in']

    def get_success_url(self):
        return reverse_lazy(
            'grade_list',
            kwargs={'sec': self.kwargs['sec'], 'enr': self.kwargs['enr']}
        )

    def get_context_data(self, **kwargs):
        context = super(GradeFormMixin, self).get_context_data(**kwargs)
        enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enr'])
        context['enrollment'] = enrollment
        return context


class GradeList(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, ListView):
    def get_queryset(self):
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['enr'], section=self.kwargs['sec'])
        return Grade.objects.filter(enrollment=enrollment)

    def get_context_data(self, **kwargs):
        context = super(GradeList, self).get_context_data(**kwargs)
        enrollment = get_object_or_404(Enrollment, id=self.kwargs['enr'], section=self.kwargs['sec'])
        grades = Grade.objects.filter(enrollment=enrollment)

        context['enrollment'] = enrollment

        # Quick summary of total points earned and total points possible.
        points_earned = {'essay': 0.0, 'test': 0.0, 'quiz': 0.0, 'ps': 0.0, 'hwk': 0.0, 'ec': 0.0}
        points_possible = {'essay': 0, 'test': 0, 'quiz': 0, 'ps': 0, 'hwk': 0, 'ec': 0}

        # Store assignments that we will filter out so that we can display
        # the ungraded assignments in a different fashion.
        graded_assignments = []
        for grade in grades:
            graded_assignments.append(grade.assignment)
            points_earned[grade.assignment.category] += grade.points

        # Grab all the ungraded assignments.
        assignments = Assignment.objects.filter(section=self.kwargs['sec'])
        context['non_graded_assignments'] = []

        for assignment in assignments:
            if assignment not in graded_assignments:
                context['non_graded_assignments'].append(assignment)
            points_possible[assignment.category] += assignment.points_possible

        # Calculate total grade and other related data.
        context['points_earned'] = sum(points_earned.values())
        context['points_possible'] = sum(points_possible.values())
        context['total_grade_percentage'] = to_percent(
            context['points_earned'], context['points_possible']
        ) if context['points_possible'] != 0 else '0%'  # In case if there are no assignments.
        context['final_letter_grade'] = get_letter_grade(float(context['total_grade_percentage'][:-1]))

        # The code chunk below is the logic to display a summary
        # of the grades filtered by categories.
        # For example:
        # Essay | 87%
        # Test  | 50%
        # and so on..
        nothing_msg = "Nothing yet."

        def convert(category):
            """Grabs the readable version of the category."""
            return dict(assignment.CATEGORIES).get(str(category))

        # If the total points possible is 0, then create a tuple containing the nothing message.
        # Otherwise, calculate the percentage.
        context['info_by_category'] = [
            (convert(category), nothing_msg) if points_possible[category] == 0
            else (convert(category), to_percent(points_earned[category], points_possible[category]))
            for category in points_earned
            ]

        return context


class GradeCreate(LoginRequiredMixin, GradeViewMixin, GradeFormMixin, SectionIDMixin, CreateView):
    def get_form(self, form_class=None):
        """
        Only allows assignments created for that section, and only allow
        the user that was selected to be in the field choices..
        """
        form = super(GradeCreate, self).get_form(form_class)
        form.fields['enrollment'].queryset = Enrollment.objects.filter(pk=self.kwargs['enr'])

        # Don't allow assignments that are already graded for the enrolled to show up
        # in the choices.
        grades = Grade.objects.filter(enrollment=self.kwargs['enr'])
        assignments = Assignment.objects.filter(section=self.kwargs['sec'])

        graded_assignments = [grade.assignment for grade in grades]
        pks_of_non_graded_assignments = [
            assignment.pk for assignment in assignments if assignment not in graded_assignments
            ]

        form.fields['assignment'].queryset = Assignment.objects.filter(
            section=self.kwargs['sec'],
            pk__in=pks_of_non_graded_assignments
        )

        return form

    def get_initial(self):
        enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enr'])
        return {'enrollment': enrollment}


class GradeCreateOffAssignment(LoginRequiredMixin, GradeViewMixin, GradeFormMixin, SectionIDMixin, CreateView):
    """
    This custom view is for when the instructor wishes to grade a
    specific assignment on a specific student's page.
    """
    def get_form(self, form_class=None):
        form = super(GradeCreateOffAssignment, self).get_form(form_class)
        form.fields['assignment'].queryset = Assignment.objects.filter(pk=self.kwargs['asn'])
        form.fields['enrollment'].queryset = Enrollment.objects.filter(pk=self.kwargs['enr'])
        return form

    def get_initial(self):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['asn'])
        enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enr'])
        return {'assignment': assignment, 'enrollment': enrollment}


class GradeUpdate(LoginRequiredMixin, GradeViewMixin, GradeFormMixin, SectionIDMixin, UpdateView):
    def get_form(self, form_class=None):
        """
        Only allows assignments created for that section, and only allow
        the user that was selected to be in the field choices..
        """
        form = super(GradeUpdate, self).get_form(form_class)
        form.fields['enrollment'].queryset = Enrollment.objects.filter(pk=self.kwargs['enr'])
        form.fields['assignment'].queryset = Assignment.objects.filter(pk=self.kwargs['asn'])
        return form


class GradeDelete(LoginRequiredMixin, GradeViewMixin, SectionIDMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(
            'grade_list',
            kwargs={'sec': self.kwargs['sec'], 'enr': self.kwargs['enr']}
        )