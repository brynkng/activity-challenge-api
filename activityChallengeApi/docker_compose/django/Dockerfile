FROM python:3.6.2
ENV PYTHONUNBUFFERED 1

# update package lists, fix broken system packages
RUN apt-get update
RUN apt-get -f install

ARG requirements=requirements/production.txt

# install and cache dependencies in /tmp directory.
# doing it this way also installs any newly added dependencies.
RUN pip3 install --upgrade pip
ADD requirements/ /tmp/requirements
RUN pip3 install -r /tmp/$requirements

# load project files and set work directory
ADD . /app/
WORKDIR /app

# create user and add to docker group
RUN adduser --disabled-password --gecos '' activitychallenge
RUN groupadd docker
RUN usermod -aG docker activitychallenge

# grant newly created user permissions on essential files
RUN chown -R activitychallenge:$(id -gn activitychallenge) ~/
RUN chown -R activitychallenge:$(id -gn activitychallenge) /app/

# change user to newly created user
USER activitychallenge
