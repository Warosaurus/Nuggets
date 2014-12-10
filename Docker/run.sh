#!bin/bash
#@Author Warosaurus
#This file will run all the containers.

docker run -d --name db ubuntu:sqlite /bin/bash
docker run -d --volumes-from db ubuntu:python python ~/Nuggets/Apps/a.py
#To add webapp.
