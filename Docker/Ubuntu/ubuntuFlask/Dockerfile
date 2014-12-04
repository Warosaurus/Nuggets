FROM ubuntu:14.04
MAINTAINER indi

#Commands
#Basic
RUN apt-get update
RUN apt-get install -y git
#Python
RUN sudo apt-get install -y python python-dev python-distribute
RUN sudo apt-get install -y python-pip
RUN sudo pip install flask
RUN git clone https://github.com/Warosaurus/Nuggets.git
RUN mv Nuggets ~/
CMD python ~/Nuggets/flask_test/app.py
