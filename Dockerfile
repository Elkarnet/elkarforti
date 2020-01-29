FROM alpine

MAINTAINER parreitu@protonmail.com

COPY elkarforti /data/web
COPY entrypoint.sh requirements.txt /

# Setup
RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev build-base nano openldap-dev sqlite sqlite-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


WORKDIR /data/web

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000