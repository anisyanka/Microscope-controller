#!/bin/sh
PID1=`pgrep gst-launch-1.0`
PID2=`pgrep v4l2-ctl`

if [ ! -z "${PID1}" ]; then
    echo "kill pid=$PID1"
    sudo kill -9 $PID1 > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

if [ ! -z "${PID2}" ]; then
    echo "kill pid=$PID2"
    sudo kill -9 $PID2 > /dev/null
else
    echo "v4l2-ctl process doesn't exist"
fi
