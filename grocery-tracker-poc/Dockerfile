FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

# install x11vnc
RUN apt-get update && \
	apt-get install -y x11vnc

USER pwuser
WORKDIR /home/pwuser

COPY docker-entrypoint.sh /home/pwuser

# copy app source code
COPY src /home/pwuser

# need this so we can run playwright executable
ENV PATH="/home/pwuser/.local/bin:$PATH"

# can be used in python scripts to figure out which environment we are in
ENV IN_DOCKER=true 
ENV ENVIRONMENT=dev

# install python dependencies
RUN cd /home/pwuser && \
	pip install -r requirements.txt

ENTRYPOINT [ "./docker-entrypoint.sh" ]
