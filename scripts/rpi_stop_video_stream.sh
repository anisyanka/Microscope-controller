#!/bin/sh
PID_TO_KILL=`pgrep gst-launch-1.0`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "gstreamer process doesn't exist"
fi
