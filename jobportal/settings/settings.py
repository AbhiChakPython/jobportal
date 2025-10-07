import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from celery import Celery

# ===============================
# Base Paths & Environment
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
django_env = os.getenv('DJANGO_ENV', 'dev').lower()

if django_env == 'dev':
    load_dotenv(BASE_DIR / '.env.dev')
elif django_env == 'prod':
    load_dotenv(BASE_DIR / '.env.prod')

# ===============================
# Django Core Settings
# ===============================
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host not in ["localhost", "127.0.0.1"]
]
CSRF_TRUSTED_ORIGINS.append("http://127.0.0.1")

LOGIN_URL = '/api/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ===============================
# Installed Apps
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'rest_framework.authtoken',
    'django_redis',
    'whitenoise',
    'widget_tweaks',
    'guardian',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_NAME = 'anonymous'

# ===============================
# Middleware
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jobportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jobportal.wsgi.application'

# ===============================
# Database
# ===============================

# --- Production/Environment Variable Check ---
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            # CRITICAL: Do not pass a 'default' value here.
            # dj_database_url will automatically look for DATABASE_URL in the environment.
            conn_max_age=int(os.getenv('DB_CONN_MAX_AGE', 600)),
            ssl_require=os.getenv('DB_SSL_REQUIRED', 'False').lower() in ['true', '1', 'yes']
        )
    }
# --- Local Development Fallback (Optional, but good practice) ---
else:
    # If DATABASE_URL is not set, use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ===============================
# Password Validators
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===============================
# Internationalization
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===============================
# Static & Media
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===============================
# Logging
# ===============================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{levelname}] {asctime} {name} {module} {message}', 'style': '{'},
        'simple': {'format': '[{levelname}] {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'file': {'class': 'logging.FileHandler', 'filename': LOG_DIR / 'jobportal.log', 'formatter': 'verbose', 'level': 'INFO'},
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': True},
        'users': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
    },
}

# ===============================
# REST Framework
# ===============================
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '100/minute',
        'login': '5/minute',
        'jobs_list': '50/minute',
    }
}

# ===============================
# Celery Configuration
# ===============================
app = Celery('jobportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
