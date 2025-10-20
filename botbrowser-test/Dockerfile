FROM debian:bookworm-slim

# Path to BotBrowser binary
ENV BOTBROWSER_EXEC_PATH=/usr/bin/chromium-browser-stable

# Display for Xvfb if you want to launch browser with headful mode
ENV DISPLAY=:99

# Expose Chrome DevTools Protocol port
EXPOSE 9222

# Install runtime dependencies and Xvfb
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb dbus-x11 x11vnc ca-certificates wget \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libgbm1 libgtk-3-0 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libxkbcommon0 libpangocairo-1.0-0 libpango-1.0-0 \
    libwayland-client0 libwayland-server0 libdbus-1-3 libatspi2.0-0 \
    fonts-liberation libu2f-udev libcurl3-gnutls libcurl4 libvulkan1 xdg-utils \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy and install BotBrowser package
RUN wget -q https://github.com/botswin/BotBrowser/releases/download/v141-20251012/botbrowser_20251013_141.0.7390.77_x86_64.deb && \
	dpkg -i botbrowser_*.deb || apt-get update && apt-get install -f -y && \
  rm botbrowser_*.deb

# install python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Set working directory
WORKDIR /botbrowser

COPY docker-entrypoint.sh /botbrowser
COPY start-x.sh /botbrowser
COPY requirements.txt /botbrowser

COPY src /botbrowser/src

RUN pip install --break-system-packages -r requirements.txt

# Declare mount points for profiles and user data
VOLUME ["/botbrowser/profiles", "/botbrowser/user-data-dir"]

# ENTRYPOINT: start Xvfb then Chromium with CDP and user args
ENTRYPOINT [ "./docker-entrypoint.sh" ]
