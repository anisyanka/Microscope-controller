#!/bin/sh
HOST=`awk -F' ' '{print $(1)}' /home/pi/.microscope/host_ip.conf`

PID_TO_KILL=`pgrep gst-launch-1.0`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "gstreamer process doesn't exist"
fi

video=$(ls /sys/class/video4linux -1 | head -n1)
sudo v4l2-ctl -d /dev/$video --set-fmt-video=width=4656,height=3496,pixelformat=MJPG -p 10 > /dev/null
gst-launch-1.0 -v v4l2src device=/dev/$video io-mode=4 ! image/jpeg,width=4656,height=3496,type=video,framerate=10/1 ! jpegdec ! videoconvert ! x264enc tune=zerolatency ! rtph264pay ! udpsink host=$HOST port=5602 > /dev/null &

pid=`pgrep gst-launch-1.0`
exit $pid
