#!/bin/bash

# Source the .env file to export environment variables
#!/bin/bash

# Source the .env file to export environment variables
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

$@
# Apply Django database migrations
python manage.py migrate

# Start Apache in the foreground
exec apache2ctl -D FOREGROUND


