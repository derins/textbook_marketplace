release: pip install psycopg2-binary
release: pip install django-widget_tweaks
release: python manage.py makemigrations
release: python manage.py migrate --run-syncdb
web: gunicorn project.wsgi
