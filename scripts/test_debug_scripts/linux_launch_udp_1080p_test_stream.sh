#!/bin/sh
HOST=`awk -F' ' '{print $(1)}' /home/pi/.microscope/host_ip.conf`

PID_TO_KILL=`pgrep gst-launch-1.0`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

gst-launch-1.0 videotestsrc ! videoconvert ! video/x-raw,width=1920,height=1080,format=YUY2 ! jpegenc ! rtpjpegpay ! udpsink host=$HOST port=5602 > /dev/null &

pid=`pgrep gst-launch-1.0`
exit $pid
