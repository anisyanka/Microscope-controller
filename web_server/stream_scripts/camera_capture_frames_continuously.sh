#!/bin/sh

# $1 - width
# $2 - height
# $3 - framerate


video=$(ls /sys/class/video4linux -1 | head -n1)
v4l2-ctl -d /dev/$video --set-fmt-video=width=$1,height=$2,pixelformat=MJPG -p $3
gst-launch-1.0 -v --eos-on-shutdown v4l2src device=/dev/$video io-mode=4 ! image/jpeg,width=$1,height=$2,type=video,framerate=$3/1 ! filesink location=/dev/stdout