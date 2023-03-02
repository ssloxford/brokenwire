FROM ubuntu:20.04

ENV LANG C.UTF-8

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
RUN apt -y update
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata
RUN apt -y install python3-pip wget git python-mako doxygen cmake build-essential texlive-fonts-recommended texlive-fonts-extra dvipng sshpass software-properties-common 
RUN add-apt-repository -y ppa:gnuradio/gnuradio-releases
RUN apt -y install gnuradio
RUN apt -y install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy python3-mako python3-sphinx python3-lxml libfftw3-dev libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0

RUN apt -y install limesuite limesuite-udev

WORKDIR /home

ADD ./code /home/code
WORKDIR /home/code

### Make sure the newest numpy version is installed
RUN pip3 install --upgrade numpy

### Install Pyhton Requirements and Jupyter ###
RUN pip3 install -r req
RUN pip3 install --upgrade jupyter
RUN pip3 install jupyterlab

### Start a shell 
CMD ["/bin/bash"]
