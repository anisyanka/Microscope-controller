#!/bin/sh
sudo v4l2-ctl -d /dev/video0 --stream-mmap --stream-to=/home/pi/.microscope/web_server/tmp.img --stream-count=1
