#!/bin/bash

# set up xvfb window for headful browsing
export DISPLAY=:0
Xvfb $DISPLAY -screen 0 1920x1080x24 &

sleep 1
x11vnc -display $DISPLAY -ncache -forever -nopw -bg &

# run app
python main.py
