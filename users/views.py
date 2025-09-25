import random
import logging
from django.core.paginator import Paginator
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .schemas import UserProfileAPISchema
from .decorators import role_required
from .utils.tasks import send_welcome_email_dev
from pydantic import ValidationError as PydanticValidationError
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


logger = logging.getLogger(__name__)

# -----------------------------
# Home Page
# -----------------------------
def home(request):
    jobs = cache.get('all_jobs')
    if not jobs:
        jobs = list(JobListing.objects.all())
        cache.set('all_jobs', jobs, timeout=60*5)

    random_jobs = random.sample(jobs, min(len(jobs), 3))
    return render(request, 'index.html', {'jobs': random_jobs})


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('profile')  # redirect to profile if already logged in

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        remember_me = request.POST.get('remember-me')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # sets session

            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # browser close

            messages.success(request, f"Welcome back, {user.username}!")

            # redirect to 'next' if coming from @login_required, else profile
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'profile')

        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


# -----------------------------
# Logout
# -----------------------------
@login_required
def logout_view(request):
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        messages.success(request, "Logout successful")
        logger.info(f"User logged out: {username}")
        return redirect('home')
    return redirect('logout_confirm')


def logout_confirm(request):
    return render(request, 'logout.html')


# -----------------------------
# Registration
# -----------------------------
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')

    if request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "email": request.POST.get('email', '').strip().lower(),
            "location": request.POST.get('location', '') or "N/A",
            "phone_number": request.POST.get('phone_number', '') or "0000000000",
            "skills": request.POST.get('skills', ''),
            "experience": int(request.POST.get('experience', 0) or 0),
            "education": request.POST.get('education', ''),
        }

        # Validate using Pydantic
        try:
            validated_data = UserProfileAPISchema(**data)
        except PydanticValidationError as e:
            messages.error(request, f"Invalid Data: {e.errors()}")
            return redirect('register')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms', None)

        if not terms:
            messages.error(request, "You must agree to the terms and conditions")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=validated_data.username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if validated_data.email and User.objects.filter(email=validated_data.email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=validated_data.username, email=validated_data.email)
        user.set_password(password)
        user.save()

        # Trigger welcome email asynchronously
        if user.email:
            send_welcome_email_dev(user.username, user.email)

        # Create user profile
        role = request.POST.get('role', 'JOB_SEEKER')
        profile = UserProfile.objects.create(
            user=user,
            location=validated_data.location,
            phone_number=validated_data.phone_number,
            skills=validated_data.skills,
            experience=validated_data.experience,
            education=validated_data.education,
            role=role
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')


# -----------------------------
# Terms & Password Reset
# -----------------------------
def terms_view(request):
    return render(request, 'terms.html')


def password_reset_view(request):
    return render(request, 'password_reset.html')


# -----------------------------
# Profile Views
# -----------------------------
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "We created a default profile for you. Please update it.")
    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def edit_profile_view(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        data = {
            "username": user.username,
            "location": request.POST.get('location'),
            "email": request.POST.get('email'),
            "phone_number": request.POST.get('phone_number'),
            "skills": request.POST.get('skills'),
            "experience": request.POST.get('experience'),
            "education": request.POST.get('education'),
        }

        try:
            validated_data = UserProfileAPISchema(**data)
        except PydanticValidationError as e:
            messages.error(request, f"Invalid data: {e.errors()}")
            return redirect('edit_profile')

        if validated_data.email:
            user.email = validated_data.email
            user.save()

        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

        if 'remove_image' in request.POST:
            user_profile.profile_image.delete(save=False)
            user_profile.profile_image = None

        user_profile.location = validated_data.location
        user_profile.phone_number = validated_data.phone_number
        user_profile.skills = validated_data.skills
        user_profile.experience = validated_data.experience
        user_profile.education = validated_data.education
        user_profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})


# -----------------------------
# Job Views
# -----------------------------
@login_required
def jobs_view(request):
    user_profile = request.user.userprofile
    if user_profile.role == 'RECRUITER':
        jobs = JobListing.objects.filter(created_by=request.user)
    else:
        jobs = JobListing.objects.all()

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs.html', {'page_obj': page_obj})


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JobListing
from .forms import JobListingForm

# -----------------------------
# Edit Job View
# -----------------------------
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    # Check permission: Admin or the recruiter who created the job
    if not (request.user.userprofile.role == 'ADMIN' or (request.user.userprofile.role == 'RECRUITER' and job.created_by == request.user)):
        messages.error(request, "You do not have permission to edit this job.")
        return redirect('jobs')

    if request.method == 'POST':
        form = JobListingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('job-details', job_id=job.id)
    else:
        form = JobListingForm(instance=job)

    return render(request, 'create_job.html', {'form': form, 'edit_mode': True})


# -----------------------------
# Delete Job View
# -----------------------------
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    # Check permission: Admin or the recruiter who created the job
    if not (request.user.userprofile.role == 'ADMIN' or (request.user.userprofile.role == 'RECRUITER' and job.created_by == request.user)):
        messages.error(request, "You do not have permission to delete this job.")
        return redirect('jobs')

    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('jobs')

    return render(request, 'confirm_delete_job.html', {'job': job})


@login_required
def job_details_view(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_details.html', {'job': job})


# -----------------------------
# Job Creation (Admin / Recruiter)
# -----------------------------
def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@role_required('RECRUITER')
def create_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # don’t save yet
            job.created_by = request.user  # assign the creator
            job.save()
            cache.delete('all_jobs')
            return redirect('jobs')
    else:
        form = JobListingForm()

    return render(request, 'create_job.html', {'form': form})


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'forgot_password_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'