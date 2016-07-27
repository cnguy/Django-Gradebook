from django.db import models
from django.utils import timezone
from .utils import *
import datetime
import pytz


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    SUBJECTS = {
        ('english', "ENGLISH"),
        ('math', "MATH")
    }

    subject = models.CharField(choices=SUBJECTS, max_length=20)

    def __str__(self):
        return self.title + ": " + self.description


class Person(models.Model):
    user = models.OneToOneField('auth.User')

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name


class Teacher(Person):
    def __str__(self):
        return "Teacher: " + super().__str__()


class Section(models.Model):
    teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)

    section_id = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.course.title + ": Section " + str(self.section_id)


class Student(Person):
    student_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.student_id) + " - " + super().__str__()


class Assignment(models.Model):
    section = models.ForeignKey(Section)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_time_created = models.DateTimeField(default=timezone.now)

    # Separated because materialize.css does not play well with DateTime form fields.
    # date_time_created uses timezone.now, so it's okay for that to stay as it is.
    date_due = models.DateField(default=datetime.date.today)
    time_due = models.TimeField(default=datetime.time)

    points_possible = models.IntegerField()

    CATEGORIES = {
        ('essay', "Essay"),
        ('test', "Test"),
        ('quiz', "Quiz"),
        ('ps', "Problem Set"),
        ('hwk', "Homework"),
        ('ec', "Extra Credit")
    }

    category = models.CharField(choices=CATEGORIES, max_length=20)

    def __str__(self):
        return "[" + self.get_assignment_category() + "] " + str(self.title) + ": " + str(self.description)

    def get_assignment_category(self):
        return dict(self.CATEGORIES).get(str(self.category))


class Enrollment(models.Model):
    section = models.ForeignKey(Section)
    student = models.ForeignKey(Student)

    def __str__(self):
        return str(self.section) + ": " + str(self.student)


class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    assignment = models.ForeignKey(Assignment)

    ASSIGNMENT_GRADES = (
        ('a+', "A+"), ('a', "A"), ('a-', "A-"),
        ('b+', "B+"), ('b', "B"), ('b-', "B-"),
        ('c+', "C+"), ('c', "C"), ('c-', "C-"),
        ('d+', "D+"), ('d', "D"), ('d-', "D-"),
        ('f', "F")
    )

    points = models.FloatField()
    letter_grade = models.CharField(choices=ASSIGNMENT_GRADES, max_length=3, default="A+")
    date_time_turned_in = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return super().__str__() + str(self.assignment) + " - " + str(self.letter_grade)

    def get_percent_grade(self):
        return to_percent(self.points, self.assignment.points_possible)

    def get_grade(self):
        return dict(self.ASSIGNMENT_GRADES).get(str(self.letter_grade))

    def on_time(self):
        """Multiple function calls when templating, but it's to make everything simpler."""
        naive_assignment_dt_due = datetime.datetime.combine(self.assignment.date_due, self.assignment.time_due)
        local_timezone = pytz.timezone("America/Los_Angeles")
        local_assignment_dt_due = local_timezone.localize(naive_assignment_dt_due, is_dst=None)
        utc_dt = local_assignment_dt_due.astimezone(pytz.utc)
        return self.date_time_turned_in <= utc_dt

class Announcement(models.Model):
    section = models.ForeignKey(Section)
    headline = models.CharField(max_length=50)
    details = models.TextField(max_length=200)
    date_time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "[{section}] {title}".format(section=self.section, title=self.headline)