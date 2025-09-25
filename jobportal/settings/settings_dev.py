from .settings import *  # Import base settings from settings.py
from dotenv import load_dotenv
import os


# Load environment variables from the corresponding .env file based on the environment
load_dotenv('.env.dev')  # Explicitly load the development .env file
# Development-specific settings
DEBUG = True  # Enable debugging for development


# Local caching (Optional, only if you want Redis caching in development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery tasks will run immediately instead of sending to broker
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True  # propagate exceptions

LOGIN_URL = '/auth/login/'  # matches your login_view path
LOGIN_REDIRECT_URL = '/profile/'  # optional, default redirect after login

# Optional: Local media settings, useful for development environment
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Use console email backend in development (emails printed to terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@jobportal.com'

# File logs: keep detailed
LOGGING['handlers']['file']['level'] = 'DEBUG'

# Console logs: reduce verbosity
LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['handlers']['console']['formatter'] = 'simple'

# App-specific loggers
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['users']['level'] = 'INFO'