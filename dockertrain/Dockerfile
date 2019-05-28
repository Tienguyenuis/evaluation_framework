FROM ubuntu:18.04

ENV _BASH_VERSION 5.0

RUN apt-get update &&\
    apt-get install -y python3.6 &&\
    apt-get install  -y python3-pip &&\
    apt-get install -y python &&\
    apt-get install -y python-pip &&\
    apt-get install -y vim &&\
    pip3 install paramiko &&\
    pip install paramiko 

#docker build -t graph_embedding:0.5 .
