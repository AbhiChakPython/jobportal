from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(username, user_email):
    send_mail(
        subject=f"Welcome to Job Portal, {username} 🎉",
        message=f"Hi {username},\n\nThank you for registering on Job Portal. Explore jobs and apply today!",
        from_email="noreply@jobportal.com",
        recipient_list=[user_email],
        fail_silently=False,
    )