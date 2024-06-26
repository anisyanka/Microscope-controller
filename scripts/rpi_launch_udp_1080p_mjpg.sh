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
sudo v4l2-ctl -d /dev/$video --set-fmt-video=width=1920,height=1080,pixelformat=MJPG -p 30 > /dev/null
gst-launch-1.0 -v --eos-on-shutdown v4l2src device=/dev/$video io-mode=4 ! image/jpeg,width=1920,height=1080,type=video,framerate=30/1 ! rtpjpegpay ! queue ! udpsink host=$HOST port=5602 > /dev/null &

pid=`pgrep gst-launch-1.0`
exit $pid
