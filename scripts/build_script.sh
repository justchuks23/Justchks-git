echo "DB_HOST=$DB_HOST" >> .env
echo "DB_NAME=$DB_NAME" >> .env
echo "DB_USER=$DB_USER" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env
echo "SECRET_KEY=$SECRET_KEY" >> .env
#sleep 50
ls -la
cat .env 

docker build -t $ZOOM_YOUTUBE_INTEGRATION_IMAGE .
docker save $ZOOM_YOUTUBE_INTEGRATION_IMAGE > zoom_youtube_integration.tar





