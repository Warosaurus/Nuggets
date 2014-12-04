FROM ubuntu:14.04
MAINTAINER warosaurus

RUN apt-get update
RUN apt-get install -y git
RUN cd ~/
RUN git clone https://github.com/Warosaurus/Nuggets.git

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
