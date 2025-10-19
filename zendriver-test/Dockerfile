FROM ubuntu:noble

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=America/Los_Angeles

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENV DISPLAY=:0

# need to specifically set shell to bash for Debian images, which defaults to /bin/sh
SHELL [ "/bin/bash", "-c" ]

RUN apt-get update && \
	apt-get install -y adduser wget gnupg && \
	apt-get install -y python3 python3-pip && \
	ln -s /usr/bin/python3 /usr/bin/python && \
	apt-get install -y xvfb x11vnc xdotool && \
	rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google.asc > /dev/null
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && \
	apt-get install -y google-chrome-stable && \
	rm -rf /var/lib/apt/lists/*

RUN adduser --shell /bin/bash gwart

COPY docker-entrypoint.sh /home/gwart
COPY start-x.sh /home/gwart
COPY src /home/gwart

# using break-system-packages probably isn't a great idea, but it will work for now
RUN pip install --break-system-packages zendriver

USER gwart
WORKDIR /home/gwart

# must match user_data_dir parameter in python script
# premake this directory so that we can mount to it in docker and it will
# have the correct permission and owner
RUN mkdir /home/gwart/chrome_data

ENTRYPOINT [ "bash", "-c", "-l", "./docker-entrypoint.sh" ]
