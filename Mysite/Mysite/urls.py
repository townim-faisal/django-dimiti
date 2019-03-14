"""Mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from auth_user.views import user_signin, user_signout, user_signup, user_activate
from django.contrib.auth import views as password_reset_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # music
    re_path(r'^music/', include('music.urls')),

    # authentication
    path('signin/', user_signin, name='signin'),
    path('signout/', user_signout, name='signout'),
    path('signup/', user_signup, name='signup'),
    path('activate/<uidb64>/<token>/', user_activate, name='activate'),

    # password reset - Django 2.1 contrib views change from function view to class view
    path('password_reset/',
        password_reset_views.PasswordResetView.as_view(
            template_name="auth_user/password-reset/password_reset_form.html",
            email_template_name = "auth_user/password-reset/password_reset_email.html",
            subject_template_name = "auth_user/password-reset/password_reset_subject.txt"
        ),
        name='password_reset'
    ),
    path('password_reset/done/',
        password_reset_views.PasswordResetDoneView.as_view(
            template_name = "auth_user/password-reset/password_reset_done.html"
        ),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        password_reset_views.PasswordResetConfirmView.as_view(
            template_name = "auth_user/password-reset/password_reset_confirm.html"
        ),
        name='password_reset_confirm'
    ),
    path('reset/done/',
        password_reset_views.PasswordResetCompleteView.as_view(
            template_name = "auth_user/password-reset/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),

    #profile
    re_path(r'^profile/', include('user_profile.urls')),


]
