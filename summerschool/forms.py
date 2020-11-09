from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import School, SchoolKid


class KidsSchoolRegister(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class KidsSchoolUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class KidsSchoolProfileUpdate(forms.ModelForm):
    class Meta:
        model = School
        fields = ['fullname', 'photo', 'contact_number']


class SchoolKidProfileForm(forms.ModelForm):

    class Meta:
        model = SchoolKid
        fields = ['child_name', 'age', 'school', 'grade', 'photo']