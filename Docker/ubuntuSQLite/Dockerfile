FROM ubuntu:localbase
MAINTAINER warosaurus

RUN apt-get install -y sqlite3
RUN mkdir /tmp/db/
RUN cd /tmp/db/ && sqlite3 base.db < /home/Nuggets/Docker/ubuntuSQLite/db.sql

VOLUME ["/tmp/db/", "/home/local/"]
WORKDIR /tmp/db/

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
#Add - create database/tables

CMD ["/bin/bash true"]
