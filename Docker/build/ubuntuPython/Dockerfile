FROM ubuntu:localbase
MAINTAINER warosaurus

RUN sudo apt-get install -y python python-dev python-distribute python-pip

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
