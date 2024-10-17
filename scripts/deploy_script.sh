#!/bin/bash
set -x  # Enable debugging

sudo docker load --input zoom_youtube_integration.tar

######################################################################################################
sudo docker stop $Z2Y_CONTAINER && sudo docker rm $Z2Y_CONTAINER
sudo docker system prune -f
sudo docker volume prune -f
#########################################################################################################
ls -la
docker-compose -f docker-compose.yml up -d 
