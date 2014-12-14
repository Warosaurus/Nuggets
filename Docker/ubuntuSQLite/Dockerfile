FROM ubuntu:localbase
MAINTAINER warosaurus

RUN apt-get install -y sqlite3
RUN mkdir /opt/db/
RUN cd /opt/db/ && sqlite3 base.db < /home/Nuggets/Docker/ubuntuSQLite/db.sql

VOLUME ["/opt/db", "/home/local"]

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
#Add - create database/tables

CMD ["/bin/bash true"]
