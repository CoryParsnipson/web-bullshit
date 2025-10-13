FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

USER pwuser
WORKDIR /home/pwuser

COPY src /home/pwuser

ENV PATH="/home/pwuser/.local/bin:$PATH"

RUN cd /home/pwuser && \
	pip install -r requirements.txt
