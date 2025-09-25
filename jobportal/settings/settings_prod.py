import os
from dotenv import load_dotenv
from .settings import *  # Import base settings from settings.py


# Load environment variables from the corresponding .env file based on the environment
load_dotenv('.env.prod')  # Explicitly load the production .env file

# Production-specific settings
DEBUG = False  # Disable debugging in production


# Caching with Redis (for production)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Redis container service
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# Whitenoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Secure Cookies & HTTPS in production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Media settings (for production use)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Ensure proper storage configuration

# Allow only specific hosts (e.g., production domain or Render)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'your-production-domain.com').split(",")


LOGGING['handlers']['file']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['users']['level'] = 'INFO'

# Add email notifications for critical errors
LOGGING['handlers']['mail_admins'] = {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler',
    'include_html': True,
}

LOGGING['loggers']['django']['handlers'].append('mail_admins')
LOGGING['loggers']['users']['handlers'].append('mail_admins')


ADMINS = [('Admin Name', 'admin@example.com')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
