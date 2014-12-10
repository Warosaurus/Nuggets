FROM ubuntu:localbase
MAINTAINER warosaurus

RUN apt-get install -y sqlite3
RUN cd ~/Nuggets/Docker/ubuntuSQLite/ && sqlite3 base.db < db.sql

#Empty the cache to save space.
RUN apt-get autoclean
#Run final command
#Add - create database/tables

