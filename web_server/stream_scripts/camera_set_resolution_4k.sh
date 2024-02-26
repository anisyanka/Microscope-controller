#!/bin/sh
video=$(ls /sys/class/video4linux -1 | head -n1)
sudo v4l2-ctl -d /dev/$video --set-fmt-video=width=4656,height=3496,pixelformat=MJPG -p 10