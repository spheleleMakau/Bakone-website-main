#!/usr/bin/env bash
set -e

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Verifying auth migrations..."
python manage.py showmigrations auth

echo "Checking auth_user table existence..."
python - <<'PY'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakone.settings')
django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute('SELECT 1 FROM auth_user LIMIT 1')
    print('auth_user table verified')
PY

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn bakone.wsgi:application
