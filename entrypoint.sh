#!/bin/sh

# Stop execution if any command fails
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files to Google Cloud Storage..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"
