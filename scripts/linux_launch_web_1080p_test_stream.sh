PID_TO_KILL=`pgrep gst-launch-1.0`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

gst-launch-1.0 videotestsrc ! videoconvert ! videoscale ! video/x-raw,width=320,height=240 ! theoraenc ! oggmux ! tcpserversink host=0.0.0.0 port=5602 > /dev/null &

pid=`pgrep gst-launch-1.0`
exit $pid
