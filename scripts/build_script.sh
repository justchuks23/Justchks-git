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

#sshpass -p $SERVER_PASSWORD ssh -tt -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '$SERVER_PASSWORD' | rm deploy_script.sh  zoom_youtube_integration.tar Dockerfile docker-compose.yml || true"

#sshpass -p $SERVER_PASSWORD scp -r -o StrictHostKeyChecking=no zoom_youtube_integration.tar Dockerfile docker-compose.yml scripts/deploy_script.sh $SERVER_USER@$SERVER_IP:~/





