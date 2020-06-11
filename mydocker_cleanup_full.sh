#!/bin/bash
sudo docker stop $(sudo docker ps -a -q)

#remove all
sudo docker rmi -f $(sudo docker images -q)
sudo docker rm -f $(sudo docker ps -a -q)

#remove all images
sudo docker image rm $(docker images -q -f dangling=true);

#remove all volumes:
sudo docker volume rm $(docker volume ls -q -f dangling=true);

#clean everything
sudo docker system prune --volumes
