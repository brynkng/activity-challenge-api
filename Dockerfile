FROM python:3.6.2
ENV PYTHONUNBUFFERED 1

# update package lists, fix broken system packages
RUN apt-get update
RUN apt-get -f install
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ARG requirements=requirements/production.txt

# install and cache dependencies in /tmp directory.
# doing it this way also installs any newly added dependencies.
RUN pip3 install --upgrade pip
ADD requirements/ /tmp/requirements
RUN pip3 install -r /tmp/$requirements

# load project files and set work directory
COPY . /app/
WORKDIR /app

COPY start.sh /start.sh
CMD ["/start.sh"]