from .settings import *
from dotenv import load_dotenv
import os
import dj_database_url

# Load development environment variables
load_dotenv(BASE_DIR / '.env.dev')

# Development-specific overrides
DEBUG = True

# Database (from DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Local caching (in-memory for dev)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery tasks run immediately in dev
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

# Optional: Media settings for dev
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Use console email backend for dev
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@jobportal.com')

# Logging overrides for development
LOGGING['handlers']['file']['level'] = os.getenv('LOG_FILE_LEVEL', 'DEBUG')
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['users']['level'] = 'INFO'
