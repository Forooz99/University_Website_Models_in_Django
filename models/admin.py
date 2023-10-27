from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Department)


