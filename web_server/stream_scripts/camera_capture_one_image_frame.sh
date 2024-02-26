#!/bin/sh
sudo v4l2-ctl -d /dev/$(ls /sys/class/video4linux -1 | head -n1) --stream-mmap --stream-to=$1 --stream-count=1