FROM ubuntu:localbase
MAINTAINER warosaurus

RUN sudo apt-get install -y python python-dev python-distribute python-pip python-numpy python-scipy $
RUN cp /home/local/snmpdump.txt /home/Nuggets/Apps/

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
