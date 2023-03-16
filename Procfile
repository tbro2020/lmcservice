web: gunicorn --bind 0.0.0.0:$PORT lmcservice.wsgi
celery: celery -A lmcservice worker -l info
