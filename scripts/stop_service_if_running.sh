#!/bin/sh
if systemctl is-active --quiet $1 ; then
    echo "$1 is running, so stop it"
	sudo systemctl stop $1
else
    echo "$1 is inactive"
fi

PID1=`pgrep gst-launch-1.0`
PID2=`pgrep v4l2-ctl`

if [ ! -z "${PID1}" ]; then
    echo "kill pid=$PID1"
    sudo kill $PID1 > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

if [ ! -z "${PID2}" ]; then
    echo "kill pid=$PID2"
    sudo killall v4l2-ctl > /dev/null
else
    echo "v4l2-ctl process doesn't exist"
fi
