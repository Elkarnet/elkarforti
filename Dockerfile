FROM alpine

MAINTAINER parreitu@protonmail.com

# Install required packages
COPY requirements.txt /
RUN apk add --no-cache \
    python3 \
    python3-dev \
    build-base \
    nano \
    openldap-dev \
    sqlite \
    sqlite-dev \
    tzdata \
  && pip3 install --upgrade pip \
  && pip3 install -r requirements.txt

COPY elkarforti /data/web
# Copy scripts to automatic enable and disable rooms
COPY disable-all-rooms.sh /disable-all-rooms.sh
COPY enable-all-rooms.sh /enable-all-rooms.sh

RUN chmod 755 /disable-all-rooms.sh /enable-all-rooms.sh

COPY crontab.txt /crontab.txt

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000
