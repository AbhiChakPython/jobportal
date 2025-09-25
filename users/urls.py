# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, login_view, logout_view, register_view, logout_confirm, terms_view,
    profile_view, edit_profile_view, jobs_view, job_details_view, create_job, CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, edit_job, delete_job
)

urlpatterns = [
    path('', home, name='home'),
    path('terms/', terms_view, name='terms'),

    # Authentication
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/logout/confirm/', logout_confirm, name='logout_confirm'),
    path('auth/register/', register_view, name='register'),

    # Profile
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),

    # Jobs
    path('jobs/', jobs_view, name='jobs'),
    path('jobs/<int:job_id>/', job_details_view, name='job-details'),
    path('jobs/<int:job_id>/edit/', edit_job, name='edit_job'),
    path('create_job/', create_job, name='create-job'),
    path('jobs/<int:job_id>/delete/', delete_job, name='delete_job'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Forgot Password (for anonymous users)
    path('forgot-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('forgot-password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('forgot-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('forgot-password/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
