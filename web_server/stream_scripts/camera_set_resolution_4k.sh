#!/bin/sh
v4l2-ctl -d /dev/video0 --set-fmt-video=width=4656,height=3496,pixelformat=MJPG -p 10