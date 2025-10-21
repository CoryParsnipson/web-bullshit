#!/bin/bash

# set up xvfb window for headful browsing
echo "Running xvfb on Display ${DISPLAY}"
rm -f /tmp/.X99-lock
Xvfb $DISPLAY -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &

sleep 1
echo "Running x11vnc on Display ${DISPLAY}"
x11vnc -display $DISPLAY -ncache -forever -nopw -bg &
