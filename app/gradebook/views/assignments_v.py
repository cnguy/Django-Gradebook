from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView

from gradebook.models import Assignment, Grade, Enrollment, Section
from gradebook.views.utils_mixins import SectionIDMixin
from gradebook.utils import *


class AssignmentViewMixin(object):
    model = Assignment

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class AssignmentFormMixin(object):
    fields = ['section', 'title', 'description', 'category', 'points_possible', 'date_due', 'time_due']


class AssignmentCreate(LoginRequiredMixin, AssignmentViewMixin, AssignmentFormMixin, SectionIDMixin, CreateView):
    def get_form(self, form_class=None):
        form = super(AssignmentCreate, self).get_form(form_class)
        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs['sec'])
        return form

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs['sec'])
        return {'section': section}

    def get_context_data(self, **kwargs):
        context = super(AssignmentCreate, self).get_context_data(**kwargs)
        context['title'] = "Create a new assignment"
        return context


class AssignmentUpdate(LoginRequiredMixin, AssignmentViewMixin, AssignmentFormMixin, SectionIDMixin, UpdateView):
    def get_form(self, form_class=None):
        form = super(AssignmentUpdate, self).get_form(form_class)
        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs['sec'])
        return form

    def get_context_data(self, **kwargs):
        context = super(AssignmentUpdate, self).get_context_data(**kwargs)
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        context['title'] = "Editing: {assignment}".format(assignment=assignment)
        return context


class AssignmentDelete(LoginRequiredMixin, AssignmentViewMixin, DeleteView):
    pass  # TODO;


class AssignmentStats(LoginRequiredMixin, SectionIDMixin, TemplateView):
    template_name = 'gradebook/assignment_stats.html'

    def get_context_data(self, **kwargs):
        context = super(AssignmentStats, self).get_context_data(**kwargs)
        section = get_object_or_404(Section, pk=self.kwargs['sec'])
        assignment = get_object_or_404(Assignment, pk=self.kwargs['asn'])
        grades = Grade.objects.filter(assignment=assignment)
        enrollments = Enrollment.objects.filter(section=section)

        context['current_section'] = section
        context['assignment'] = assignment
        grades = grades.order_by('-points') # Sort from highest points to lowest.
        context['assignment_summary'] = {
            'A+': 0, 'A': 0, 'A-': 0,
            'B+': 0, 'B': 0, 'B-': 0,
            'C+': 0, 'C': 0, 'C-': 0,
            'D+': 0, 'D': 0, 'D-': 0,
            'F': 0, 'N': 0
        }

        context['grades_with_colors'] = []
        # The sum of points earned and possible for all students.
        # This is used to determine the average grade.
        points_earned_btw_all_students = 0.0
        points_possible_btw_all_students = 0
        num_of_late_assignments = 0

        for grade in grades:
            context['assignment_summary'][grade.letter_grade.upper()] += 1
            points_earned_btw_all_students += grade.points
            points_possible_btw_all_students += assignment.points_possible
            if not(grade.on_time()):
                num_of_late_assignments += 1

            # grade logic
            color = ""
            grade_of_current = grade.get_grade()[0:1]
            if grade_of_current == "A":
                color = "#a5d6a7"
            elif grade_of_current == "B":
                color ="#b3e5fc"
            elif grade_of_current == "C":
                color = "#f0f4c3"
            else:
                color = "#ffcdd2"
            context['grades_with_colors'].append((grade, color))

        context['average_grade'] = to_percent(
            points_earned_btw_all_students,
            points_possible_btw_all_students
        ) if points_possible_btw_all_students != 0 else 'N'

        # [N] is the number of non-graded assignments.
        context['assignment_summary']['N'] = len(enrollments) - sum(context['assignment_summary'].values())
        max_points = grades.aggregate(Max('points'))['points__max'] if len(grades) != 0 else 0
        context['highest_grade'] = to_percent(
            max_points,
            assignment.points_possible
        ) if points_possible_btw_all_students != 0 else 'N'
        context['num_of_late_assignments'] = num_of_late_assignments

        enrollments_graded = [grade.enrollment for grade in grades]

        context['enrollments_to_be_graded'] = [
            enrollment for enrollment in enrollments if enrollment not in enrollments_graded
            ]

        return context