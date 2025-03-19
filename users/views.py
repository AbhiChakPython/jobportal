from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
# from django.urls import reverse
from .serializers import UserProfileSerializer
from pydantic import ValidationError
from .schemas import UserProfileAPISchema
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def home(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass  # This ensures messages are marked as read and won't persist
    return render(request, 'index.html')


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_Me = request.POST.get('remember-me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if remember_Me:
                request.session.set_expiry(1209600)  # 2 weeks Session then closed
            else:
                request.session.set_expiry(0)  # Session will expire after browser is closed

            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials", extra_tags="danger")
            return redirect('login')
    return render(request, 'login.html')


def logout_confirm(request):
    return render(request, 'logout.html')


def logout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to log out")
        return redirect('login')

    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout successful")
        return redirect('home')

    return redirect('logout_confirm')


def jobs_view(request):
    return render(request, 'jobs.html')


def register_view(request):
    if request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "email": request.POST.get('email').strip().lower(),
            "location": request.POST.get('location'),
            "phone_number": request.POST.get('phone_number'),
            "skills": request.POST.get('skills'),
            "experience": request.POST.get('experience'),
            "education": request.POST.get('education'),
        }

        try:
            validated_data = UserProfileAPISchema(**data)
        except ValidationError as e:
            messages.error(request, f"Invalid Data: {e.errors()}")
            return redirect('register')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms', None)

        if validated_data.email in ['email', '', 'NA', 'na', 'Not Applicable', 'not applicable']:
            email = None

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

        user = User.objects.create_user(username=validated_data.username, email=validated_data.email, password=password)
        user.save()

        UserProfile.objects.create(
            user=user,
            location=validated_data.location,
            phone_number=validated_data.phone_number,
            skills=validated_data.skills,
            experience=validated_data.experience or 0,
            education=validated_data.education,
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')


def terms_view(request):
    return render(request, 'terms.html')


def password_reset_view(request):
    return render(request, 'password_reset.html')


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            validated_data = UserProfileAPISchema(**request.data)
        except ValidationError as e:
            return Response({"error": e.errors()}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if validated_data.email:
            user.email = validated_data.email
            user.save()

        user_profile.location = validated_data.location
        user_profile.phone_number = validated_data.phone_number
        user_profile.skills = validated_data.skills
        user_profile.experience = validated_data.experience or 0
        user_profile.education = validated_data.education
        user_profile.save()

        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)


def profile_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view your profile")
        return redirect('login')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, "User profile not found")
        return redirect('home')

    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def edit_profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

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
            validated_data = UserProfileSchema(**data)
        except ValidationError as e:
            messages.error(request, f"Invalid data: {e.errors()}")
            return redirect('edit_profile')

        # profile_image = request.POST.get('profile_image')

        if validated_data.email:
            user.email = validated_data.email
            user.save()

        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

        if 'remove_image' in request.POST:
            user_profile.profile_image.delete(save=False)  # Deletes the existing profile image
            user_profile.profile_image = None

        user_profile.location = validated_data.location
        user_profile.phone_number = validated_data.phone_number
        user_profile.skills = validated_data.skills
        user_profile.experience = validated_data.experience
        user_profile.education = validated_data.education
        user_profile.save()

        messages.success(request, 'User profile updated successfully')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})
