#!/bin/bash
#@Author Warosaurus
#This file will run all the containers.

docker run -d -t -P --name db -v /home/indi/:/home/local/ ubuntu:sqlite /bin/bash
docker run -d -t -i --volumes-from db --name py ubuntu:python python /home/Nuggets/Apps/a.py
#To add webapp.
