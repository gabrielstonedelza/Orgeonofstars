from django.contrib import admin

from .models import Profile, MyProfileUser, LoginConfirmCode

admin.site.register(Profile)
admin.site.register(MyProfileUser)
admin.site.register(LoginConfirmCode)

