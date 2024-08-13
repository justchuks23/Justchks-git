#!/bin/bash

# Print the current directory
echo "Current directory:"
pwd

# List files in the build context
echo "Listing files in the build context:"
ls -la

# Check if site_conf.conf exists
if [ -f "site_conf.conf" ]; then
    echo "site_conf.conf file exists."
else
    echo "site_conf.conf file does not exist."
fi
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "DEBUG=$DEBUG" >> .env
echo "DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME" >> .env
echo "DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL" >> .env
echo "DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD" >> .env
#sleep 50
ls -la
cat .env 

docker build -t $Z2Y_IMAGE .
docker save $Z2Y_IMAGE > zoom_youtube_integration.tar





