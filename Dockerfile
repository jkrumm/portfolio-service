FROM python:3.9.1

RUN apt-get update && mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /usr/src/app
