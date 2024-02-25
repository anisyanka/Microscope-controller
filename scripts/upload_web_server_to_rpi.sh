#!/bin/sh
microscope_contoller_scr_dir=Microscope-controller
web_dir=$microscope_contoller_scr_dir/web_server


rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "mkdir -p $web_dir; mkdir -p $web_dir/templates;" 
ssh $rpi_user@$rpi_ip "mkdir -p $web_dir/static; mkdir -p $web_dir/static/css; mkdir -p $web_dir/static/images; mkdir -p $web_dir/static/scripts; mkdir -p $web_dir/stream_scripts;" 

# Send css
scp $web_dir/static/css/styles.css \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/static/css

# Send images
scp $web_dir/static/images/favicon.ico \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/static/images

# Send js scripts
scp $web_dir/static/scripts/video_control.js \
    $web_dir/static/scripts/buttons_control.js \
    $web_dir/static/scripts/get_battery_level.js \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/static/scripts

# Send stream scripts
scp $web_dir/stream_scripts/camera_set_resolution_4k.sh \
    $web_dir/stream_scripts/camera_set_resolution_1920x1080.sh \
    $web_dir/stream_scripts/camera_capture_image.sh \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/stream_scripts

# Send Flask web-server
scp $web_dir/templates/index.html \
    $web_dir/templates/layout.html \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/templates
scp $web_dir/microscope_server.py \
    $web_dir/helpers.py \
    $web_dir/stream_control.py \
    $web_dir/config_reader.py \
    $web_dir/microscope_modbus.py \
    $web_dir/microscope_server.service \
    $web_dir/requirements.txt \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/

# Send config
scp $web_dir/microscope_server.conf \
        $rpi_user@$rpi_ip:/home/pi/$web_dir/

ssh $rpi_user@$rpi_ip "chmod +x $web_dir/microscope_server.py"
