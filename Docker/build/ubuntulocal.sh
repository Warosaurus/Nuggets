#!/bin/bash
# @Author Warosaurus
# Motivation: Often you pull an image which comes with multiple layers and you would like 
# to have a single layer for a base image of example.
# Pull the image and flatten it.

base="temp"
#build
docker build -t ubuntu/temp .
#run
echo creating container from: $base
dockerid=$(docker run -d ubuntu/temp)
echo flattening image
docker export $dockerid | docker import - ubuntu:localbase
echo removing container
docker rm $dockerid
echo removing old image
docker rmi ubuntu/temp ubuntu:14.04
echo finished.
