#!/bin/bash
sudo docker stop $(sudo docker ps -a -q)

#remove all
#sudo docker rm -f $(sudo docker ps -a -q)

#remove not running
sudo docker rm -v $(docker ps -a -q -f status=exited);

#sudo docker rmi -f $(sudo docker images -q)
sudo docker volume rm $(sudo docker volume ls -q)

#remove all images
#sudo docker image rm $(docker images -q -f dangling=true);

#remove all volumes:
#sudo docker volume rm $(docker volume ls -q -f dangling=true);

#clean everything
#sudo docker system prune --volumes
