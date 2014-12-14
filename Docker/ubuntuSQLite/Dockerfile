FROM ubuntu:localbase
MAINTAINER warosaurus

RUN apt-get install -y sqlite3
RUN mkdir /home/db/ /home/local
RUN cd /home/db/ && sqlite3 base.db < /home/Nuggets/Docker/ubuntuSQLite/db.sql

VOLUME ["/home/db/"]

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
#Add - create database/tables

CMD ["true"]
