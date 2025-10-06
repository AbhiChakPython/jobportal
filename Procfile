# ===============================
# Web process (Django Gunicorn server)
# ===============================
web: gunicorn jobportal.wsgi:application --bind 0.0.0.0:$PORT

# ===============================
# Celery worker (handles background tasks)
# ===============================
worker: celery -A jobportal worker -l info

# ===============================
# Celery beat (handles scheduled tasks)
# ===============================
beat: celery -A jobportal beat -l info
