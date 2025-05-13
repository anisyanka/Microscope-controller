#!/bin/sh

# $1 - width
# $2 - height
# $3 - framerate
# $4 - 1-write video to file and udp simultaneously. 0 - not.
# $5 - video duration time in seconds


video=$(ls /sys/class/video4linux -1 | head -n1)
v4l2-ctl -d /dev/$video --set-fmt-video=width=$1,height=$2,pixelformat=MJPG -p $3

video_root_dir="/home/pi/.microscope/videos"
new_dir_name=`date +%d.%m.%y_%H.%M.%S`

if [ $4 -eq 0 ] ; then
    gst-launch-1.0 -v --eos-on-shutdown v4l2src device=/dev/$video io-mode=4 ! image/jpeg,width=$1,height=$2,type=video,framerate=$3/1 ! filesink location=/dev/stdout
else
    # Create dir depend on date and time
    mkdir -p $video_root_dir/$new_dir_name

    gst-launch-1.0 -v --eos-on-shutdown v4l2src device=/dev/$video io-mode=4 ! image/jpeg,width=$1,height=$2,type=video,framerate=$3/1 ! tee name=t \
    t. ! queue ! filesink location=/dev/stdout \
    t. ! queue ! jpegdec ! videoconvert ! x264enc key-int-max=10 tune=zerolatency ! h264parse ! splitmuxsink location="$video_root_dir/$new_dir_name/%010d.mp4" max-size-time="$5"000000000
fi
