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
