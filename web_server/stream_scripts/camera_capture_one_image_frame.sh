#!/bin/sh
video=$(ls /sys/class/video4linux -1 | head -n1)
sudo v4l2-ctl -d /dev/$video --stream-mmap --stream-to=$1 --stream-count=1 > /dev/null
