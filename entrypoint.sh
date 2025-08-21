#!/bin/bash

# Source the .env file to export environment variables
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

echo "Starting Django app..."
$@
# Apply Django database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
# Start Apache in the foreground
exec apache2ctl -D FOREGROUND
