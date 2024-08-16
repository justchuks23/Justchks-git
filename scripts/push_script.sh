#sshpass -p $SERVER_PASSWORD scp -r -o StrictHostKeyChecking=no zoom_youtube_integration.tar $SERVER_USER@$SERVER_IP:~/

#sshpass -p $SERVER_PASSWORD ssh -tt -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '$SERVER_PASSWORD' | rm deploy_script.sh  zoom_youtube_integration.tar Dockerfile docker-compose.yml || true"

sshpass -p $SERVER_PASSWORD scp -r -o StrictHostKeyChecking=no zoom_youtube_integration.tar Dockerfile docker-compose.yml scripts/deploy_script.sh entrypoint.sh site_conf.conf $SERVER_USER@$SERVER_IP:~/

