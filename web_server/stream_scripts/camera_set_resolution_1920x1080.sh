#!/bin/sh
video=$(ls /sys/class/video4linux -1 | head -n1)
sudo v4l2-ctl -d /dev/$video --set-fmt-video=width=1920,height=1080,pixelformat=MJPG -p 30