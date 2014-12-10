FROM ubuntu:localbase
MAINTAINER warosaurus

RUN apt-get install -y sqlite3
RUN mkdir /opt/DB/
RUN cd /opt/DB/ && sqlite3 base.db < ~/Nuggets/Docker/ubuntuSQLite/db.sql

VOLUME ["/opt/DB"]

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
#Add - create database/tables

