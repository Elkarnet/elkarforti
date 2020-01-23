FROM alpine

MAINTAINER parreitu@protonmail.com

# Initialize
RUN mkdir -p /data/web

WORKDIR /data
COPY requirements.txt /data/

COPY start.sh /
RUN chmod +x /start.sh


# Setup
RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev build-base nano openldap-dev sqlite sqlite-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


WORKDIR /data/web


