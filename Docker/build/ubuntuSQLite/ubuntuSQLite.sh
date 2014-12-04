#!/bin/bash
# @Author Warosaurus

#build
docker build -t ubuntu/tempsqlite .
containerid=$(docker run -d ubuntu/tempsqlite /bin/bash exit)
docker export $containerid | docker import - ubuntu:sqlite
docker rm $containerid
docker rmi ubuntu/tempsqlite
echo finished.
