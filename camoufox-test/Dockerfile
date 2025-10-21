FROM ubuntu:noble

ARG TZ=America/Los_Angeles

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENV DISPLAY=:0

# install required distro packages
RUN apt-get update && apt-get install -y \
	adduser xvfb x11vnc xdotool python3 python3-pip \
  # these are camoufox dependencies
	libgtk-3-0 libx11-xcb1 libasound2t64 \
	&& ln -s /usr/bin/python3 /usr/bin/python \
	&& rm -rf /var/lib/apt/lists/*

# create non root user
RUN adduser --shell /bin/bash gwart

USER gwart
WORKDIR /home/gwart

# install camoufox
RUN pip install --break-system-packages camoufox && \
	python -m camoufox fetch

# copy project code into container
COPY docker /home/gwart/docker
COPY src /home/gwart/src

ENTRYPOINT [ "bash", "-c", "-l", "./docker/entrypoint.sh" ]
