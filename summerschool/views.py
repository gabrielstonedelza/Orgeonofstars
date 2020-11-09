from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import School, Student,  SchoolKid, UserSurvey
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import (KidsSchoolRegister, KidsSchoolUpdateForm, KidsSchoolProfileUpdate,SchoolKidProfileForm)
from email.message import EmailMessage
from django.conf import settings
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect


def summerhome(request):
    return render(request, "summerschool/summerhome.html")


def register_school(request):
    msg = EmailMessage()
    msg1 = EmailMessage()
    if request.method == "POST":
        form = KidsSchoolRegister(request.POST)
        if form.is_valid():
            kids_email = form.cleaned_data.get('email')

            if User.objects.filter(email=kids_email).exists():
                messages.info(request, f"Sorry,a user with the same email already exists")
            else:
                form.save()
                Student.objects.create(student_email=kids_email)
                msg["Subject"] = "Thank you for joining our summer tutoring program."
                msg["From"] = settings.EMAIL_HOST_USER
                msg["To"] = kids_email
                msg.set_content(
                    "We are glad you have decided to join us in this studies,so you know it's going to be more fun than you expected,stay blessed and see you in class.")
                hml = f"""
                    <!Doctype html>
                    <html>
                    <body>
                    <h1 style='font-style:italic;'>Thank you for joining our summer tutoring program.</h1>
                    <p style='color:SlateGray;'> We are glad you have decided to join us in this studies,so you know it's going to be more fun than you expected,stay blessed and see you in class.</p>
                    <p style='color:SlateGray;'>ORgeonofstars</p>
                    </body>
                    </html>
                    </html>
                    """
                msg.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg)
                    messages.success(request, f"Thank you for joining our summer tutoring program.")
                    return redirect('school_login')
                # to organization email
                msg1["Subject"] = "A new Kid just joined the gradeschool summer tutoring program"
                msg1["From"] = settings.EMAIL_HOST_USER
                msg1["To"] = settings.EMAIL_HOST_USER
                msg1.set_content(
                    "Got a new kid for the summer tutoring program.")
                hml = f"""
                    <!Doctype html>
                    <html>
                    <body>
                    <h1 style='font-style:italic;'>A new Kid just joined the gradeschool summer tutoring program</h1>
                    <p style='color:SlateGray;'> Got a new kid for the summer tutoring program.</p>
                    <p style='color:SlateGray;'>ORgeonofstars</p>
                    </body>
                    </html>
                    </html>
                    """
                msg1.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg1)
        else:
            messages.info(request, f"Something went wrong")
    else:
        form = KidsSchoolRegister()

    context = {
        "form": form
    }
    return render(request, "summerschool/schoolregister.html", context)


@login_required
def kids_profile_school(request):
    if School.objects.filter(user=request.user).exists():
        user = get_object_or_404(School, user=request.user)
        if user:
            user.verified = True
            user.save()

        if request.method == "POST":
            ug_form = KidsSchoolUpdateForm(request.POST, instance=request.user)
            ugp_form = KidsSchoolProfileUpdate(request.POST, request.FILES, instance=request.user.school)
            if ug_form.is_valid() and ugp_form.is_valid():
                ug_form.save()
                ugp_form.save()
                return redirect('schoolhome')
        else:
            ug_form = KidsSchoolUpdateForm(instance=request.user)
            ugp_form = KidsSchoolProfileUpdate(instance=request.user.school)
    else:
        messages.info(request, f"sorry you are not in our school list")
        return redirect('summerhome')

    context = {
        "ug_form": ug_form,
        "ugp_form": ugp_form
    }

    return render(request, "summerschool/schoolprofile.html", context)


def school_login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            uname = request.POST['username']
            upassword = request.POST['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)
                uemail = user.email
                suser = get_object_or_404(School, user=user)
                if Student.objects.filter(student_email=uemail).exists():
                    if suser.verified:
                        return redirect('schoolhome')
                    else:
                        return redirect('school_profile')
                else:
                    messages.info(request, f"sorry we don't have your name in our school lists")
                    return redirect('main')
                # Redirect to a success page.
            else:
                messages.info(request, f"invalid username or password")
        else:
            messages.info(request, f"invalid information given")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }

    return render(request, "summerschool/school_login.html", context)


@login_required
def schoolhome(request):
    user_kids = SchoolKid.objects.filter(user=request.user).order_by('-date_registered')

    context = {
      "user_kids": user_kids
    }

    return render(request, 'summerschool/school_home.html', context)


@login_required
def school_logout(request):
    return render(request, "summerschool/logout.html")


class SchoolKidProfileCreateView(LoginRequiredMixin, CreateView):
    model = SchoolKid
    fields = ['child_name', 'age', 'school', 'grade', 'photo']
    success_url = '/schoolhome'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SchoolKidProfileDetailView(LoginRequiredMixin, DetailView):
    model = SchoolKid


class SchoolKidProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SchoolKid
    fields = ['child_name', 'age', 'school', 'grade', 'photo']
    success_url = '/schoolhome'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        kid = self.get_object()
        if self.request.user == kid.user:
            return True
        else:
            return False


class SchoolKidProfileDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = SchoolKid
    success_url = '/schoolhome'

    def test_func(self):
        kid = self.get_object()
        if self.request.user == kid.user:
            return True
        else:
            return False


class UserSurveyCreateview(CreateView):
    model = UserSurvey
    fields = ['usefulness', 'participate', 'recommend', 'something_new', 'ratings', 'improvement']
    success_url = '/donate_and_support'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def donate_and_support(request):

    return render(request, "summerschool/donate_and_suport.html")
