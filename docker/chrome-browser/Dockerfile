FROM ubuntu:14.04

MAINTAINER Dibyo Majumdar <dibyo.majumdar@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y \
        libxss1 \
        libappindicator1 \
        libindicator7 \
        wget
RUN wget -O opt/google-chrome-stable_current_amd64.deb \
        https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i opt/google-chrome*.deb
RUN apt-get install -y -f
RUN dpkg -i opt/google-chrome*.deb


