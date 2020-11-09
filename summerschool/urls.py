from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (SchoolKidProfileCreateView, SchoolKidProfileUpdateView, SchoolKidProfileDeleteView, SchoolKidProfileDetailView, UserSurveyCreateview)

urlpatterns = [
    path('summerhome/', views.summerhome, name='summerhome'),
    path('school_registrations/', views.register_school, name="school_register"),
    path('kid_login/', views.school_login_request, name='school_login'),
    path('schoolhome/', views.schoolhome, name='schoolhome'),
    path('school_profile/', views.kids_profile_school, name='school_profile'),
    path('school_kid/new/',SchoolKidProfileCreateView.as_view(),name="kid_create"),
    path('school_kid/<int:pk>/',SchoolKidProfileDetailView.as_view(),name='kids_detail'),
    path("school_kid/<int:pk>/update/",SchoolKidProfileUpdateView.as_view(),name='kid_update'),
    path('school_kid/<int:pk>/delete/',SchoolKidProfileDeleteView.as_view(),name='kid_delete'),
    path('survey/new/', UserSurveyCreateview.as_view(), name='survey_new'),
    path('donate_and_support/', views.donate_and_support, name='donate_and_support'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='summerschool/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='summerschool/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='summerschool/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='summerschool/password_reset_complete.html'), name='password_reset_complete'),
    path('school_logout/', views.school_logout, name='school_logout')
]
