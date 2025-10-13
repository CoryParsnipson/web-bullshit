#!/bin/bash

# set up xvfb window for headful browsing
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
x11vnc -display $DISPLAY -forever -nopw -bg &

# run app
python main.py
