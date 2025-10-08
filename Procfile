web: gunicorn jobportal.wsgi:application --bind 0.0.0.0:8080
worker: celery -A jobportal worker -l info
beat: celery -A jobportal beat -l info