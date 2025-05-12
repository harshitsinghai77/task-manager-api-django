#!/bin/bash

set -e

echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."

# Keep trying to connect to MySQL until successful
while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  echo "Waiting for MySQL..."
  sleep 2
done

echo "MySQL is up!"

# Wait for MySQL to be ready (if necessary)
# Run Django migrations
echo "Applying database migrations..."
python manage.py migrate

# Create a superuser 
echo "Creating superuser..."
python config/scripts/create_superuser.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run the Django application with Gunicorn
echo "Starting production server..."
gunicorn --bind 0.0.0.0:8000 --workers 3 --threads 2 config.wsgi:application

