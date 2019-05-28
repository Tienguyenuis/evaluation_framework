FROM ubuntu:18.04

ENV _BASH_VERSION 5.0

COPY requirements.txt /docker/requirements.txt

RUN apt-get update &&\
    apt-get install -y python3.6 &&\
    apt-get install  -y python3-pip &&\
    apt-get install -y python &&\
    apt-get install -y python-pip &&\
    apt-get install -y vim &&\
    pip3 install -r /docker/requirements.txt &&\
    pip install -r /docker/requirements.txt

#docker build -t graph_embedding_eval:0.5 . 
