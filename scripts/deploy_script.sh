#!/bin/bash
set -x  # Enable debugging

sudo docker load --input zoom_youtube_integration.tar

#####################################################################################################################
sudo docker stop $ZOOM_YOUTUBE_INTEGRATION_CONTAINER && sudo docker rm $ZOOM_YOUTUBE_INTEGRATION_CONTAINER
sudo docker system prune -f
sudo docker volume prune -f
######################################################################################################################
docker-compose -f docker-compose.yml up -d 
