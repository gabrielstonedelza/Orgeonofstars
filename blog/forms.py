from django import forms
from django.contrib.auth.models import User
from .models import (Volunteer, JoinTrip, Partnership, NewsLetter,
                     Report, Post, Comments, NewsUpdate, ContactUs, ClientInfoProgress, Reviews, UsersCheckedIn,
                     VideoConference
                     )


class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = NewsUpdate
        fields = ['title', 'message']


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'profession', 'country', 'photo',
                  'phone', 'why_join_Orgeon', 'additional_message']


class JoinTripForm(forms.ModelForm):
    class Meta:
        model = JoinTrip
        fields = ['name', 'email', 'phone']


class PartnershipForm(forms.ModelForm):
    class Meta:
        model = Partnership
        fields = ['partnership', 'name', 'email', 'phone']


class NewsLetterForm(forms.ModelForm):
    email = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your working email'}))

    class Meta:
        model = NewsLetter
        fields = ['email']


class ReportForm(forms.ModelForm):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Report Title'}))
    report = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Report....', 'rows': '2', 'cols': '35', 'id': 'reportform', 'name': 'reportform'}))

    class Meta:
        model = Report
        fields = ['title', 'report', 'report_doc']


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'comment....', 'id': 'commentform'}))

    class Meta:
        model = Comments
        fields = ['comment']


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))

    # class Meta:
    #     model = User
    #     fields = ['username','password']


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'name'}))
    email = forms.EmailField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    phone = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'phone'}))
    message = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Message....', 'rows': '3', 'cols': '35', 'id': 'contact_message',
               'name': 'contact_message'}))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'message']


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = ClientInfoProgress
        fields = ['care_plan', 'name', 'age', 'email', 'phone', 'emergency_phone', 'gender', 'client_image', 'next_of_kin', 'issue', 'progress', 'assessment_phase_details',
                  'development_phase_details', 'planning_phase_details', 'implementation_phase_details', 'evaluation_phase_details', 'star_phase_details']


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = ClientInfoProgress
        fields = ['care_plan', 'name', 'age', 'email', 'phone', 'emergency_phone', 'gender', 'client_image', 'next_of_kin', 'issue', 'progress', 'assessment_phase_details',
                  'development_phase_details', 'planning_phase_details', 'implementation_phase_details', 'evaluation_phase_details', 'star_phase_details']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review_content', 'ratings']


class CheckInForm(forms.ModelForm):
    check_in = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "enter your check in code here"}))

    class Meta:
        model = UsersCheckedIn
        fields = ['check_in']


class VideoConferenceForm(forms.ModelForm):
    class Meta:
        model = VideoConference
        fields = ['conference_name', 'allowed_to_join', 'is_active']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message', 'post_doc', 'image_file', 'need_replies']
