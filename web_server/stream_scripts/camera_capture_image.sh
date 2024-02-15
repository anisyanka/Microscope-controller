#!/bin/sh
sudo v4l2-ctl -d /dev/video0 --stream-mmap --stream-to=$1 --stream-count=1 > /dev/null
