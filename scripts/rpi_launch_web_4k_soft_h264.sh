#!/bin/sh
PID_TO_KILL=`pgrep gst-launch-1.0`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

sudo v4l2-ctl -d /dev/video0 --set-fmt-video=width=4656,height=3496,pixelformat=MJPG -p 10 > /dev/null
gst-launch-1.0 -v v4l2src device=/dev/video0 io-mode=4 ! image/jpeg,width=4656,height=3496,type=video,framerate=10/1 ! jpegdec ! videoconvert ! x264enc tune=zerolatency ! rtph264pay ! queue ! tcpserversink host=0.0.0.0 port=5602 > /dev/null &

pid=`pgrep gst-launch-1.0`
exit $pid
