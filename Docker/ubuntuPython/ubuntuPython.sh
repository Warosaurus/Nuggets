#!/bin/bash
# @Author Warosaurus

#build
docker build -t ubuntu/temppython .
containerid=$(docker run -d ubuntu/temppython /bin/bash exit)
docker export $containerid | docker import - ubuntu:python
docker rm $containerid
docker rmi ubuntu/temppython
