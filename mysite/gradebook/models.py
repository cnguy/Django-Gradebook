from django.db import models
from django.utils import timezone
from .utils import *


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
    date_time_due = models.DateTimeField(blank=True, null=True)
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

    def __str__(self):
        return super().__str__() + str(self.assignment) + " - " + str(self.letter_grade)

    def get_percent_grade(self):
        return to_percent(self.points, self.assignment.points_possible)

    def get_grade(self):
        return dict(self.ASSIGNMENT_GRADES).get(str(self.letter_grade))


class Announcement(models.Model):
    section = models.ForeignKey(Section)
    headline = models.CharField(max_length=50)
    details = models.TextField(max_length=200)
    date_time_created = models.DateTimeField(default=timezone.now)