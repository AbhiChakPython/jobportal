# users/utils/tasks.py
from django.conf import settings
from users.tasks import send_welcome_email

def send_welcome_email_dev(username, user_email):
    if settings.DEBUG:
        # In dev, call synchronously
        send_welcome_email(username, user_email)
    else:
        # In prod, use Celery
        send_welcome_email.delay(username, user_email)
