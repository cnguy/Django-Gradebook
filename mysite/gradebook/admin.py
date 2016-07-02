from django.contrib import admin
from .models import Assignment, Course, Enrollment, Grade, Section, Student, Teacher

# Register your models here.
myModels = [Assignment, Course, Enrollment, Grade, Section, Student, Teacher]
admin.site.register(myModels)