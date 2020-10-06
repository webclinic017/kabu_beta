FROM ubuntu:18.04
FROM nginx:latest
USER root

ENV APP_PATH /var/www/html

# RUNでコンテナ生成時に実行する
RUN apt-get update && apt-get install -y \
curl
RUN apt-get install -y python3 python3-pip unzip
RUN apt-get install -y python3-dev default-libmysqlclient-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
COPY ./default.conf /etc/nginx/conf.d/

WORKDIR $APP_PATH
COPY ./requirements.txt $APP_PATH
RUN  pip install -r $APP_PATH/requirements.txt


EXPOSE 80

ADD ./image/server/start-server.sh /tmp/start.sh
CMD /bin/sh /tmp/start.sh
