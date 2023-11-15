#echo "DB_HOST=$DB_HOST" >> .env
#echo "DB_NAME=$DB_NAME" >> .env
#echo "DB_USER=$DB_USER" >> .env
#echo "DB_PASSWORD=$DB_PASSWORD" >> .env
echo "SECRET_KEY=$SECRET_KEY" >> .env
#sleep 50
ls -la
cat .env 

docker build -t $ZOOM_YOUTUBE_INTEGRATION_IMAGE .
docker save $ZOOM_YOUTUBE_INTEGRATION_IMAGE > zoom_youtube_integration.tar

sshpass -p $SERVER_PASSWORD ssh -tt -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '$SERVER_PASSWORD' | rm deploy_script.sh  zoom_youtube_integration.tar Dockerfile || true"

sshpass -p $SERVER_PASSWORD scp -r -o StrictHostKeyChecking=no zoom_youtube_integration.tar Dockerfile scripts/deploy_script.sh $SERVER_USER@$SERVER_IP:~/





