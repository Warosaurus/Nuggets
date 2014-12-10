FROM ubuntu:14.04
MAINTAINER warosaurus

RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/Warosaurus/Nuggets.git && mv Nuggets ~/

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
