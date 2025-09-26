from .settings import *
from dotenv import load_dotenv
import os

# Load development environment variables
load_dotenv(BASE_DIR / '.env.dev')

# Development-specific overrides
DEBUG = True

# Local caching (in-memory for dev)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery tasks run immediately in dev
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Optional: Media settings for dev
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Use console email backend for dev (emails printed to terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@jobportal.com'

# Logging overrides for development
LOGGING['handlers']['file']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['users']['level'] = 'INFO'
