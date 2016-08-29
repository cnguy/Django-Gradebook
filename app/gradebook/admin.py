from django.contrib import admin
from .models import Announcement, Assignment, Course, Enrollment, Grade, Section, Student, Teacher

# Register your models here.
myModels = [Announcement, Assignment, Course, Enrollment, Grade, Section, Student, Teacher]
admin.site.register(myModels)