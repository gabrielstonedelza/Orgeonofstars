from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from django.conf import settings
from .models import Profile, MyProfileUser, LoginConfirmCode
import sys
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from blog.process_mail import send_my_mail
from blog.check_ins import mycheck_in
from blog.notifications import my_notifications
import secrets


@login_required()
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            usermail = form.cleaned_data.get('email')
            if User.objects.filter(email=usermail).exists():
                messages.info(request, f"{usermail} already exists.")
            else:
                form.save()
                username = form.cleaned_data.get('username')
                MyProfileUser.objects.create(profiler_email=usermail)
                subject = f"New employee added."
                message = f"An employee with the username {username} was just added."
                from_email = settings.EMAIL_HOST_USER
                to_list = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                messages.success(request, f"{username}'s profile successfully created.")
                return redirect('employees')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, "users/register.html", context)


@login_required()
def profile(request):
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, 'users/profile.html', context)


def login_request(request):
    uuser = ''
    user_get_login_code = secrets.SystemRandom().randint(1, 10000)
    has_login_code_already = False
    user_platform = sys.platform
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            uname = request.POST['username']
            upassword = request.POST['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)

                if not LoginConfirmCode.objects.filter(logged_user=user).exists():
                    LoginConfirmCode.objects.create(logged_user=user, logged_in_platform=user_platform,
                                                    login_code=user_get_login_code)
                    return redirect('main')
                else:
                    messages.info(request,
                                  f"you already have an unexpired login token,meaning you have logged in on another "
                                  f"device,please wait just a second and login again as we log you out of the other "
                                  f"device")
                    euser = get_object_or_404(LoginConfirmCode, logged_user=user)
                    if euser:
                        euser.delete()
                    return redirect('login')
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
        "has_login_code_already": has_login_code_already
    }
    return render(request, "users/login.html", context)


def logout_request(request):
    try:
        ul1 = LoginConfirmCode.objects.filter(logged_user=request.user)
        if ul1:
            ul1.delete()
        #     save users last seen

    except LookupError as e:
        messages.info(request, f"User details relating to your information does not exist,{e}")
    return render(request, "users/logout.html")
