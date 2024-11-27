#!/bin/sh

# Stop the script if any command fails
set -e

# Navigate to the project directory
cd /src/DSA_site_validator

# Check if the repository exists and pull the latest changes
if [ -d ".git" ]; then
    echo "Pulling the latest changes from Git..."
    git fetch origin main
    git reset --hard origin/main
else
    echo "Git repository not initialized. Skipping git pull."
fi

# Navigate to the project directory
cd /src/DSA_site_validator/validator

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser if necessary
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating Django superuser..."
    python manage.py createsuperuser --noinput || true
fi

# Start Gunicorn to serve the application
exec gunicorn validator.wsgi:application --bind 0.0.0.0:8000
