from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from gradebook.models import Announcement, Assignment, Enrollment, Grade, Section, Teacher
from gradebook.utils import *


class SpecificSection(LoginRequiredMixin, TemplateView):
    """
    A custom view to display the description, announcements, assignments,
    and enrollments of a specific section.
    """
    template_name = 'gradebook/section.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificSection, self).get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, user=self.request.user)
        section = get_object_or_404(Section, teacher=teacher, pk=self.kwargs['sec'])

        context['current_section'] = section
        context['announcements'] = Announcement.objects.filter(section=section).order_by('date_time_created')
        context['assignments'] = Assignment.objects.filter(section=section).order_by('date_due')
        context['enrollments'] = Enrollment.objects.filter(section=section).order_by('student__user__last_name')
        context['enrollments_and_grades'] = []

        # Number of a's, number of b's, etc.
        num_of_letter_grades = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

        # Calculate total letter grades for each enrollment.
        for enrollment in context['enrollments']:
            grades = Grade.objects.filter(enrollment=enrollment)
            points_earned = 0.0
            points_possible = 0

            for grade in grades:
                points_earned += grade.points

            for assignment in context['assignments']:
                points_possible += assignment.points_possible

            percentage = to_percent(points_earned, points_possible)[:-1] if points_possible != 0 else 0
            float_percentage = float(percentage)
            letter_grade = get_letter_grade(float_percentage)
            num_of_letter_grades[letter_grade] += 1
            # If # of graded assignments != # of assignments, student has ungraded assignments.
            needs_grading = len(grades) != len(context['assignments'])

            context['enrollments_and_grades'].append((enrollment, letter_grade, needs_grading))

        context['grade_summary'] = [
            (grade, num_of_letter_grades[grade]) for grade in sorted(num_of_letter_grades.keys())
            ]

        return context