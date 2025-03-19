from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home, login_view, logout_view, jobs_view, register_view, logout_confirm, terms_view, profile_view, \
    edit_profile_view
from django.contrib.auth import views as auth_views
from .views import UserProfileView


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout/confirm', logout_confirm, name='logout_confirm'),
    path('jobs/', jobs_view, name='jobs'),
    path('register/', register_view, name='register'),
    path('terms/', terms_view, name='terms'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)