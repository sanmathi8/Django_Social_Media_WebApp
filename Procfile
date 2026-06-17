release: python manage.py migrate && python manage.py init_db
web: gunicorn socialmedia.wsgi:application --log-file -
