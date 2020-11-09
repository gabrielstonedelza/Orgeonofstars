from django.contrib import admin
from .models import School, Student,  SchoolKid, UserSurvey

admin.site.register(School)
admin.site.register(Student)
admin.site.register(SchoolKid)
admin.site.register(UserSurvey)
