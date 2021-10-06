# base image
FROM python:3.9.1

RUN apt-get update
RUN apt-get -y upgrade

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt
#sudo apt-get install mysql-server
# install requirements
# RUN pip install PyMySQL
# RUN apt-get -y install mysql-server
RUN #apt-get update && apt-get install libssl-dev
RUN pip install --upgrade pip
# RUN pip3 install mariadb
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app
