#!/bin/sh
sudo v4l2-ctl -d /dev/video0 --stream-mmap --stream-to=/home/pi/.modbus_converter/web_viewer/tmp.img --stream-count=1
