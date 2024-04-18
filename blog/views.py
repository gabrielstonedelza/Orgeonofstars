from django.shortcuts import render, redirect, get_object_or_404
from .models import (Volunteer, Events, JoinTrip, Partnership, NewsLetter, Report, Post, Comments, Gallery,
                     ContactUs, ClientInfoProgress, NotifyMe, Reviews, UsersCheckedIn, VideoConference)
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from email.message import EmailMessage
import smtplib
from django.conf import settings
import pytz
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import (VolunteerForm,
                    JoinTripForm,
                    PartnershipForm,
                    NewsLetterForm,
                    ReportForm,
                    CommentsForm,
                    NewsUpdateForm, ContactForm, ReviewForm, CheckInForm, VideoConferenceForm, PostCreateForm,
                    CreateClientForm, ClientUpdateForm
                    )
from django.contrib.auth.models import User
import random
from django.contrib import auth
from django.utils import timezone
from summerschool.models import UserSurvey
from users.models import Profile, MyProfileUser, LoginConfirmCode
from summerschool.models import School, Student, SchoolKid
from .notifications import my_notifications
from blog.process_mail import send_my_mail
from .check_ins import mycheck_in


def csrf_failure(request, reason=""):
    return render(request, "blog/403_csrf.html")


@login_required()
def news_letter(request):
    subscribed_users = NewsLetter.objects.all()
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)
    if request.method == "POST":
        form = NewsUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title').upper()
            update_message = form.cleaned_data.get('message')
            send_my_mail("Hi from Orgeon of stars", settings.EMAIL_HOST_USER, subscribed_users,
                         {"title": title, "message": update_message},
                         "email_templates/news_letter.html")
            return redirect('newsletter_create')
    else:
        form = NewsUpdateForm()

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/newsletter.html", context)


def home(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if NewsLetter.objects.filter(email=email).exists():
                messages.info(request, "This email already exists.")
            else:
                form.save()
                message = f"A new subscriber with the email '{email}' just subscribed to your newsletter."
                send_my_mail("New subscriber", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER,
                             {"message": message, "subscriber": email}, "email_templates/news_letter_subscribe.html")

                return redirect('home')

    else:
        form = NewsLetterForm()

    context = {
        'form': form
    }
    return render(request, "blog/home.html", context)


def success_stories(request):
    return render(request, "blog/success-stories.html")


def needy_stories(request):
    return render(request, "blog/stories_of_need.html")


def inspirational_stories(request):
    return render(request, "blog/inspirational_stories.html")


def some_videos(request):
    return render(request, "blog/some_videos.html")


class VolunteerFormView(CreateView):
    model = Volunteer
    fields = ['name', 'email', 'profession', 'country', 'photo',
              'phone', 'why_join_Orgeon', 'additional_message']
    success_url = '/volunteers'

    def form_valid(self, form):
        v_email = form.cleaned_data.get('email')
        v_name = form.cleaned_data.get('name')
        message = f"{v_name} just volunteered for Orgeon of stars"
        v_message = "Thank you for volunteering to work with Orgeon of stars,in order to know more about  you we will contact you soon,stay blessed."

        send_my_mail("New Volunteer", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER,
                     {"name": v_name, "message": message}, "email_templates/new_volunteer.html")
        send_my_mail("Welcome to ORgeon of stars", settings.EMAIL_HOST_USER, v_email,
                     {"name": v_name, "message": v_message}, "email_templates/volunteer_message.html")

        return super().form_valid(form)


class Volunteers(ListView):
    model = Volunteer
    template_name = 'blog/volunteers_list.html'
    context_object_name = 'volunteers'
    ordering = ['-date_volunteered']


@login_required
def our_volunteers(request):
    volunteers = Volunteer.objects.all().order_by('-date_volunteered')
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)

    context = {
        "ourvolunteers": volunteers,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/ourvolunteer_list.html", context)


def events(request):
    events = Events.objects.all().order_by('-date_posted')[:1]

    context = {
        'events': events
    }

    return render(request, "blog/events.html", context)


def join_trip(request):
    if request.method == "POST":
        form = JoinTripForm(request.POST)
        if form.is_valid():
            trip_email = form.cleaned_data.get('email')
            if JoinTrip.objects.filter(email=trip_email).exists():
                messages.info(request, "Email already exitst.")
        else:
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            t_message = "Orgeon of stars is so delighted that you have decided to join our trip, saving lives and helping the vulnerable children is our top priority and we are happy that you've made it yours too.We will let you know of any other information before we embark on this journey.Stay blessed."

            send_my_mail(f"{name} wants to join the trip.", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER,
                         {"name": name, "email": email, "phone": phone}, "email_templates/new_tripper.html")
            send_my_mail(f"Hi {name}!,", settings.EMAIL_HOST_USER, email, {"name": name, "message": t_message},
                         "email_templates/tripper_message.html")

            messages.success(
                request, "Thank you for joining us on this trip.")
            return redirect('events')

    else:
        form = JoinTripForm()

    context = {
        'form': form
    }

    return render(request, "blog/jointrip_form.html", context)


def become_partner(request):
    partner_message = "We are happy to see you and also partner with you.We will contact you soon for additional information.Stay blessed."
    if request.method == "POST":
        form = PartnershipForm(request.POST)
        if form.is_valid():
            partner_email = form.cleaned_data.get('email')
            if Partnership.objects.filter(email=partner_email).exists():
                messages.info(
                    request, "A partner with the same email already exits.")

            else:
                form.save()
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')

                send_my_mail(f"Thank you for your partnership {name}.", settings.EMAIL_HOST_USER, partner_email,
                             {"name": name, "message": partner_message}, "email_templates/partner_success_message.html")
                send_my_mail("Got new partner", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER,
                             {"name": name, "email": email, "phone": phone}, "email_templates/new_partner.html")

                messages.success(request, "Thank you for joining us..")
                return redirect('partners')
    else:
        form = PartnershipForm()

    context = {
        'form': form
    }

    return render(request, "blog/partnerform.html", context)


def partners(request):
    partners = Partnership.objects.all()

    context = {
        'partners': partners
    }

    return render(request, "blog/partners.html", context)


def donate(request):
    return render(request, "blog/donate.html")


@login_required
def report_list(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        all_reports = Report.objects.all().order_by('-date_posted')
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)

        paginator = Paginator(all_reports, 10)
        page = request.GET.get('page')
        all_reports = paginator.get_page(page)
    else:
        messages.info(request, "Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "reports": all_reports,
        "all_reports": all_reports,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/reports.html", context)


@login_required()
def report_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        mycheck = mycheck_in(request.user)
        my_notify = my_notifications(request.user)
        report = get_object_or_404(Report, id=id)
        hasRead = False
        if report:
            if not report.has_read.filter(id=request.user.id).exists():
                report.has_read.add(request.user)
                hasRead = True
        reports = Report.objects.all().order_by('-date_posted')[:6]
    else:
        messages.info(request, "Sorry we cannot find your login details")
        return redirect('login')

    context = {
        'report': report,
        'hasread': hasRead,
        'reports': reports,
        "user_has_checked_in": mycheck['user_has_checked_in'],
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/report_detail.html", context)


@login_required
def create_report(request):
    users = User.objects.exclude(id=request.user.id)
    admin_email = get_object_or_404(User, username="joselyn")

    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        mycheck = mycheck_in(request.user)
        my_notify = my_notifications(request.user)
        if request.method == "POST":
            form = ReportForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                report = form.cleaned_data.get('report')
                report_doc = form.cleaned_data.get('report_doc')
                Report.objects.create(user=request.user, title=title, report=report, report_doc=report_doc)

                send_my_mail(f"Got new report from {request.user.username}", settings.EMAIL_HOST_USER,
                             admin_email.email, {
                                 "name": request.user.username, },
                             "email_templates/report_success_message.html")

                messages.success(request, "Your report was created successfully.")
                return redirect('reports')
        else:
            form = ReportForm()
    else:
        messages.info(request, "Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/report_form.html", context)


@login_required()
def employees(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        mycheck = mycheck_in(request.user)
        my_notify = my_notifications(request.user)
        employees = Profile.objects.filter(verified=True)

    else:
        messages.info(request, "Sorry we cannot find your login details")
        return redirect('login')
    context = {
        'employees': employees,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/employees.html", context)


@login_required
def create_post(request):
    need_replies = False
    employees_email = []
    employees = User.objects.exclude(id=request.user.id)
    users = User.objects.exclude(id=request.user.id)
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            pdoc = form.cleaned_data.get('post_doc')
            img_file = form.cleaned_data.get('image_file')
            if form.cleaned_data.get('need_replies'):
                need_replies = True
            Post.objects.create(author=request.user, title=title, message=message, image_file=img_file, post_doc=pdoc,
                                need_replies=need_replies)
            for i in employees:
                employees_email.append(i.email)
            send_my_mail(f"New post from {request.user.username}", settings.EMAIL_HOST_USER, employees_email,
                         {"name": request.user.username, }, "email_templates/post_success_message.html")

            return redirect('posts')
    else:
        form = PostCreateForm()

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/post_form.html", context)


@login_required
def post_list(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        posts = Post.objects.all().order_by('-date_posted')
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')

    context = {
        "posts": posts,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/post_list.html", context)


@login_required()
def post_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)

        hasRead = False
        post = get_object_or_404(Post, id=id)
        user = get_object_or_404(User, username=post.author)

        if post:
            post.views += 1
            post.save()
            if not post.has_read.filter(id=request.user.id).exists():
                post.has_read.add(request.user)
                hasRead = True

        comments = Comments.objects.filter(post=post).order_by('-date_posted')
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        comments = paginator.get_page(page)

        if request.method == "POST":
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment = request.POST.get('comment')
                comment = Comments.objects.create(
                    user=request.user, post=post, comment=comment)
                comment.save()

        else:
            form = CommentsForm()
    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')

    context = {
        "post": post,
        'form': form,
        'comments': comments,
        'hasRead': hasRead,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    if request.is_ajax():
        html = render_to_string("blog/comment_form.html",
                                context, request=request)
        return JsonResponse({"form": html})

    return render(request, "blog/post_detail.html", context)


@login_required
def check_in(request):
    mycheck = mycheck_in(request.user)

    my_notify = my_notifications(request.user)
    this_user = get_object_or_404(LoginConfirmCode, logged_user=request.user)
    your_code = this_user.login_code
    admin_user = User.objects.get(username="joselyn")

    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin_code = form.cleaned_data.get('check_in')
            if checkin_code == this_user.login_code:
                UsersCheckedIn.objects.create(
                    user=request.user, check_in=checkin_code, check_date=date.today())
                if request.user.username == "joselyn":
                    send_my_mail("You just checked in at Orgeon", settings.EMAIL_HOST_USER, admin_user.email,
                             {"name": request.user.username, }, "email_templates/checkin_alert.html")
                else:
                    send_my_mail(f"New check in from {request.user.username}", settings.EMAIL_HOST_USER, admin_user.email,
                                 {"name": request.user.username, }, "email_templates/checkin_alert.html")

                send_my_mail("Successful Check in", settings.EMAIL_HOST_USER, request.user.email,
                             {"name": request.user.username, }, "email_templates/users_checkin_alert.html")
                return redirect('main')
            else:
                messages.info(request, "Wrong code entered")
        else:
            messages.info(
                request, "Invalid code,please type code as you see it")
    else:
        form = CheckInForm()

    context = {
        "form": form,
        "your_code": your_code,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/checkin.html", context)


@login_required()
def main(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        form = ''
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)
        v_users = []
        users = User.objects.exclude(id=request.user.id)
        for i in users:
            if i.profile.verified:
                v_users.append(i)
        reports = Report.objects.all().order_by('-date_posted')[:6]
        posts = Post.objects.all().order_by('-date_posted')
        td = date.today()
        tt = timezone.now()
        ntt = tt.time
        current_events = Events.objects.filter(date_of_event=td)

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')
    context = {
        "chat": v_users,
        'reports': reports,
        'posts': posts,
        'current_events': current_events,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "form": form,
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/main.html", context)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Events
    fields = ['theme', 'venue', 'date_of_event',
              'event_poster', 'description_of_event']
    success_url = '/events'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Events


@login_required()
def user_activities(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)
        school_users = School.objects.all()
        users = Profile.objects.filter(verified=True).count()
        students = SchoolKid.objects.all()
        grade_school = SchoolKid.objects.filter(school="GradeSchool")
        pre_school = SchoolKid.objects.filter(school="PreSchool")
        kindergarten = SchoolKid.objects.filter(school="Kindergarten")
        volunteers = Volunteer.objects.all().count()
        partners = Partnership.objects.all().count()
        subscribers = NewsLetter.objects.all().count()
        myclients = ClientInfoProgress.objects.all().count()

        useful = UserSurvey.objects.filter(usefulness__gt=5)
        participate = UserSurvey.objects.filter(participate="yes")
        recommend = UserSurvey.objects.filter(recommend="yes")
        something_new = UserSurvey.objects.filter(something_new="yes")
        checkins = UsersCheckedIn.objects.all().order_by('-date_checked_in')
        paginator = Paginator(checkins, 10)
        page = request.GET.get('page')
        checkins = paginator.get_page(page)

    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')

    context = {
        "users": users,
        "volunteers": volunteers,
        "partners": partners,
        "myclients": myclients,
        "subscribers": subscribers,
        "students": students,
        "grade_school": grade_school,
        "pre_school": pre_school,
        "kindergarten": kindergarten,
        "school_users": school_users,
        "useful": useful,
        "participate": participate,
        "recommend": recommend,
        "something_new": something_new,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "checkins": checkins,
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/activities.html", context)


@login_required
def our_summer_program(request):
    all_students = SchoolKid.objects.all().order_by('-date_registered')

    context = {
        "all_students": all_students
    }

    return render(request, "blog/all_students.html", context)


def gallery(request):
    gallery = Gallery.objects.all().order_by('-date_posted')
    context = {
        "gallery": gallery
    }
    return render(request, "blog/gallery.html", context)


@login_required
def all_users(request):
    users = User.objects.exclude(id=request.user.id)

    context = {
        "users": users,
    }

    return render(request, "blog/users-direct.html", context)


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            message = form.cleaned_data.get('message')
            ContactUs.objects.create(
                name=name, email=email, phone=phone, message=message)

            send_my_mail(f"Message from {name}", settings.EMAIL_HOST_USER, "help@orgeonofstars.org",
                         {"name": name, "email": email,
                             "phone": phone, "message": message},
                         "email_templates/contact_alert.html")
            return redirect('home')

    else:
        form = ContactForm()

    context = {
        "form": form
    }

    return render(request, "blog/contact-us.html", context)


@login_required
def client_list(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        all_clients = ClientInfoProgress.objects.all().order_by('-date_issued')
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)
    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')

    context = {
        "clients": all_clients,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/clientinfoprogress_list.html", context)


@login_required
def client_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        client = get_object_or_404(ClientInfoProgress, id=id)
        my_notify = my_notifications(request.user)
        mycheck = mycheck_in(request.user)

    else:
        messages.info(request, "Sorry your login details were not found")
        return redirect('login')

    context = {
        "client": client,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/client_detail.html", context)


@login_required
def create_client(request):
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)
    if request.method == "POST":
        form = CreateClientForm(request.POST, request.FILES)
        if form.is_valid():
            cplan = form.cleaned_data.get('care_plan')
            name = form.cleaned_data.get('name')
            age = form.cleaned_data.get('age')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            ephone = form.cleaned_data.get('emergency_phone')
            gender = form.cleaned_data.get('gender')
            cimage = form.cleaned_data.get('client_image')
            nok = form.cleaned_data.get('next_of_kin')
            issue = form.cleaned_data.get('issue')
            progress = form.cleaned_data.get('progress')
            a_details = form.cleaned_data.get('assessment_phase_details')
            d_details = form.cleaned_data.get('development_phase_details')
            p_details = form.cleaned_data.get('planning_phase_details')
            i_details = form.cleaned_data.get('implementation_phase_details')
            e_details = form.cleaned_data.get('evaluation_phase_details')
            s_details = form.cleaned_data.get('star_phase_details')

            ClientInfoProgress.objects.create(care_plan=cplan, assessment_officer=request.user, name=name, age=age,
                                              email=email, phone=phone, emergency_phone=ephone, gender=gender,
                                              client_image=cimage, next_of_kin=nok, issue=issue, progress=progress,
                                              assessment_phase_details=a_details, development_phase_details=d_details,
                                              planning_phase_details=p_details, implementation_phase_details=i_details,
                                              evaluation_phase_details=e_details, star_phase_details=s_details)
            messages.success(request, "Client was created successfully")
            return redirect('clients')

    else:
        form = CreateClientForm()
    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/clientinfoprogress_form.html", context)


@login_required
def client_update(request, id):
    client = get_object_or_404(ClientInfoProgress, id=id)
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)
    if request.method == "POST":
        form = ClientUpdateForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client details updated")
            return redirect('clients')
    else:
        form = ClientUpdateForm(instance=client)
    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }
    return render(request, "blog/client_update_form.html", context)


class ClientInfoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClientInfoProgress
    success_url = '/clients'

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.assessment_officer:
            return True
        else:
            return False


def reviews(request):
    all_surveys = UserSurvey.objects.all().order_by('-date_answered')

    # all reviews
    all_reviews = Reviews.objects.all().order_by('-date_posted')

    context = {

        "all_reviews": all_reviews,
        "all_surveys": all_surveys,
    }

    return render(request, "blog/reviews.html", context)


def create_reviews(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()

            send_my_mail("New review posted", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, {"name": ""},
                         "email_templates/review_alert.html")

            messages.success(request, 'Review Added.')
            return redirect('reviews')

    else:
        form = ReviewForm()

    context = {
        "form": form
    }

    return render(request, "blog/review_form.html", context)


@login_required
def user_notifications(request):
    my_notify = my_notifications(request.user)
    mycheck = mycheck_in(request.user)

    if request:
        for i in my_notify['notification']:
            if not i.read:
                i.read = True
                i.save()

    paginator = Paginator(my_notify['notification'], 10)
    page = request.GET.get('page')
    my_notify['notification'] = paginator.get_page(page)

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/notifications.html", context)


class CreateConferenceView(LoginRequiredMixin, CreateView):
    model = VideoConference
    fields = ['conference_name', 'allowed_to_join', 'is_active']
    success_url = '/all-conferences'

    def form_valid(self, form):
        form.instance.conference_creator = self.request.user
        return super().form_valid(form)


@login_required
def all_conferences(request):
    conferences = VideoConference.objects.all().order_by('-date_started')
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)

    context = {
        "conferences": conferences,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/all_conferences.html", context)


@login_required
def conference_detail(request, id):
    conference = get_object_or_404(VideoConference, id=id)
    mycheck = mycheck_in(request.user)
    my_notify = my_notifications(request.user)
    my_allowed_users = conference.allowed_to_join.all()
    print(my_allowed_users)

    context = {
        "conference": conference,
        "my_allowed_users": my_allowed_users,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "user_has_checked_in": mycheck['user_has_checked_in']
    }

    return render(request, "blog/conference_detail.html", context)


class ConferenceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoConference
    fields = ['conference_name', 'allowed_to_join', 'is_active']
    success_url = '/all-conferences'

    def form_valid(self, form):
        form.instance.conference_creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.conference_creator:
            return True
        else:
            return False


class ConferenceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoConference
    success_url = '/all-conferences'

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.conference_creator:
            return True
        else:
            return False
